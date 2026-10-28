# Timestral Crypto Lab — PRD

Versione 0.1 · 28 ottobre 2026 · Stato: specifica iniziale da revisionare.

## 1. Origine e obiettivo

Fonte: Master Brief per Work fornito da Stefano, integrato dalle istruzioni successive: unico repository GitHub, documentazione prima dell'applicazione e validazione Timestral su BTC/USDT e SOL/USDT come prima milestone tecnica.

Realizzare un laboratorio capace di dimostrare o smentire, con misure riproducibili, l'utilità di previsioni AI e strategie crypto. Il prodotto futuro analizzerà mercati, selezionerà opportunità e opererà autonomamente entro limiti configurati, inizialmente solo con capitale virtuale.

L'utente conosce lo sviluppo software ma ha esperienza di trading limitata: dashboard e wiki devono spiegare decisioni, unità e rischi senza suggerire certezza.

## 2. Perimetro corrente e non obiettivi

**Consegna corrente:** documenti, struttura Git, piano offline M1 e sincronizzazione. Nessun trading automatico, benchmark eseguito o componente applicativo incluso.

**Prima milestone tecnica M1:** installabilità e inferenza Timestral, dati storici OHLCV BTC/USDT e SOL/USDT, benchmark cronologico con baseline, metriche previsionali e misure hardware. Nessun ordine, P&L o bot necessario.

**Prodotto successivo:** MVP spot paper, scanner, strategie/backtest, futures simulati, autonomia e VPS secondo roadmap.

Esclusioni: ordini reali, chiavi operative, trasferimenti di fondi, promessa di rendimento, massimizzazione del numero di trade, microservizi prematuri e app mobile nativa.

## 3. Decisioni confermate

- Sviluppo Windows; predisposizione per piccolo server cloud 24/7.
- Dashboard web responsive e comprensibile da smartphone.
- Market Scanner dinamico multi-asset, con selezione automatica delle opportunità.
- Timestral sostituibile; separazione tra Forecast, Strategy, Risk ed Execution.
- Risk Manager indipendente con autorità di veto; autonomia entro parametri utente.
- HOLD e nessuna operazione se non esiste un'opportunità valida.
- Audit di decisioni, motivazioni, ordini virtuali, anomalie e stato dei servizi.
- Kill switch, blocchi automatici, persistenza e riconciliazione.
- Backtest e paper trading precedono qualsiasi futura valutazione del reale.
- Prima versione solo PAPER: nessun ordine reale eseguibile e nessuna chiave di trading necessaria.

## 4. Requisiti funzionali

| ID | Requisito | Milestone |
| --- | --- | --- |
| F01 | Ingestione storica OHLCV BTC/USDT e SOL/USDT con provenienza e qualità verificabili | M1 |
| F02 | Interfaccia comune di previsione; Timestral e baseline statistiche comparabili | M1 |
| F03 | Benchmark cronologico, split fissati, holdout, metriche per asset/timeframe/orizzonte | M1 |
| F04 | Registrare dipendenze, licenze, hardware, latenza, RAM e limiti del modello | M1 |
| F05 | Servizio dati recenti/reali pubblici; validare e persistere candele/quote | M2 |
| F06 | Strategy indipendente con BUY/SELL/HOLD e ragioni leggibili | M2 |
| F07 | Risk Manager con veto, sizing, esposizione, stop, perdita giornaliera e blocchi | M2 |
| F08 | Simulatore spot, una posizione, saldo/ordini/costi coerenti e persistenti | M2 |
| F09 | Dashboard minima collegata al simulatore, PAPER permanente e controlli | M2 |
| F10 | Scanner dinamico: volatilità, spread, liquidità, volumi e filtri sicurezza | M3 |
| F11 | Confronto operativo Timestral/baseline dopo gate di validazione | M3–M4 |
| F12 | Intraday e scalping, backtest causali e walk-forward con costi realistici | M4 |
| F13 | Futures solo simulati, long/short, leva, margine, funding e liquidazioni | M5 |
| F14 | Paper continuativo, monitoraggio, alert, riavvii e riconciliazione | M6 |
| F15 | Containerizzazione, sicurezza, backup e deployment VPS | M7 |

## 5. Requisiti non funzionali

