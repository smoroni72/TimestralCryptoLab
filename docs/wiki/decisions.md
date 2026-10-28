# Registro delle decisioni architetturali

28 ottobre 2026. Le decisioni confermate derivano dal brief/istruzioni di Stefano; le proposte attendono validazione.

| ID | Decisione | Stato | Conseguenza |
| --- | --- | --- | --- |
| ADR-001 | Unico repository smoroni72/TimestralCryptoLab, wiki in docs/wiki | Confermata | Codice e documenti hanno la stessa cronologia; niente GitHub Wiki separata |
| ADR-002 | Prima versione solo PAPER e nessuna chiave trading | Confermata | Nessun adapter di ordini reali; futures soltanto virtuali |
| ADR-003 | Separare Forecast, Strategy, Risk ed Execution | Confermata | Modello sostituibile, rischio con veto, test indipendenti |
| ADR-004 | Prima milestone tecnica: benchmark Timestral BTC/USDT e SOL/USDT | Confermata | Nessun bot prima della pianificazione e revisione del percorso di validazione |
| ADR-005 | Python 3.12 e harness offline per M1 | Proposta | Compatibilità Windows, dipendenze e licenze da verificare prima del lock |
| ADR-006 | Applicazione modulare in un processo, SQLite e dashboard leggera M2 | Proposta | Un writer e meno complessità operativa; contratti separati, non microservizi |
| ADR-007 | Fonte storica candidata Binance spot, 15m/1h | Proposta | Manifest/hash e gestione timestamp obbligatori; nessuna dipendenza da conto Binance |
| ADR-008 | 5M primario, 28M esplorativo; CPU come riferimento iniziale | Proposta | Risorse misurate, nessuna taglia scelta solo dai benchmark del produttore |
| ADR-009 | EUR distinto da USDT | Confermata come requisito di correttezza | Definire FX o un run in valuta quote prima di simulare capitale |

Ogni nuova decisione deve riportare problema, alternative, motivazione, evidenza e implicazioni per i test. Conservare gli esiti negativi; non sostituire retroattivamente un protocollo già valutato sul test senza una nuova versione.
