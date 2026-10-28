# Istruzioni operative per Codex

## Ambito corrente

**Solo documentazione, struttura e piano di validazione. Non implementare ancora trading automatico.**

La prima milestone tecnica è M1: validazione Timestral offline su BTC/USDT e SOL/USDT. In questa consegna viene pianificata, non eseguita. Non creare bot, simulatori operativi, dashboard di facciata, scheduler, adapter di ordini o connessioni a conti. L'implementazione del benchmark richiede la successiva istruzione dell'utente dopo la verifica della sincronizzazione.

## Fonte e priorità

Le istruzioni esplicite dell'utente prevalgono. Leggere [PRD.md](PRD.md), [ARCHITECTURE.md](ARCHITECTURE.md), [ROADMAP.md](ROADMAP.md), [wiki](docs/wiki/README.md) e gli eventuali AGENTS.md più specifici prima di modificare file. Il master brief è la base; l'istruzione successiva sposta la validazione Timestral al primo posto e sospende lo sviluppo del bot.

Separare sempre: decisioni confermate, proposte, risultati osservati e ipotesi. Non dichiarare risultati previsionali, test Windows, deployment o sincronizzazione locale senza evidenze.

## Repository e collaborazione

- Usare unicamente `smoroni72/TimestralCryptoLab` e il suo checkout. Nessun repository alternativo o `.git` annidato.
- Directory ufficiale Windows: `C:\Users\smoro\Documents\Codex\TimestralCryptoLab`.
- Verificare ambiente, directory, branch, `git status`, istruzioni e remote prima di agire.
- Preservare modifiche dell'utente; niente reset distruttivi, clean indiscriminati o force push.
- Eseguire fetch prima di pubblicare; se il remote avanza, integrare senza sovrascrivere lavoro altrui.
- Documentazione, schema dei dati, test e stato vanno aggiornati nello stesso cambiamento del codice pertinente.
- Non inviare messaggi a terzi, creare automazioni o pubblicare servizi senza istruzioni.

## Sicurezza e rigore

Prima versione solo PAPER. Nessuna chiave con permessi di trading e nessun endpoint per inviare ordini reali, neppure nascosto dietro un flag. Forecast non invia ordini; Strategy propone; Risk Manager ha veto; Execution simula. Dati non affidabili bloccano ingressi. HOLD è valido.

Nella M1: niente P&L presentato come validazione del modello; misurare errori e calibrazione fuori campione. Usare solo dati disponibili a ogni origine temporale. Non effettuare shuffle, fitting sul test, uso di OHLCV futuri o selezione del modello sul holdout finale. Congelare protocollo e configurazione prima del test.

Le finestre cronologiche successive al training non dimostrano da sole assenza di contaminazione del pretraining di un modello foundation: documentare il limite e prevedere una verifica prospettica.

Nelle milestone future: rischio ed esecuzione con test significativi; costi, gap e slippage espliciti. Una sola posizione iniziale. Futures/leva soltanto simulati nella M5; nessuna promessa di redditività.

## Qualità e riproducibilità

- UTC per dati e log; distinguere EUR, USDT e altre quote.
- Manifest con URL, checksum, periodo, unità timestamp, versione dati e versione codice.
- Fissare revisioni di codice e pesi del modello; controllare licenze e versioni ufficiali.
- Test deterministici senza rete obbligatoria; smoke test reali separati e dichiarati.
- Registrare hardware, RAM, p50/p95 latenza, device, thread e condizioni warm/cold.
- Motivare ogni dipendenza. Non committare dati grezzi, pesi, segreti o database.

## Chiusura del lavoro

Riportare file modificati, verifiche effettive, limitazioni e commit pubblicati. Se il push fallisce, distinguere commit locale da commit remoto. In questa fase non esistono test applicativi: verificare Markdown, link e coerenza dei documenti senza inventare esecuzioni del bot.
