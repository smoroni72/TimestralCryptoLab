# Piano test e verifica

Stato: piano, nessun test applicativo presente o eseguito nel repository.

## Documentazione M0

Verificare esistenza dei documenti richiesti, link Markdown locali, assenza di codice del bot/segreti, stato dichiarato e coerenza fra PRD, architettura, roadmap e wiki. Verificare SHA del branch remoto dopo la pubblicazione. La sincronizzazione Windows/Codex richiede un controllo dal PC, non può essere dedotta da un push Work.

## Benchmark M1

| Livello | Casi significativi |
| --- | --- |
| Parser | Timestamp ms/us, cambio unità 2025, ordinamento, duplicati concordanti/discordanti |
| Qualità | NaN/infinito, prezzi non positivi, OHLC impossibili, volumi negativi, candele aperte |
| Aggregazione | Quattro 15m complete → 1h; niente aggregazione parziale o intervallo traslato |
| Causalità | Cambiare dati futuri non cambia input/previsione passata; niente scaler fitted sul test |
| Split | Target non attraversano frontiere; contesto passato ammesso; holdout non usato per tuning |
| Baseline | Persistenza zero rendimento, drift e media rendimenti su fixture con soluzioni note |
| Modello | Shape/horizon/quantili, valori finiti, revisioni fissate; smoke test reale separato |
| Metriche | MAE/RMSE/pinball/copertura su vettori con risultati calcolati indipendentemente |
| Comparabilità | Stesse origini e maschere per modelli; niente eliminazione selettiva di errori sfavorevoli |
| Riproducibilità | Hash/config/seed e risultati entro tolleranze dichiarate |

Fixture piccole e deterministiche per la suite offline. Download/inferenza reale come integrazione separata, con tempi/errori registrati. I test non devono essere semplici copie delle formule implementate: usare casi limite e risultati attesi indipendenti.

## Rischio/esecuzione M2

Testare rischio teorico con tutti i costi; veto per spread/dati/limiti/stato; saldi non negativi; una posizione; arrotondamento; stop oltrepassato con gap; P&L e equity riconciliati; perdita giornaliera inclusa componente non realizzata; cambio giorno e posizione overnight; configurazioni invalide.

Integrare kill con dati assenti, uscita pendente, pausa che mantiene le uscite, ripartenza prudente, ordini duplicati, rollback, restore e seconda istanza writer. End-to-end con dati controllati fino alla dashboard, senza endpoint reali di trading.

## Strategie/futures e operazioni future

Backtest: niente look-ahead o fill retroattivi, costi e timing stressati, universo storico corretto. Futures: margine/funding/liquidazione con casi indipendenti. Runtime: fault injection rete/clock/dati e soak test; deployment: backup/restore e rollback.

Ogni report di esecuzione deve indicare comando reale, ambiente, versione, risultato e limiti. Nessuna casella di accettazione va spuntata sulla base di un test soltanto pianificato.
