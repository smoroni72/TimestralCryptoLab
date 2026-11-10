# M1: prima attività, pipeline OHLCV

10 novembre 2026. Base verificata: `23b099f449647d016db19e1b272e5ced520efa6b`,
checkout ufficiale Windows, `main`, working tree inizialmente pulito, unico remote
`https://github.com/smoroni72/TimestralCryptoLab.git`. Nessun push eseguito.

## Implementato

Download Binance Public Data spot incrementale per archivio e riprendibile via
HTTP Range; checksum ufficiali SHA-256; parser ms/us per riga; candele native
15m/1h; Parquet UTC; controlli OHLCV, gap, duplicati, completezza; quarantena e
manifest con provenienza/versioni/hash/esclusioni. [Comandi e schema](../docs/wiki/data-pipeline.md).
Il periodo M1 `[2023-01-01,2026-10-01)` e gli split non sono stati modificati.

## Verifiche osservate

Ambiente: Windows 11 (build 26200), Python 3.12.10, PyArrow 23.0.1, venv locale.
Installazione editable con `python -m pip --python .venv install -e .` riuscita
nell'ambiente autorizzato dopo un errore di permessi dei temporanei nella sandbox.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

21 test offline superati: ms/us al cambio anno, 15m, close inclusivo, fine esclusiva,
NaN/inf/prezzi/volumi invalidi, candele aperte, disallineamenti, duplicati identici
e discordanti, gap ai bordi/interni, piano mensile/giornaliero, cache alterata,
checksum mancanti/malformati, HTTP 403, Range 206/200/416, risposte troncate,
schema/round trip Parquet, idempotenza, quarantena, manifest fallito e lock.
Nessuna rete richiesta dalla suite. Una fixture iniziale aveva URL fittizio
non valido: corretta prima del risultato finale. La sandbox ha negato l'accesso
ai temporanei anche sotto il checkout; suite eseguita con autorizzazione esterna.

Smoke reale eseguito, con codice in sviluppo (`code_dirty=true`):

```powershell
.\.venv\Scripts\python.exe -m timestral_crypto_lab.data --symbols BTCUSDT --intervals 1h --start 2025-01-01 --end 2025-01-02 --output data/smoke-us
```

Esito `validated`, 24 righe, unità us, zero esclusioni/conflitti/gap.
Fonte:
`https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2025-01-01.zip`.
SHA-256 ufficiale e locale:
`8077644eb5088200969b135d7046ba777281be303fa32aceff28fe3baeaa5873`.
Hash canonico:
`12c09dae87148004f220c6a7627ec59b4549545486c340451f91d7696a3a823a`.
Download osservato `2026-11-10T15:09:09.219341+00:00`.
Archivi e Parquet sotto `data/smoke-us/`, esclusi da Git.

Ricostruzione del medesimo campione con `--offline` sul codice finale riuscita:
24 righe `validated`, nessuna richiesta di rete, SHA canonico invariato.

Verifica documentale: 25 file Markdown, 68 link locali, nessuna destinazione
mancante. `git diff --check` senza errori. `git check-ignore` conferma l'esclusione
di manifest runtime, Parquet, `.venv` e `.cache`.

## File della consegna

Creati: `pyproject.toml`, `config/m1-data.json`,
`src/timestral_crypto_lab/__init__.py`, `src/timestral_crypto_lab/data.py`,
`tests/test_data.py`, `docs/wiki/data-pipeline.md`, `reports/m1-data-pipeline.md`.

Modificati: `.gitignore`, `README.md`, `PRD.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
`config/README.md`, `src/README.md`, `tests/README.md`, `docs/wiki/README.md`,
`docs/wiki/data-contracts.md`, `docs/wiki/testing.md`, `docs/wiki/status.md`,
`docs/wiki/timestral-validation.md`.

## Limiti

Connessione Binance dalla sandbox rifiutata (WinError 10061). Smoke riuscito solo
dopo autorizzazione esplicita fuori sandbox; nessun proxy o aggiramento usato.
Il campione reale copre BTCUSDT/1h/us: gli altri casi sono fixture offline,
non evidenza della completezza di BTC/SOL per tutto il periodo M1.
Il dataset completo non è stato acquisito. Non sono stati eseguiti benchmark
previsionali, inferenze, test di trading, misure hardware o deployment.

La cache congela gli archivi: nuove correzioni della fonte richiedono un output
separato. Ripresa testata via HTTP simulato, non con interruzione reale di rete.
Nessuna aggregazione, imputation o selezione di modelli. Float64 introduce
arrotondamento esplicito dei decimali. Versioni dirette fissate; nessun lock con
hash multipiattaforma. La M1 complessiva non è completata.
