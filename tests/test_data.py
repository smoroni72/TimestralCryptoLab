import hashlib
import io
import json
import tempfile
import unittest
import urllib.error
import zipfile
from datetime import timedelta
from pathlib import Path

import pyarrow.parquet as pq

from timestral_crypto_lab.data import (
    BASE, STEPS, acquire, download, micros, normalize, plan, quality, run, utc,
)


def candle(when="2025-01-01", interval="1h", unit="us", **changes):
    tick = 1 if unit == "us" else 1000
    opened = micros(utc(when))
    row = [str(opened // tick), "10", "12", "9", "11", "2",
           str((opened + STEPS[interval]) // tick - 1), "21", "4", "1", "10", "0"]
    for index, value in changes.items():
        row[int(index)] = value
    return ",".join(row)


def archive(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as output:
        output.writestr(path.stem + ".csv", "\n".join(lines) + "\n")
    path.with_suffix(".zip.CHECKSUM").write_text(
        hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.name, encoding="utf-8")


class Response(io.BytesIO):
    def __init__(self, body, status=200, **headers):
        super().__init__(body)
        self.status = status
        self.headers = headers


class PipelineTests(unittest.TestCase):
    def setUp(self):
        cache = Path(__file__).resolve().parents[1] / ".cache" / "tests"
        cache.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=cache)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def parse(self, lines, start="2024-12-31T23:00:00Z", end="2025-01-02", as_of="2025-01-03", interval="1h"):
        path = self.root / "fixture.zip"
        archive(path, lines)
        return normalize(path, interval, micros(utc(start)), micros(utc(end)), micros(utc(as_of)))

    def test_units_transition_preserves_close_precision(self):
        rows, excluded, units = self.parse([
            candle("2024-12-31T23:00:00Z", unit="ms"), candle()])
        self.assertEqual(excluded, [])
        self.assertEqual(units, {"ms": 1, "us": 1})
        self.assertEqual(rows[1][0] - rows[0][0], STEPS["1h"])
        self.assertEqual(rows[0][1] % 1_000_000, 999000)
        self.assertEqual(rows[1][1] % 1_000_000, 999999)

    def test_15m(self):
        rows, excluded, _ = self.parse([candle(interval="15m")], interval="15m")
        self.assertEqual(len(rows), 1)
        self.assertEqual(excluded, [])

    def test_invalid_values(self):
        for changes, reason in [({"1": "0"}, "invalid_price"), ({"2": "10"}, "invalid_price"),
                                ({"3": "13"}, "invalid_price"), ({"5": "-1"}, "negative_volume"),
                                ({"7": "-2"}, "negative_volume"), ({"4": "NaN"}, "non_finite"),
                                ({"5": "inf"}, "non_finite"), ({"1": "bad"}, "malformed_row"),
                                ({"0": "1735689600"}, "malformed_row"),
                                ({"6": "1735693200000000"}, "invalid_interval")]:
            with self.subTest(changes=changes):
                rows, excluded, _ = self.parse([candle(**changes)])
                self.assertEqual(rows, [])
                self.assertEqual(excluded[0]["reason"], reason)

    def test_incomplete_and_exclusive_end(self):
        rows, excluded, _ = self.parse([candle()], as_of="2025-01-01T00:30:00Z")
        self.assertEqual(rows, [])
        self.assertEqual(excluded[0]["reason"], "incomplete_candle")
        rows, excluded, _ = self.parse([candle()], end="2025-01-01")
        self.assertEqual(excluded[0]["reason"], "outside_requested_period")

    def test_misalignment_and_mixed_close_units(self):
        for row in [candle("2025-01-01T00:01:00Z"), candle(**{"6": "1735693199999"})]:
            self.assertEqual(self.parse([row])[1][0]["reason"], "invalid_interval")

    def test_duplicates_conflicts_order_and_boundary_gaps(self):
        first, _, _ = self.parse([candle()])
        row = first[0]
        later = (row[0] + 2 * STEPS["1h"], row[1] + 2 * STEPS["1h"], *row[2:])
        conflicting = (*row[:2], 10.5, *row[3:])
        clean, counts, gaps, conflicts = quality([later, row, row, conflicting], "1h", row[0] - STEPS["1h"], later[0] + 2 * STEPS["1h"])
        self.assertEqual(clean, [later])
        self.assertEqual(counts["duplicate_timestamp"], 2)
        self.assertEqual(counts["out_of_order"], 1)
        self.assertEqual(counts["missing_intervals"], 4)
        self.assertEqual([g["candles"] for g in gaps], [3, 1])
        self.assertEqual(conflicts, [row[0]])

    def test_identical_duplicates_are_deduplicated(self):
        rows = self.parse([candle(), candle()])[0]
        clean, counts, _, conflicts = quality(rows, "1h", rows[0][0], rows[0][0] + STEPS["1h"])
        self.assertEqual(len(clean), 1)
        self.assertEqual(conflicts, [])
        self.assertEqual(counts["missing_intervals"], 0)

    def test_monthly_daily_plan_no_overlap(self):
        urls = list(plan("BTCUSDT", "1h", utc("2024-12-31"), utc("2025-02-02")))
        self.assertEqual(len(urls), 3)
        self.assertIn("daily/klines/BTCUSDT/1h/BTCUSDT-1h-2024-12-31.zip", urls[0])
        self.assertIn("monthly/klines", urls[1])
        self.assertTrue(urls[2].endswith("2025-02-01.zip"))
        self.assertEqual(len(list(plan("SOLUSDT", "15m", utc("2023-01-01"), utc("2026-10-01")))), 45)

    def test_range_resume_and_range_ignored(self):
        target = self.root / "test.zip"
        partial = self.root / "test.zip.part"
        partial.write_bytes(b"abc")
        def opener(request, timeout):
            self.assertEqual(request.get_header("Range"), "bytes=3-")
            return Response(b"def", 206, **{"Content-Range": "bytes 3-5/6", "Content-Length": "3"})
        download("https://example.invalid", target, opener)
        self.assertEqual(target.read_bytes(), b"abcdef")
        partial.write_bytes(b"old")
        download("https://example.invalid", target, lambda *a, **kw: Response(b"new"))
        self.assertEqual(target.read_bytes(), b"new")

    def test_bad_range_preserves_partial(self):
        target = self.root / "test.zip"
        partial = self.root / "test.zip.part"
        partial.write_bytes(b"abc")
        with self.assertRaisesRegex(ValueError, "Content-Range"):
            download("https://example.invalid", target, lambda *a, **kw: Response(b"x", 206, **{"Content-Range": "bytes 0-0/1"}))
        self.assertEqual(partial.read_bytes(), b"abc")

    def test_truncated_response_can_resume(self):
        target = self.root / "test.zip"
        with self.assertRaisesRegex(ValueError, "Truncated"):
            download("https://example.invalid", target, lambda *a, **kw: Response(b"abc", **{"Content-Length": "6"}))
        self.assertFalse(target.exists())
        download("https://example.invalid", target, lambda *a, **kw: Response(b"def", 206, **{"Content-Range": "bytes 3-5/6"}))
        self.assertEqual(target.read_bytes(), b"abcdef")

    def test_checksum_and_cache_tampering(self):
        url = next(plan("BTCUSDT", "1h", utc("2025-01-01"), utc("2025-01-02")))
        path = self.root / "raw" / url.removeprefix(BASE + "/")
        archive(path, [candle()])
        _, source = acquire(url, self.root, offline=True)
        self.assertEqual(source["checksum_status"], "verified")
        path.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            acquire(url, self.root, offline=True)

    def test_missing_checksum_is_explicit_and_network_errors_not_ignored(self):
        url = next(plan("BTCUSDT", "1h", utc("2025-01-01"), utc("2025-01-02")))
        path = self.root / "raw" / url.removeprefix(BASE + "/")
        archive(path, [candle()])
        path.with_suffix(".zip.CHECKSUM").unlink()
        with self.assertRaisesRegex(ValueError, "unavailable"):
            acquire(url, self.root, offline=True)
        self.assertEqual(acquire(url, self.root, offline=True, allow_missing=True)[1]["checksum_status"], "unavailable")
        def forbidden(*a, **kw):
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
        with self.assertRaises(urllib.error.HTTPError):
            acquire(url, self.root, allow_missing=True, opener=forbidden)

    def seed_day(self, invalid=False):
        config = {"symbols": ["SOLUSDT"], "intervals": ["1h"], "start": "2025-01-01", "end": "2025-01-02"}
        url = next(plan("SOLUSDT", "1h", utc(config["start"]), utc(config["end"])))
        path = self.root / "raw" / url.removeprefix(BASE + "/")
        lines = [candle((utc("2025-01-01") + timedelta(hours=i)).isoformat()) for i in range(24)]
        if invalid:
            lines[7] = candle("2025-01-01T07:00:00Z", **{"5": "-2"})
        archive(path, lines)
        return config

    def test_offline_end_to_end_parquet_manifest_idempotence(self):
        config = self.seed_day()
        def no_network(*a, **kw):
            self.fail("Offline pipeline attempted network")
        first = run(config, self.root, offline=True, as_of=utc("2025-01-03"), opener=no_network)
        second = run(config, self.root, offline=True, as_of=utc("2025-01-03"), opener=no_network)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "validated")
        dataset = first["datasets"][0]
        table = pq.read_table(self.root / dataset["path"])
        self.assertEqual(table.num_rows, 24)
        self.assertEqual(str(table.schema.field("open_time").type), "timestamp[us, tz=UTC]")
        self.assertEqual(table["close"][0].as_py(), 11)
        self.assertTrue(table["is_closed"][0].as_py())
        self.assertEqual(json.loads((self.root / "manifest.json").read_text()), second)
        self.assertFalse((self.root / ".pipeline.lock").exists())

    def test_rejected_series_quarantined(self):
        result = run(self.seed_day(invalid=True), self.root, offline=True, as_of=utc("2025-01-03"))
        self.assertEqual(result["status"], "rejected")
        dataset = result["datasets"][0]
        self.assertTrue(dataset["path"].startswith("quarantine/"))
        self.assertEqual(dataset["rows"], 23)
        self.assertEqual(dataset["anomalies"]["missing_intervals"], 1)
        self.assertEqual(dataset["exclusions"][0]["reason"], "negative_volume")

    def test_failure_writes_manifest_and_releases_lock(self):
        config = self.seed_day()
        next(self.root.rglob("*.zip")).write_bytes(b"corrupt")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            run(config, self.root, offline=True)
        self.assertEqual(json.loads((self.root / "manifest.json").read_text())["status"], "failed")
        self.assertFalse((self.root / ".pipeline.lock").exists())

    def test_invalid_config_rejected_before_network(self):
        config = self.seed_day()
        for change in [{"start": "2025-01-01T00:01:00Z"}, {"symbols": ["../BTCUSDT"]},
                       {"end": "2024-01-01"}, {"intervals": ["1m"]}, {"symbols": []}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                run({**config, **change}, self.root)

    def test_writer_lock_preserves_existing_manifest(self):
        config = self.seed_day()
        (self.root / ".pipeline.lock").touch()
        (self.root / "manifest.json").write_text("existing")
        with self.assertRaisesRegex(ValueError, "locked"):
            run(config, self.root, offline=True)
        self.assertEqual((self.root / "manifest.json").read_text(), "existing")

    def test_range_416_restarts_download(self):
        target = self.root / "test.zip"
        target.with_suffix(".zip.part").write_bytes(b"stale")
        calls = []
        def opener(request, timeout):
            calls.append(request.get_header("Range"))
            if len(calls) == 1:
                raise urllib.error.HTTPError(request.full_url, 416, "Range", {}, None)
            return Response(b"fresh")
        download("https://example.invalid", target, opener)
        self.assertEqual(calls, ["bytes=5-", None])
        self.assertEqual(target.read_bytes(), b"fresh")

    def test_partial_response_length_checked_without_content_length(self):
        target = self.root / "test.zip"
        target.with_suffix(".zip.part").write_bytes(b"abc")
        with self.assertRaisesRegex(ValueError, "Truncated"):
            download("https://example.invalid", target,
                     lambda *a, **kw: Response(b"d", 206, **{"Content-Range": "bytes 3-5/6"}))

    def test_malformed_checksum_never_accepted(self):
        self.seed_day()
        path = next(self.root.rglob("*.CHECKSUM"))
        path.write_text("f" * 64 + "  wrong.zip")
        url = next(plan("SOLUSDT", "1h", utc("2025-01-01"), utc("2025-01-02")))
        with self.assertRaisesRegex(ValueError, "Malformed"):
            acquire(url, self.root, offline=True, allow_missing=True)


if __name__ == "__main__":
    unittest.main()
