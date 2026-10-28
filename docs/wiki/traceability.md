# Tracciabilità requisiti e accettazione

| Requisiti PRD | Specifica principale | Gate |
| --- | --- | --- |
| F01, N03, N08, N11 | [Dati](data-contracts.md), [protocollo](timestral-validation.md) | M1 qualità/causalità |
| F02–F04, N02, N06, N10, N12 | [Protocollo](timestral-validation.md), [fonti](sources.md), [test](testing.md) | M1 inferenza, confronto e report |
| F05–F08, N01, N03–N07, N11 | [Architettura](../../ARCHITECTURE.md), [rischio](risk-and-execution.md) | M2 end-to-end e invarianti |
| F09, N09 | [Guida funzionale](functional-guide.md) | M2 PAPER/UI/controlli |
| F10–F11 | [Roadmap](../../ROADMAP.md), [architettura](../../ARCHITECTURE.md) | M3 ranking e modello |
| F12, N07–N08, N12 | [Roadmap](../../ROADMAP.md), [test](testing.md) | M4 backtest e confronto netto |
| F13, N01, N06–N07 | [Rischio](risk-and-execution.md), [test](testing.md) | M5 ledger futures |
| F14, N03–N05 | [Roadmap](../../ROADMAP.md), [architettura](../../ARCHITECTURE.md) | M6 soak e guasti |
| F15, N10 | [Roadmap](../../ROADMAP.md) | M7 deployment/restore |

La sola presenza di una specifica non significa requisito implementato. In fase di sviluppo aggiungere link ai test e ai report effettivi, conservando lo stato nel [registro](status.md).
