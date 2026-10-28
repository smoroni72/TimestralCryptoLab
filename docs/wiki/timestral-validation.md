# M1 — Protocollo di validazione Timestral

Versione 0.1 · 28 ottobre 2026 · **Piano proposto, non eseguito.** Nessun risultato o comando di benchmark è già disponibile. Prima dell'esecuzione fissare configurazione e revisioni in un manifest versionato.

## 1. Domande e separazione dei gate

1. Tecnico: installazione e inferenza riproducibili su Windows/CPU? Quanto costano RAM e tempo?
2. Previsionale: Timestral migliora le baseline sugli stessi target e sulle stesse origini cronologiche?
3. Operativo futuro: l'eventuale miglioramento sopravvive a regole di strategia, costi e latenza? Questa domanda appartiene a M4, non a M1.

Risultati negativi completano correttamente l'esperimento. Non usare P&L o numero di trade come metrica di questa fase.

## 2. Dataset e periodo proposti

Fonte candidata: archivi pubblici **spot Binance**, non futures. Simboli BTCUSDT e SOLUSDT, presentati come BTC/USDT e SOL/USDT. Verificare accessibilità, condizioni d'uso, completezza e checksum prima di congelare il dataset; nessuna chiave trading.

| Asse | Proposta da congelare prima del run |
| --- | --- |
| Periodo complessivo | 2023-01-01 00:00 UTC ≤ tempo < 2026-10-01 00:00 UTC |
| Sviluppo | 2023-01-01 ≤ tempo < 2024-07-01 |
| Validazione/selezione | 2024-07-01 ≤ tempo < 2025-07-01 |
| Holdout finale | 2025-07-01 ≤ tempo < 2026-10-01 |
| Timeframe | 15 minuti e 1 ora |
| Origini | Ogni ora UTC; candele di contesto già chiuse a quell'istante |
| Orizzonti | h=1 e h=4 candele per entrambi i timeframe |
| Contesto primario | 256 candele chiuse; 1.024 come ablation opzionale selezionata solo su validazione |

Date comuni per entrambi gli asset. Se la fonte non soddisfa queste finestre, registrare la modifica **prima** di analizzare il test. Scegliere finestre che contengano regimi diversi senza selezionarle in base alla performance del modello.

Gli originari timeframe scalping 1m/5m restano M4. OHLCV va acquisito per intero e validato; il primo confronto è univariato sul close per isolare il contributo del modello. Successive ablation possono usare solo covariate OHLCV passate.

## 3. Qualità e normalizzazione dei dati

URL, download UTC, SHA-256 dell'archivio e del dataset normalizzato, unità timestamp originale e righe per asset/timeframe. Convertire esplicitamente millisecondi/microsecondi in UTC: non presumere una sola unità per l'intero storico. Le fonti indicano microsecondi per gli archivi spot dal 2025; verificare i file effettivi.

Richiedere valori finiti, prezzi positivi, volume non negativo, low ≤ open/close ≤ high, timestamp univoci e ordinati, intervalli coerenti e sole candele chiuse. Non riempire artificialmente un target mancante. Escludere finestre con gap secondo policy fissata e riportare il numero di esclusioni. La disponibilità di NaN nel modello non sostituisce i controlli qualità.

Per 1h scegliere e fissare una sola fonte: candele native oppure aggregazione di quattro 15m contigue. Se aggregazione: open primo, high massimo, low minimo, close ultimo, volume somma; vietati gruppi incompleti. Se fonti native, usare l'aggregato solo come controllo diagnostico e documentare differenze.

## 4. Modelli e target

Target principale: `x_t = log(close_t)`. Forecast a h passi convertito in rendimento logaritmico `r_hat(t,h) = x_hat(t+h) - x_t`; target reale `r(t,h) = log(close_(t+h)/close_t)`.

| Modello | Previsione / regola |
| --- | --- |
| Persistenza / random walk | x_hat(t+h)=x_t; rendimento previsto zero |
| Random walk con drift | x_t + h * (x_t-x_(t-L+1))/(L-1), stesso contesto L |
| Media rendimenti | x_t + h * media degli ultimi 32 log-rendimenti disponibili |
| Timestral-5M | Candidato primario CPU, stesso contesto e orizzonte; revisioni codice/pesi fissate |
| Timestral-28M | Esplorativo opzionale entro budget; decisione prima di aprire il test |

La scelta 5M è una proposta di economia sperimentale, non una superiorità già misurata. Non scaricare tutte le taglie per default. Se si modifica il target o si confrontano i prezzi invece dei log-prezzi, dichiarare la variante separata e non selezionarla sul test.

Timestral: inferenza zero-shot iniziale, nessun fine-tuning. OHLCV futuro non è una covariata nota. Eventuali indicatori, scaler e trasformazioni si calcolano solo sul passato; parametri fitted soltanto sullo split consentito.

## 5. Split e causalità

A ogni origine t, contesto terminato non oltre t e target in (t,t+h]. Tutti i target di una finestra devono ricadere nello stesso split valutato. Eliminare le origini i cui target attraversano una frontiera; la durata del purge dipende dal massimo h effettivamente usato. È lecito usare storia precedente alla frontiera come contesto, perché era già osservabile.

