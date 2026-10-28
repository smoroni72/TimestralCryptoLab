# Guida funzionale del prodotto futuro

Stato: specifica UX, nessuna schermata implementata.

## Cosa vedrà Stefano

PAPER sempre visibile, con capitale virtuale e sorgente dati distinti. La dashboard spiega prima cosa sta succedendo e perché, poi consente di aprire i dettagli quantitativi. Un modello che non individua opportunità sufficienti deve poter rimanere HOLD senza essere considerato guasto.

| Area | Informazioni e comportamento attesi |
| --- | --- |
| Panoramica | Equity virtuale, liquidità, P&L realizzato/non realizzato, costi e drawdown |
| Mercati | Coppie osservate, dati aggiornati, ranking, esclusioni e ragioni |
| Previsioni | Modello/versione, orizzonte, previsione e incertezza; confronto baseline |
| Decisioni | BUY/SELL/HOLD, dati usati e motivazione; distinto dal veto rischio |
| Posizioni | Quantità, prezzo medio, stop, esposizione e costi di chiusura stimati |
| Confronti | Intraday/scalping e Timestral/baseline su periodi e ipotesi coerenti |
| Rischio | Capitale, rischio per trade, perdita giornaliera, stop, leva simulata futura |
| Stato | Bot, salute dati/servizi, anomalia e chiusura pendente |
| Audit | Eventi, ordini virtuali, motivi e modifiche configurazione |

## Comandi proposti

Avvia dopo verifica dei dati; pausa blocca nuovi ingressi ma mantiene controlli sulle posizioni; arresto immediato blocca ingressi e richiede chiusura virtuale alla prima quotazione affidabile. Se non esistono dati validi, mostrare la chiusura come pendente, senza inventare un prezzo. Riavvio in pausa e ripresa manuale dopo riconciliazione.

Parametri validati lato server; spiegare unità e conseguenze prima di applicare modifiche. Configurazioni versionate e collegate a ciascun run. Cambi di capitale o valuta non devono alterare retroattivamente il rendimento di un esperimento.

## Glossario minimo

- Equity: liquidità più valore netto stimato delle posizioni.
- P&L: profitto o perdita; distinguere importi già realizzati da stime correnti.
- Drawdown: perdita rispetto al precedente massimo dell'equity.
- Spread: differenza tra prezzo di acquisto e vendita disponibili.
- Slippage: differenza fra prezzo atteso e prezzo simulato di esecuzione.
- Basis point (bp): 0,01%; 100 bp equivalgono a 1%.
- Quantile: soglia della distribuzione prevista; non probabilità certa di profitto.
- Paper: operazioni virtuali; dati reali non significano denaro reale.
- HOLD: decisione di non cambiare esposizione; può essere la scelta corretta.

## M1 e interfaccia

La validazione M1 richiede report, non una dashboard di trading. Mostrare risultati per asset, timeframe, orizzonte e baseline, con ipotesi e limiti. Accesso da smartphone nella futura app richiede layout responsive; l'accesso da fuori PC richiede anche autenticazione e infrastruttura sicura.
