# Dati, qualità e unità

Stato: contratti e policy proposti, non codice implementato.

## Dataset M1

Spot BTCUSDT/SOLUSDT, 15m/1h, provenienza candidata archivi pubblici Binance. Conservare file originali immutabili fuori Git; manifest versionati con URL, SHA-256, data download, schema, unità temporali e intervallo UTC. Gli archivi possono essere corretti dalla fonte: usare checksum e snapshot per distinguere versioni.

Il parser deve riconoscere e convalidare unità temporali documentate, normalizzando UTC senza perdere precisione in modo silenzioso. Non confondere timestamp di apertura, chiusura e disponibilità del dato.

## Invarianti

Prezzi finiti/positivi; low ≤ open/close ≤ high; volume finito/non negativo; timestamp ordinati/univoci; intervalli contigui nelle finestre; nessuna candela parziale. Duplicati uguali deduplicabili con audit, duplicati discordanti bloccanti. Target mancanti mai interpolati. Esclusioni e righe eliminate fanno parte del report.

La canonicalizzazione deve definire tipi, ordine colonne e gestione decimali prima di calcolare l'hash normalizzato. Le fixture dei test devono attraversare il cambio di unità timestamp previsto dalla fonte.

## Dati runtime futuri

Quote bid/ask con exchange_time se fornito e received_at separato. Definire timeout/freschezza per fonte; confrontare clock locale/exchange. Non trasformare un timestamp di ricezione in prova che la quotazione sia aggiornata all'exchange. Mercato in manutenzione, spread anomalo o dati incoerenti bloccano ingressi.

OHLCV non contiene spread, profondità o sequenza intrabar. Non ricostruire fill realistici dalle sole candele senza ipotesi dichiarate. Funding/mark price futures richiederanno dataset distinti.

## Valute

BTC/USDT e SOL/USDT sono target M1; gli errori in prezzo sono USDT. Le metriche su log-rendimenti sono adimensionali. Il capitale di 1.000 EUR riguarda il futuro simulatore: definire un feed FX e tempi di conversione oppure un run in valuta quote approvato, mai assumere 1 EUR = 1 USDT.
