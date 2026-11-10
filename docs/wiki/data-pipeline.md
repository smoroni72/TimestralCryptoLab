# Pipeline OHLCV M1

Implementata il 10 novembre 2026. Ambito: acquisizione e qualità dei dati spot,
senza Timestral, benchmark previsionale, trading o dashboard. Il periodo del
[protocollo M1](timestral-validation.md) rimane invariato:
`2023-01-01T00:00:00Z <= open_time < 2026-10-01T00:00:00Z`.
La configurazione è in [config/m1-data.json](../../config/m1-data.json).

## Installazione Windows

PowerShell, Python 3.12 a 64 bit. Non serve attivare l'ambiente né modificare
ExecutionPolicy. PyArrow 23.0.1 è l'unica dipendenza runtime: scrive e legge
Parquet con tipi UTC espliciti e compressione Zstandard. Setuptools 80.9.0 è
richiesto solo per il packaging. Download, parsing CSV, hash, CLI e test usano
la libreria standard; unittest evita una dipendenza di test aggiuntiva.

```powershell
Set-Location 'C:\Users\smoro\Documents\Codex\TimestralCryptoLab'
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

L'installazione richiede accesso all'indice dei pacchetti oppure wheel già
disponibili. Non viene installato alcun modello. Le versioni dirette sono
fissate in pyproject.toml; non è incluso un lock multipiattaforma con hash.

## Acquisizione

```powershell
# Tutto il periodo M1, quattro serie; non eseguito in questa consegna
.\.venv\Scripts\python.exe -m timestral_crypto_lab.data --config config/m1-data.json --output data/m1

# Campione reale piccolo, separato dal dataset M1
.\.venv\Scripts\python.exe -m timestral_crypto_lab.data --symbols BTCUSDT --intervals 1h --start 2025-01-01 --end 2025-01-02 --output data/smoke-us