| ID | Requisito |
| --- | --- |
| N01 | Nessun percorso di esecuzione reale; nessuna credenziale finanziaria |
| N02 | Confini modulari, modelli sostituibili e contratti testabili |
| N03 | Nuovi ingressi bloccati con dati mancanti, scaduti o incoerenti |
| N04 | Stato persistente, operazioni atomiche e idempotenza degli ordini simulati |
| N05 | Riavvio prudente e guasti/disconnessioni espliciti; no ripresa silenziosa |
| N06 | Test automatici su rischio, esecuzione, dati, causalità e persistenza |
| N07 | Costi espliciti, risultati netti e assunzioni documentate |
| N08 | Zero look-ahead; fitting e selezione esclusivamente nel passato consentito |
| N09 | UX responsive, accessibile e comprensibile; dati sintetici distinti dai reali |
| N10 | Setup Windows riproducibile; dipendenze/versioni e futuro Docker verificabili |
| N11 | UTC e valute/unità esplicite; USDT non equiparato automaticamente a EUR |
| N12 | Risultati negativi e nessun vantaggio sono esiti validi del laboratorio |

## 6. Esperimento M1

Due asset obbligatori: BTC/USDT e SOL/USDT spot. Timeframe primari 15m e 1h; scalping 1m/5m rimandato a M4. Baseline: persistenza, drift e media dei log-rendimenti storici. Target primario: log-prezzo di chiusura; metrica primaria e orizzonti fissati nel protocollo. OHLCV disponibile solo fino all'origine della previsione.

Split cronologici comuni, tuning sulla validazione, holdout finale sigillato. Confronti appaiati alle stesse origini, incertezza statistica e dipendenza temporale considerate. La qualità previsionale non dimostra redditività. Il dettaglio riproducibile è nel [piano M1](docs/wiki/timestral-validation.md).

## 7. Parametri sperimentali del prodotto futuro

| Parametro | Proposta iniziale | Qualifica |
| --- | --- | --- |
| Capitale virtuale | 1.000 EUR | Configurabile; decidere FX per mercati USDT prima di simulare un portafoglio |
| Rischio teorico per trade | 0,5% | Costi inclusi; non limite garantito con gap |
| Perdita giornaliera | 2% | Equity netta e giornata UTC proposte; definizione da ratificare M2 |
| Posizioni simultanee | 1 | Rischio aggregato e correlazioni prima dell'espansione |
| Stop-loss | Obbligatorio | Prezzo d'uscita non garantito |
| Asset candidati | BTC, ETH, SOL, DOGE, PEPE | Disponibilità delle coppie e liquidità da validare |
| Intraday | 15m e 1h | Strategia principale candidata |
| Scalping | 1m e 5m | Sperimentale, confronto netto con intraday |
| Mercati | Spot e futures simulati | Futures solo M5 |
| Leva futures ordinaria | Fino a 5x | Solo simulata; M1 non usa leva né capitale |

Nessun parametro costituisce un risultato validato. Validatori e audit delle modifiche sono obbligatori. Capitale e ipotesi che rendono incomparabili i risultati richiedono un nuovo run; modifiche durante posizioni aperte vanno limitate e versionate.

## 8. Dashboard del prodotto futuro

PAPER permanente; portafoglio virtuale; equity, P&L, drawdown; scanner; previsioni e incertezza; posizioni aperte e storico; BUY/SELL/HOLD motivati; confronto intraday/scalping e Timestral/baseline; limiti; stato del bot, stop immediato e anomalie.

Solo funzioni effettive: moduli non implementati indicati come tali, nessun risultato inventato. Glossario e motivazioni semplici, con dettagli tecnici espandibili. Accesso smartphone remoto richiede autenticazione e rete sicura, non solo un layout responsive.

## 9. Successo e gate

M1 è completata con report riproducibile, anche quando Timestral non supera le baseline o risulta non idoneo all'hardware. La sua adozione richiede un gate distinto, non una dichiarazione automatica di successo.

Le milestone successive richiedono codice funzionante e test significativi. Non iniziarle per riempire una dashboard. Criteri in [ROADMAP.md](ROADMAP.md), tracciabilità nella [wiki](docs/wiki/traceability.md).

## 10. Questioni aperte

Date e fonte dati proposte da confermare prima del download; contaminazione da pretraining non escludibile senza evidenze; compatibilità Windows e costo VPS da misurare; coppia/FX e commissioni del futuro MVP da decidere; policy di ripresa e uscite pendenti da testare M2. Nessun punto richiede credenziali di trading.
