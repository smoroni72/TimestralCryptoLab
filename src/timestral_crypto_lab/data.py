"""Binance spot archive snapshots. All date ranges are UTC and end-exclusive."""

import argparse
import csv
import hashlib
import io
import http.client
import json
import math
import platform
import re
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path

BASE = "https://data.binance.vision/data/spot"
STEPS = {"15m": 900_000_000, "1h": 3_600_000_000}
EPOCH = datetime(1970, 1, 1, tzinfo=UTC)
NAMES = ["open_time", "close_time", "open", "high", "low", "close", "volume", "quote_volume"]


def utc(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        result = result.replace(tzinfo=UTC)
    return result.astimezone(UTC)


def micros(value):
    delta = value - EPOCH
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds


def iso(value):
    return (EPOCH + timedelta(microseconds=value)).isoformat()


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def plan(symbol, interval, start, end):
    """Monthly archives for complete months, daily archives for boundary days."""
    cursor = start.replace(hour=0, minute=0, second=0, microsecond=0)
    while cursor < end:
        month = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)
        if cursor.day == 1 and cursor >= start and month <= end:
            cadence, stamp, following = "monthly", cursor.strftime("%Y-%m"), month
        else:
            cadence, stamp, following = "daily", cursor.strftime("%Y-%m-%d"), cursor + timedelta(days=1)
        name = f"{symbol}-{interval}-{stamp}.zip"
        yield f"{BASE}/{cadence}/klines/{symbol}/{interval}/{name}"
        cursor = following


def download(url, target, opener=urllib.request.urlopen):
    """Keep .part on interruption; Range is verified before appending."""
    partial = target.with_suffix(target.suffix + ".part")
    offset = partial.stat().st_size if partial.exists() else 0
    request = urllib.request.Request(url, headers={"Range": f"bytes={offset}-"} if offset else {})
    try:
        response = opener(request, timeout=30)
    except urllib.error.HTTPError as exc:
        if exc.code == 416 and offset:
            partial.unlink()
            return download(url, target, opener)
        raise
    with response:
        status = response.status
        append = offset > 0 and status == 206
        if status not in (200, 206):
            raise ValueError(f"Unexpected HTTP status: {status}")
        if status == 206:
            match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
            if not match or int(match[1]) != offset or int(match[2]) != int(match[3]) - 1:
                raise ValueError("Invalid Content-Range; partial file preserved")
        with partial.open("ab" if append else "wb") as output:
            received = 0
            while block := response.read(1024 * 1024):
                output.write(block)
                received += len(block)
        length = str(int(match[2]) - int(match[1]) + 1) if status == 206 else response.headers.get("Content-Length")
        if length is not None and received != int(length):
            raise ValueError("Truncated HTTP response; retry to resume")
    partial.replace(target)


def acquire(url, root, offline=False, allow_missing=False, opener=urllib.request.urlopen):
    # Preserve original archive layout; no credentials, no API/order endpoints.
    target = root / "raw" / url.removeprefix(BASE + "/")
    target.parent.mkdir(parents=True, exist_ok=True)
    sidecar = target.with_suffix(".zip.CHECKSUM")
    metadata = target.with_suffix(".zip.meta.json")
    if not sidecar.exists() and not offline:
        try:
            download(url + ".CHECKSUM", sidecar, opener)
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
    expected = None
    if sidecar.exists():
        parts = sidecar.read_text(encoding="utf-8").split()
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]) or parts[1].lstrip("*") != target.name:
            raise ValueError(f"Malformed checksum: {sidecar}")
        expected = parts[0].lower()
    if expected is None and not allow_missing:
        raise ValueError(f"Official checksum unavailable: {url}")
    if not target.exists():
        if offline:
            raise ValueError(f"Archive absent in offline cache: {url}")
        download(url, target, opener)
        atomic_json(metadata, {"downloaded_at": datetime.now(UTC).isoformat()})
    digest = sha(target)
    if expected and digest != expected:
        # Keep the suspect file as evidence; never silently accept/rewrite it.
        raise ValueError(f"SHA-256 mismatch: {target}; move suspect archive aside before retry")
    return target, {
        "url": url, "checksum_url": url + ".CHECKSUM", "sha256": digest,
        "official_sha256": expected, "checksum_status": "verified" if expected else "unavailable",
        "downloaded_at": json.loads(metadata.read_text())["downloaded_at"] if metadata.exists() else None,
        "cache_path": str(target.relative_to(root)),
    }


def timestamp(raw):
    value = int(raw)
    # Restrict to contemporary Binance history; reject seconds/ns rather than guessing.
    if 1_000_000_000_000 <= value < 10_000_000_000_000:
        return value * 1000, "ms", 1000
    if 1_000_000_000_000_000 <= value < 10_000_000_000_000_000:
        return value, "us", 1
    raise ValueError("Unsupported timestamp magnitude")