# Ricostruzione usando soltanto archivi e checksum già in cache
.\.venv\Scripts\python.exe -m timestral_crypto_lab.data --symbols BTCUSDT --intervals 1h --start 2025-01-01 --end 2025-01-02 --output data/smoke-us --offline
```

Gli override `--symbols BTCUSDT SOLUSDT`, `--intervals 15m 1h`, `--start` e
`--end` prevalgono sul JSON. Date senza offset sono UTC; timestamp con offset
vengono convertiti in UTC. Estremi allineati a tutti gli intervalli richiesti,
fine esclusiva. Sono ammessi simboli alfanumerici con quote USDT e solo 15m/1h.
Cambiare date per uno smoke test non cambia il protocollo M1 né i suoi split.

Fonte primaria unica: [Binance Public Data](https://github.com/binance/binance-public-data),
host `data.binance.vision`, percorso `data/spot/{monthly,daily}/klines`.
Si scaricano mesi interi quando inclusi nella richiesta e giorni per i bordi.
Non vengono interrogati endpoint di trading né richieste credenziali.
Le candele 1h sono native; aggregazione 15m→1h non implementata.
Consultare le [condizioni del dataset](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md)
prima di un riuso o di una redistribuzione; questa consegna non redistribuisce dati.

## Incrementalità, ripresa e snapshot

- `raw/`: ZIP originali, sidecar `.CHECKSUM`, metadati di download UTC.
- I file presenti sono riutilizzati e il loro SHA-256 viene ricontrollato.
  Estendere il periodo scarica soltanto gli archivi assenti. Il Parquet viene
  ricostruito dai raw, non accodato: nessun doppio inserimento al riavvio.
- Download in `.part`; rilanciare lo stesso comando dopo un'interruzione.
  HTTP Range 206 richiede Content-Range coerente; 200 riscrive dall'inizio,
  416 scarta il solo frammento e ricomincia. Il checksum controlla il file finale.
  Non sono previsti retry automatici, scheduler o download concorrenti.
- Checksum ufficiale richiesto di default. Solo un 404 del sidecar (o assenza
  in modalità offline) permette `--allow-missing-checksum`, eccezione esplicita
  registrata come `unavailable/unverified`. Timeout, 403 e altri errori bloccano.
  Un hash discordante o un sidecar malformato bloccano sempre. Spostare il file
  sospetto dopo averlo esaminato, prima di riprovare.
- La cache rappresenta uno snapshot: i checksum già presenti non vengono
  aggiornati da remoto. Per verificare correzioni successive di Binance usare
  una nuova directory `--output`, preservando il manifest precedente.
- `.pipeline.lock` impedisce due writer sullo stesso output. Dopo un arresto
  forzato verificare che non esistano processi attivi prima di rimuovere il lock.

Non si aggirano restrizioni di rete. In questa sessione la connessione sandbox
è stata rifiutata (WinError 10061); il piccolo smoke è riuscito nell'ambiente
esterno esplicitamente autorizzato. Il periodo storico completo non è stato scaricato.

## Schema e validazione

Parquet v2.6 con Zstandard, colonne in ordine:

| Colonne | Tipo / unità |
| --- | --- |
| open_time, close_time | timestamp(us, UTC), chiusura inclusiva originale Binance |
| open, high, low, close | float64, USDT |
| volume | float64, asset base (BTC o SOL) |
| quote_volume | float64, USDT |
| symbol, interval, venue | string; venue=binance_spot |
| is_closed | bool, sempre true nelle righe conservate |

Schema non nullable. I decimali sorgente vengono convertiti esplicitamente in
IEEE-754 float64, con il suo arrotondamento; non è un ledger monetario esatto.
Gli ZIP conservano le stringhe originali. Campi trade count/taker/ignore non
entrano nello schema OHLCV. Versione sorgente e provenienza sono nel manifest.

Unità rilevata per riga mediante grandezza dell'intero, accettando solo ms/us
compatibili con lo storico Binance contemporaneo; secondi e nanosecondi rifiutati.
Open e close devono avere la stessa unità. Gli archivi spot passano a us dal 2025,
come documentato da Binance; non si applica una conversione unica all'intera serie.
Precisione della chiusura preservata: ultimo ms o ultimo us dell'intervallo.
Disponibilità della candela: `open_time + durata <= as_of`, non il solo close inclusivo.

Controlli: valori finiti, prezzi positivi, low ≤ open/close ≤ high, volumi base
e quote non negativi, allineamento UTC, durata esatta, candela completa entro
fine richiesta e istante del run. Righe CSV malformate escluse con linea e motivo.
Righe esterne alla richiesta filtrate e auditate. Duplicati identici deduplicati;
duplicati discordanti esclusi tutti a quel timestamp e serie rifiutata.
Ordinamento corretto con conteggio delle inversioni. Gap iniziali, interni e finali
registrati in intervalli `[start,end)`; nessun riempimento/interpolazione.

Solo una serie completa senza righe invalide né conflitti ottiene `validated`
in `normalized/`. Altrimenti il Parquet pulito parziale va in `quarantine/` con
stato `rejected`: non costituisce un dataset ammesso al benchmark. I futuri
consumatori devono richiedere manifest e serie `validated` e verificare gli hash.
Le esclusioni di finestre previsionali appartengono alla successiva attività M1;
questa pipeline registra righe e gap, senza costruire finestre né aprire il holdout
per selezione di modelli.

## Manifest e codici di uscita

`manifest.json` descrive l'ultimo tentativo; `manifests/<sha256-del-manifest>.json`
conserva ogni esito distinto, anche fallito. File JSON e Parquet scritti tramite
file temporanei e sostituzione atomica. Il manifest è l'indice autorevole: vecchi
Parquet possono rimanere dopo un tentativo fallito e non vanno consumati per nome.

Include configurazione, UTC/as_of, versione dati/schema, commit e stato dirty,
hash del modulo pipeline, Python/PyArrow/OS, URL, download UTC (null se cache
importata senza metadati), hash ufficiali/locali, unità originali, righe per fonte,
anomalie, gap, conflitti, esclusioni e hash Parquet. Le date degli archivi sono
identificate dagli URL; periodo richiesto e copertura effettiva sono separati.
Il checksum canonico usa ordine cronologico, interi us e `float.hex()` per le
sei colonne numeriche, separate da virgola e newline ASCII. Simbolo e intervallo
sono associati dal manifest. L'hash Parquet misura anche l'encoding; quello
canonico consente confronti indipendenti dai metadati del writer.

Uscita 0: tutte le serie validate; 2: anomalie/quarantena; 1: download, checksum,
configurazione o I/O falliti. Un errore di configurazione o lock precedente
all'avvio non sovrascrive il manifest. ZIP e checksum originali rimangono in cache.
Archivi assenti (404) bloccano, senza fallback silenzioso o modifica del periodo.

Dati e manifest runtime sotto `data/` sono ignorati da Git; `.parquet` è ignorato
anche altrove. Per congelare uno snapshot copiare il solo manifest approvato in
`reports/`, senza aggiungere ZIP, dataset o pesi. Il report della consegna è in
[reports/m1-data-pipeline.md](../../reports/m1-data-pipeline.md).
