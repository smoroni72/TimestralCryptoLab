# Rischio ed esecuzione simulata

Stato: specifica futura M2/M5; nessun motore implementato.

## Confini

Forecast produce previsioni, Strategy propone segnali, Risk Manager concede o nega, Execution contabilizza soltanto fill virtuali. Il Risk Manager può bloccare qualsiasi nuova esposizione. Una strategia o comando UI non può ordinare direttamente un acquisto aggirando il controllo.

## Sizing proposto

Budget teorico = equity di riferimento × rischio per trade. La perdita per unità deve includere distanza ingresso-stop, commissioni di apertura/chiusura e slippage previsto. Quantità = minimo fra budget/perdita unitaria, liquidità disponibile e limiti di esposizione; arrotondamento verso il basso secondo i vincoli simulati della coppia.

Default candidati: capitale virtuale 1.000 EUR, rischio 0,5%, perdita giornaliera 2%, una posizione, stop obbligatorio. Definire FX prima di tradare coppie USDT; nessuna conversione implicita. Il budget non garantisce una perdita massima in presenza di gap o guasto.

## Limite giornaliero proposto

Giornata UTC; riferimento equity netta osservata al cambio giornata, con costi stimati di liquidazione. Confrontare equity corrente comprensiva del non realizzato, non solo trade chiusi. Formalizzare come gestire assenza dati a mezzanotte e posizioni overnight senza cancellare perdite durante un gap.

Al superamento, bloccare nuovi ingressi e applicare una policy di chiusura/riduzione testata. Persistenza del blocco: un riavvio o cambio configurazione non lo cancella. Cambio giornata non riattiva automaticamente un kill switch o un guasto dati. Policy finale e casi limite vanno fissati prima del codice M2.

## Esecuzione spot M2

Long spot, senza leva, una posizione. Prezzi bid/ask quando disponibili; fee per lato e slippage configurabili; minimi, precisione e saldi controllati. Ordini/fill/saldo/audit atomici; chiavi idempotenti; nessun ordine duplicato dopo retry o riavvio.

La simulazione con sole OHLCV richiede regole conservative: non conoscere la sequenza high/low, non acquistare al close già utilizzato per decidere e non assumere uno stop eseguito esattamente al livello. Non presentarla come replica esatta di un exchange.

## Arresto e guasti

Pausa: vieta ingressi, conserva controlli di uscita. Kill: vieta subito ingressi, richiede chiusura virtuale appena esiste una quotazione valida. Assenza dati: pendente visibile, nessun fill a un prezzo vecchio presentato come attuale. Conservare stato e posizioni al riavvio; verificare riconciliazione prima della ripresa manuale.

## Futures M5

Ledger separato per long/short, margine iniziale/mantenimento, leva ordinaria candidata fino a 5x, mark price, funding, liquidazioni e costi. Testare segni, collateral, perdite e gap. Nessuna leva o esecuzione reale. Multi-posizione e correlazioni richiedono ulteriori limiti di rischio aggregato prima di essere abilitate.