Niente shuffle o cross-validation casuale. Valutazione rolling-origin, con gli stessi timestamp e maschere di qualità per tutti i modelli. Tuning/ablation sullo sviluppo e sulla validazione; scelta e metrica primaria congelate prima di un singolo passaggio finale sul holdout. Ogni riuso successivo rende quel test esplorativo e richiede un nuovo holdout.

Tenere anche un riepilogo mensile o trimestrale cronologico per osservare instabilità, senza scegliere retroattivamente i periodi migliori. Un run deve poter essere ripetuto dai manifest, incluse origini scartate e ragioni.

## 6. Metriche e confronti

Metrica primaria: MAE del rendimento logaritmico, espressa in basis point (`10.000 * mean(abs(r_hat-r))`). Celle primarie: 15m/h4 e 1h/h1, su ciascuno dei due asset, cioè **quattro celle**. Tutti gli altri orizzonti sono secondari.

Secondarie: RMSE dei rendimenti, errore sul prezzo per asset, accuratezza direzionale con trattamento dei rendimenti nulli dichiarato, bias e numero di origini valide. Evitare medie di errori in USDT fra asset con scale diverse; riportare le quattro celle separatamente e media macro delle MAE relative.

Per Timestral: pinball loss sui quantili disponibili, copertura/intervallo 80% e 90%, ampiezza media e copertura per orizzonte. Le baseline puntuali non forniscono intervalli calibrati: non inventarli; se aggiunti tramite residui passati, descrivere una variante separata.

Confronto appaiato: differenza di loss alle stesse origini contro ogni baseline. Selezionare la baseline di riferimento tramite validazione, poi mantenerla fissa. Intervalli al 95% tramite moving-block bootstrap (proposta: blocchi di 24 origini orarie, 2.000 repliche, seed 42), con analisi di sensibilità 12/48 solo esplorativa. Non trattare le finestre sovrapposte come indipendenti. Correggere i confronti primari multipli o presentare chiaramente l'incertezza senza attribuire significatività globale a un solo risultato.

## 7. Contaminazione e limite fuori campione

Gli split sono fuori campione rispetto a fitting e selezione del progetto. **Non dimostrano** che BTC/SOL nel periodo fossero esclusi dal pretraining Timestral. Registrare data/revisione del modello e informazioni pubbliche sulla composizione dei dati; non dichiarare assenza di contaminazione se non verificabile.

Prevedere una validazione prospettica, dopo il congelamento effettivo del protocollo, su almeno 30 giorni proposti di nuove candele archiviate senza riottimizzare. È un controllo offline differito, non un bot autonomo né un'automazione già attivata. Se i risultati retrospettivi sono promettenti, l'adozione rimane sperimentale finché questo controllo non è adeguato.

## 8. Risorse e riproducibilità

Manifest: commit progetto, revisioni Timestral e pesi, checksum, versioni Python/torch/numpy, OS, CPU/core/thread, RAM, GPU eventuale, precisione, batch, L, h, seed, metriche e intervalli temporali.

Misurare separatamente download, caricamento cold, warm-up e inferenza warm; almeno 100 inferenze rappresentative per p50/p95, picco RAM del processo e throughput. Stesso device e batch per i confronti di costo. Nessuna equivalenza fra dimensione file e RAM richiesta.

Budget CPU iniziale proposto: p95 ≤ 5 secondi per singola serie L=256/h≤4 e picco RAM ≤ 4 GiB, da ratificare rispetto al PC disponibile e registrare prima del run. Queste sono soglie operative candidate, non benchmark già raggiunti. Se non rispettate: taglia/contesto ridotti come nuova variante dichiarata, baseline o rinvio VPS; nessun occultamento dell'esito iniziale.

## 9. Gate finale

**Completamento M1:** dataset e protocollo verificati, esecuzioni/limitazioni documentate, report riproducibile e raccomandazione, anche negativa.

**Candidatura all'integrazione:** compatibilità/licenza accettabili; budget risorse rispettato; miglioramento macro proposto ≥ 2% rispetto alla baseline fissata sulle quattro celle primarie e nessuna cella peggiorata oltre il 5%. Riportare CI e stabilità; se il CI della differenza include zero, indicare evidenza inconcludente. Le soglie sono proposte da fissare prima del test, non regole per cercare una vittoria retrospettiva.

**Adozione operativa futura:** richiede anche evidenza prospettica e valutazione strategica/costi M4. Se Timestral non supera il gate, mantenere baseline o rivedere l'ipotesi. Un buon forecast da solo non autorizza trading automatico.

## 10. Deliverable attesi, ancora da sviluppare

Manifest dati/run e configurazione congelata; test di qualità/causalità; harness benchmark; risultati tabellari per cella; curve errore/calibrazione e risorse; report in `reports/`; ADR sulla decisione. Dataset/pesi grezzi restano fuori da Git. Non sono presenti comandi eseguibili fittizi in questa fase.