def normalize(path, interval, start_us, end_us, as_of_us):
    rows, exclusions, units = [], [], Counter()
    step = STEPS[interval]
    with zipfile.ZipFile(path) as archive:
        entries = archive.namelist()
        if entries != [path.stem + ".csv"]:
            raise ValueError(f"Unexpected ZIP members: {entries}")
        with archive.open(entries[0]) as source:
            for number, fields in enumerate(csv.reader(io.TextIOWrapper(source, encoding="utf-8-sig")), 1):
                reason = None
                opened = None
                try:
                    if len(fields) != 12:
                        raise ValueError("Expected 12 Binance kline columns")
                    opened, unit, tick = timestamp(fields[0])
                    closed, close_unit, _ = timestamp(fields[6])
                    units[unit] += 1
                    if not start_us <= opened < end_us:
                        reason = "outside_requested_period"
                    elif unit != close_unit or opened % step or closed != opened + step - tick:
                        reason = "invalid_interval"
                    elif opened + step > as_of_us or opened + step > end_us:
                        reason = "incomplete_candle"
                    values = [float(fields[i]) for i in (1, 2, 3, 4, 5, 7)]
                    o, h, low, c, volume, quote = values
                    if reason is None:
                        if not all(math.isfinite(v) for v in values):
                            reason = "non_finite"
                        elif min(o, h, low, c) <= 0 or not low <= min(o, c) <= max(o, c) <= h:
                            reason = "invalid_price"
                        elif volume < 0 or quote < 0:
                            reason = "negative_volume"
                    if reason is None:
                        rows.append((opened, closed, *values))
                except (ValueError, OverflowError):
                    reason = "malformed_row"
                if reason:
                    exclusions.append({"line": number, "open_time_us": opened, "reason": reason})
    return rows, exclusions, dict(units)


