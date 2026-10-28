# Roadmap e criteri di accettazione

Versione 0.1 · 28 ottobre 2026. Le milestone originali del master brief sono riordinate per inserire **prima** la validazione Timestral richiesta. Nessun gate risulta superato solo perché è descritto qui.

## M0 — Repository e documentazione (fase corrente)

Consegna: README, PRD, architettura, istruzioni agenti, wiki tecnica/funzionale, piano M1 e directory descrittive.

Accettazione:

- [ ] File pubblicati solo sul repository ufficiale, con SHA e link ai commit verificati.
- [ ] README/.gitignore iniziali presenti; niente codice del bot, segreti o dati pesanti.
- [ ] Link Markdown e coerenza PRD/roadmap/wiki controllati.
- [ ] Stefano aggiorna il checkout Windows e apre la stessa cartella in Codex.
- [ ] Work e Codex leggono lo stesso commit; eventuali modifiche locali preservate.
- [ ] Stefano revisiona i documenti e autorizza la successiva attività tecnica.

## M1 — Validazione offline Timestral (prima milestone tecnica)

Ambito: OHLCV storici BTC/USDT e SOL/USDT spot; 15m/1h; Timestral e baseline; protocollo cronologico, holdout e misure hardware. Nessun trading automatico o simulazione di portafoglio.

Accettazione:

- [ ] Verifica fonti ufficiali, licenze codice/pesi, revisioni e compatibilità Windows; versioni fissate.
- [ ] Smoke test reale di inferenza riproducibile, oppure incompatibilità documentata con evidenze.
- [ ] Manifest dati con URL, checksum, periodo, timestamp, controlli qualità e politica gap.
- [ ] Split/orizzonti/contesti/metriche e budget congelati prima del holdout.
- [ ] Baseline persistenza, drift e media rendimenti valutate alle stesse origini di Timestral.
- [ ] Test automatici contro look-ahead, trasformazioni fitted sul test, overlap dei target fra split e unità timestamp errate.
- [ ] Report per asset/timeframe/orizzonte, confronto appaiato, intervalli di incertezza e calibrazione quantili.
- [ ] Misure RAM, p50/p95 latenza, warm/cold, throughput e hardware registrate.
- [ ] Manifest del run, comando riproducibile e sintesi versionata; dati e pesi esclusi da Git.
- [ ] Limite di possibile contaminazione del pretraining e piano prospettico esplicitati.
- [ ] Decisione documentata: adottare, tenere sperimentale, restare su baseline o bloccare integrazione.

**Completare l'esperimento non richiede che Timestral vinca.** I criteri di adozione sono nel [protocollo](docs/wiki/timestral-validation.md). La validazione previsionale non dimostra un vantaggio di trading.

## M2 — Fondamenta e MVP spot paper

Dipendenze: M0 approvata, report M1 e decisione sul modello. Baseline utilizzabile se Timestral non è idoneo.

Consegna: servizio dati pubblici, Strategy minima, Risk Manager, simulatore spot, persistenza/audit, dashboard reale collegata, setup Windows e predisposizione Docker.

Accettazione:

- [ ] Percorso dati → previsione → segnale → rischio → fill virtuale → persistenza → dashboard dimostrato end-to-end.
- [ ] Zero percorsi di invio ordini reali e nessuna chiave trading.
- [ ] Una posizione, stop obbligatorio, sizing con costi, limite giornaliero e validatori configurazioni testati.
- [ ] Commissioni, spread e slippage contabilizzati e riconciliati.
- [ ] Dati invalidi/scaduti e disconnessioni bloccano ingressi; kill con uscita pendente esplicita.
- [ ] Duplicati, riavvio, rollback e riconciliazione coperti da test.
- [ ] EUR/USDT/FX definiti; nessuna conversione implicita.
- [ ] Dashboard PAPER, HOLD motivato, equity/P&L/drawdown e controlli funzionanti.
- [ ] Avvio Windows e build container documentati e verificati; niente deployment pubblico.

## M3 — Scanner e integrazione del modello validato

Consegna: universo dinamico con ranking, filtri, audit ed eventuale adapter Timestral nel percorso paper.

Accettazione:

- [ ] Selezione tracciabile per liquidità, spread, volatilità e volumi; esclusioni e qualità esplicite.
- [ ] Nessun filtro alimentato da dati futuri; universo storico senza survivorship bias per i test.
- [ ] Una posizione massima rispettata; aggiornamenti scanner non aggirano Risk Manager.
- [ ] Confronto modello/baseline su dati equivalenti; versione e incertezza visibili.
- [ ] Nessun uso operativo di Timestral senza decisione di gate M1.

## M4 — Strategie, backtesting e walk-forward

Consegna: intraday 15m/1h e scalping 1m/5m sperimentale; benchmark economici distinti dai benchmark previsionali.

Accettazione:

- [ ] Decisioni e fill causali: niente acquisti retroattivi al close già usato dal modello.
- [ ] Dati di sviluppo e validazione separati; costi, latenza, gap e spread stressati.
- [ ] Walk-forward riproducibile e confronto netto con cash/no-trade e buy-and-hold con ipotesi comparabili.
- [ ] P&L, drawdown, turnover, esposizione e numero trade con incertezza e limiti campionari.
- [ ] Confronto intraday/scalping e Timestral/baseline; risultati negativi conservati.

## M5 — Futures esclusivamente simulati

Consegna: long/short, leva configurabile ordinaria fino a 5x, margine, funding e liquidazioni virtuali.

Accettazione:

- [ ] Ledger futures separato dal saldo spot; formule e fonte di mark/funding documentate.
- [ ] Test su margine iniziale/mantenimento, funding positivo/negativo, gap e liquidazione.
- [ ] Nessun saldo creato da errori di segno o leva; limiti e stress test verificati.
- [ ] UI indica chiaramente futures e leva simulati; nessuna leva reale.

## M6 — Paper trading autonomo continuativo

Consegna: runtime 24/7, monitoraggio, alert e gestione operativa.

Accettazione:

- [ ] Soak test continuo proposto di 7 giorni con log e metriche, senza denaro reale.
- [ ] Errori rete, timeout, dati corrotti e riavvii iniettati e gestiti.
- [ ] Riconciliazione senza duplicati, uscite pendenti osservabili e ripresa controllata.
- [ ] Notifiche testate solo verso destinazioni autorizzate; stato e salute spiegabili.

## M7 — Deployment VPS

Consegna: container, accesso sicuro, volumi, backup/restore, monitoraggio e guida operativa.

Accettazione:

- [ ] Dimensionamento basato su misure M1/M6, non sulla sola dimensione dei pesi.
- [ ] Dashboard protetta, TLS/accesso privato e segreti fuori da Git.
- [ ] Restore provato su ambiente pulito; persistenza e log rotanti verificati.
- [ ] Deploy e rollback riproducibili; un solo writer per run e kill switch raggiungibile.

L'operatività reale non appartiene a questa roadmap: richiederebbe requisiti e autorizzazione separati. Multi-posizione e rischio di correlazione restano sviluppi futuri oltre il limite iniziale di una posizione.
