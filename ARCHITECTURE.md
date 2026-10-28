# Architettura

Versione 0.1 · Stato: progetto da validare, non implementazione.

## Impostazione

Applicazione modulare inizialmente in un processo, con responsabilità e contratti separati. Non un monolite di logica mescolata, né una rete di microservizi prematura. Un writer dello stato e un orchestratore; dashboard e strategia non possono aggirare il Risk Manager.

La M1 è un harness offline isolato dal futuro runtime paper. Condivide i contratti di dati/previsioni, non contiene esecuzione ordini.

## Stack candidato

| Area | Proposta | Motivazione / verifica |
| --- | --- | --- |
| Ricerca e runtime | Python 3.12 | Windows/Linux; compatibilità effettiva da provare M1 |
| Numerica/modello | NumPy, PyTorch e adapter ufficiale Timestral | Revisioni fissate; licenze e RAM/latency misurate |
| Test | pytest | Fixture deterministiche; rete solo nei test separati |
| Persistenza MVP | SQLite, migrazioni e transazioni | Un writer, filesystem locale, sufficiente per un bot |
| API e UI future | FastAPI/Uvicorn + HTML/CSS/JavaScript | Validazione API, dashboard responsive senza build complessa |
| Packaging | pyproject e lock delle dipendenze | Da creare con l'ambiente reale, nessun lock fittizio |
| VPS futuro | Docker, volume locale persistente | Packaging dopo slice M2; hardening e deployment M7 |

Queste scelte sono proposte, non requisiti già approvati. Non sono installate da questa consegna.

## Moduli

| Modulo | Responsabilità | Prima fase |
| --- | --- | --- |
| Market Data | Storico/realtime, qualità, timestamp, simboli e persistenza | storico M1, runtime M2 |
| Forecast | Baseline/Timestral dietro interfaccia comune; nessun segnale operativo implicito | M1 |
| Validation/Benchmarks | Split, origini rolling, metriche, risorse, manifest e report | M1 |
| Strategy | Dati disponibili e forecast → BUY/SELL/HOLD motivato | M2 |
| Risk Manager | Veto, sizing, stop, costi, esposizione, limiti e blocchi | M2 |
| Execution | Solo fill virtuali, ledger spot e riconciliazione | M2 |
| Market Scanner | Ranking dinamico e filtri liquidità/spread/volatilità/volume | M3 |
| Backtesting | Clock storico, ordini causali, strategie e costi | M4 |
| Futures Simulator | Long/short, leva, margine, funding e liquidazioni | M5 |
| Paper Orchestrator | Evoluzione run, idempotenza, ripartenza | slice M2, 24/7 M6 |
| Dashboard | Stato, spiegazioni, configurazione e kill switch | M2 |
| Audit & Monitoring | Eventi, salute, alert e riconciliazione | base M2, completo M6 |

## Contratti dati proposti

- Candle: venue, symbol, interval, open/close_time UTC, OHLCV, quote_volume se presente, is_closed, source_version.
- DatasetManifest: URL/file, checksum, unità timestamp originale, periodo, righe, gap/esclusioni, trasformazioni e hash normalizzato.
- ForecastRequest: origine, contesto solo passato, target, orizzonti, feature/versioni.
- Forecast: model/revision, context_end, target, point/quantiles, unità, horizon e note sulla calibrazione.
- BenchmarkResult: run_id, split, asset/timeframe, origini, loss, confronto appaiato, seed, hardware e software.
- Signal futuro: id, run, timestamp, asset, BUY/SELL/HOLD, motivi e forecast_ref.
- RiskDecision futura: signal_ref, config_version, approvazione/veto, quantità massima, stop, budget e reason_codes.
- VirtualOrder/Fill/Position: chiave idempotenza, quantità, lato, prezzo, costi, valuta, stato e riferimenti.

Nessuna previsione ha accesso a future OHLCV osservate. I contratti richiederanno validatori, versionamento e test prima dell'uso.

## Percorso M1

Snapshot dati → validazione qualità → finestre cronologiche → Forecast adapter o baseline → metriche alle stesse origini → report e decisione. Nessun clock live, conto o ordine.

## Percorso futuro di un ingresso

Dati validati → Strategy propone → Risk verifica dati/stato/limiti/costi e concede o nega → Execution verifica approvazione e idempotenza → commit atomico di saldo/fill/audit → dashboard.

Stop e chiusure di riduzione del rischio seguono una policy dedicata: un veto agli ingressi non deve impedire le uscite. Nessun nuovo ordine con dati scaduti o stato fermo.

## Persistenza futura

Run, configurazioni versionate, dati, forecast, segnali, decisioni rischio, ordini/fill, posizioni, equity, audit e migrazioni. Chiavi univoche per evitare duplicati; stato e contabilizzazione nella stessa transazione.

Un'unica istanza writer per run. Rifiutare o coordinare una seconda istanza: nessun multi-worker aggiunto senza progettazione. SQLite su disco locale, mai su cartella di rete. Backup coerenti con API SQLite o procedura a processo fermo; includere correttamente il WAL.

## Stati e guasti futuri

Proposti: PAUSED, RUNNING, RISK_HALTED, KILLED, con salute dati e pending_exit indipendenti. Riavvio in pausa, posizioni conservate e riconciliate. Pausa blocca ingressi, preserva monitoraggio uscite. Kill blocca subito nuovi ingressi e richiede chiusura virtuale alla prima quotazione valida. Se i dati mancano, nessun fill inventato: uscita pendente visibile. Ripresa manuale dopo verifica; reset giornaliero non deve cancellare kill o anomalie.

## Sicurezza e valuta

Nessun adapter di trading reale. Feed solo lettura pubblica; nessuna chiave operativa. Dashboard MVP su loopback, validazione server, difese CSRF/DNS rebinding; accesso remoto solo con autenticazione e canale sicuro in M7.

M1 valuta previsioni in USDT e rendimenti adimensionali; non usa il capitale EUR. Il futuro ledger deve esplicitare FX o usare un capitale virtuale in valuta quote con nuovo run: EUR e USDT non sono intercambiabili.

## Integrazione Timestral

Verifica documentale preliminare in [fonti](docs/wiki/sources.md), ma inferenza e benchmark Windows non ancora eseguiti. Il modello foundation non è una strategia. Nessun quantile è una probabilità di guadagno. Gate e piano risorse in [validazione M1](docs/wiki/timestral-validation.md).