def quality(rows, interval, start_us, end_us):
    """Drop identical duplicates; exclude *all* records at conflicting timestamps."""
    by_time, conflicts = {}, set()
    counts = Counter({"out_of_order": 0, "duplicate_timestamp": 0})
    previous = None
    for row in rows:
        if previous is not None and row[0] < previous:
            counts["out_of_order"] += 1
        previous = row[0]
        if row[0] in by_time:
            counts["duplicate_timestamp"] += 1
            if row != by_time[row[0]]:
                conflicts.add(row[0])
        else:
            by_time[row[0]] = row
    counts["conflicting_timestamps"] = len(conflicts)
    clean = [by_time[t] for t in sorted(by_time) if t not in conflicts]
    step = STEPS[interval]
    gaps, cursor = [], start_us
    for row in clean:
        if row[0] > cursor:
            gaps.append({"start": iso(cursor), "end_exclusive": iso(row[0]), "candles": (row[0] - cursor) // step})
        cursor = row[0] + step
    if cursor < end_us:
        gaps.append({"start": iso(cursor), "end_exclusive": iso(end_us), "candles": (end_us - cursor) // step})
    counts["missing_intervals"] = sum(g["candles"] for g in gaps)
    return clean, dict(counts), gaps, sorted(conflicts)


def write_parquet(path, rows, symbol, interval):
    import pyarrow as pa
    import pyarrow.parquet as pq

    fields = [pa.field(n, pa.timestamp("us", tz="UTC") if i < 2 else pa.float64(), nullable=False)
              for i, n in enumerate(NAMES)]
    fields += [pa.field("symbol", pa.string(), nullable=False), pa.field("interval", pa.string(), nullable=False),
               pa.field("venue", pa.string(), nullable=False), pa.field("is_closed", pa.bool_(), nullable=False)]
    columns = [[r[i] for r in rows] for i in range(len(NAMES))]
    columns += [[symbol] * len(rows), [interval] * len(rows), ["binance_spot"] * len(rows), [True] * len(rows)]
    table = pa.Table.from_arrays([pa.array(c, type=f.type) for c, f in zip(columns, fields)], schema=pa.schema(fields))
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".parquet.tmp")
    pq.write_table(table, temp, compression="zstd", version="2.6")
    temp.replace(path)
    # Independent of Parquet encoding/library metadata; integer us + float.hex values.
    canonical = hashlib.sha256()
    for row in rows:
        canonical.update((",".join([str(row[0]), str(row[1]), *(v.hex() for v in row[2:])]) + "\n").encode("ascii"))
    return {"parquet_sha256": sha(path), "canonical_sha256": canonical.hexdigest(), "rows": len(rows)}


def run(config, root, *, offline=False, allow_missing=False, as_of=None, opener=urllib.request.urlopen):
    import pyarrow

    start, end = utc(config["start"]), utc(config["end"])
    symbols, intervals = config["symbols"], config["intervals"]
    if not symbols or not intervals or len(set(symbols)) != len(symbols) or len(set(intervals)) != len(intervals):
        raise ValueError("Symbols/intervals must be non-empty and unique")
    if any(not re.fullmatch(r"[A-Z0-9]+USDT", s) for s in symbols) or any(i not in STEPS for i in intervals):
        raise ValueError("Only spot USDT symbols and 15m/1h intervals are supported")
    if start >= end or any(micros(t) % STEPS[i] for i in intervals for t in (start, end)):
        raise ValueError("Dates must be ordered and aligned to every requested interval")
    now = as_of or datetime.now(UTC)
    try:
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True))
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    manifest = {
        "schema_version": 1, "dataset_version": "binance-spot-native-v1", "created_at": now.isoformat(),
        "as_of": now.isoformat(), "config": config, "code_revision": revision, "code_dirty": dirty,
        "python": platform.python_version(), "pyarrow": pyarrow.__version__, "platform": platform.platform(),
        "pipeline_sha256": sha(Path(__file__)),
        "policy": {"range": "[start,end)", "gap_fill": False, "hourly": "native",
                   "checksum_required": not allow_missing, "canonical": "ordered integer UTC us,float.hex OHLCV lines v1"},
        "datasets": [], "status": "running",
    }
    root.mkdir(parents=True, exist_ok=True)
    # One writer per output directory. OS releases the lock on exceptions/process exit.
    lock = root / ".pipeline.lock"
    try:
        descriptor = lock.open("x")
    except FileExistsError:
        raise ValueError(f"Output locked: {lock}; verify no writer is running before removing stale lock") from None
    with descriptor:
        try:
            for symbol in symbols:
                for interval in intervals:
                    dataset = {"symbol": symbol, "interval": interval, "sources": [], "exclusions": []}
                    manifest["datasets"].append(dataset)
                    rows = []
                    for url in plan(symbol, interval, start, end):
                        source = {"url": url, "acquisition_status": "pending"}
                        dataset["sources"].append(source)
                        try:
                            path, provenance = acquire(url, root, offline, allow_missing, opener)
                        except Exception as exc:
                            source.update({"acquisition_status": "failed", "error": f"{type(exc).__name__}: {exc}"})
                            raise
                        source.update(provenance)
                        source["acquisition_status"] = "verified" if provenance["official_sha256"] else "unverified"
                        parsed, excluded, units = normalize(path, interval, micros(start), micros(end), micros(now))
                        source.update({"timestamp_units": units, "input_rows": len(parsed) + len(excluded),
                                       "accepted_rows_before_deduplication": len(parsed), "excluded_rows": len(excluded)})
                        dataset["exclusions"].extend({"source": url, **e} for e in excluded)
                        rows.extend(parsed)
                    clean, anomalies, gaps, conflicts = quality(rows, interval, micros(start), micros(end))
                    invalid = [e for e in dataset["exclusions"] if e["reason"] != "outside_requested_period"]
                    valid = not invalid and not anomalies["missing_intervals"] and not conflicts
                    # Quarantine incomplete/invalid series; downstream must require status=validated.
                    relative = Path("normalized" if valid else "quarantine") / f"{symbol}-{interval}-{start:%Y%m%dT%H%M%S}-{end:%Y%m%dT%H%M%S}.parquet"
                    dataset.update(write_parquet(root / relative, clean, symbol, interval))
                    dataset.update({"path": relative.as_posix(), "status": "validated" if valid else "rejected",
                                    "anomalies": anomalies, "gaps": gaps, "conflicting_open_times_us": conflicts,
                                    "actual_start": iso(clean[0][0]) if clean else None,
                                    "actual_end_exclusive": iso(clean[-1][0] + STEPS[interval]) if clean else None})
            manifest["status"] = "validated" if all(d["status"] == "validated" for d in manifest["datasets"]) else "rejected"
        except Exception as exc:
            manifest["status"] = "failed"
            manifest["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            try:
                identifier = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
                atomic_json(root / "manifests" / f"{identifier}.json", manifest)
                atomic_json(root / "manifest.json", manifest)
            finally:
                descriptor.close()
                lock.unlink()
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/m1-data.json"))
    parser.add_argument("--symbols", nargs="+")
    parser.add_argument("--intervals", nargs="+", choices=list(STEPS))
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--output", type=Path, default=Path("data/m1"))
    parser.add_argument("--offline", action="store_true", help="Read cache only; zero network")
    parser.add_argument("--allow-missing-checksum", action="store_true", help="Explicit audited exception for HTTP 404/missing sidecar")
    args = parser.parse_args(argv)
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        for key in ("symbols", "intervals", "start", "end"):
            if getattr(args, key) is not None:
                config[key] = getattr(args, key)
        result = run(config, args.output, offline=args.offline, allow_missing=args.allow_missing_checksum)
        print(f"{result['status']}: {args.output / 'manifest.json'}")
        return 0 if result["status"] == "validated" else 2
    except (OSError, ValueError, zipfile.BadZipFile, http.client.HTTPException) as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
