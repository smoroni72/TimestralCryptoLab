# Stato del progetto

Aggiornato: 10 novembre 2026. Implementata soltanto la pipeline dati storici M1.

| Area | Stato ed evidenza |
| --- | --- |
| Repository ufficiale | smoroni72/TimestralCryptoLab; branch main, partenza pulita da 23b099f449647d016db19e1b272e5ced520efa6b |
| Windows / Codex locale | Directory, branch, remote e SHA verificati; Python 3.12.10, PyArrow 23.0.1 |
| GitHub | Nessuna pubblicazione autorizzata in questa attività; commit soltanto locale |
| Pipeline dati | Binance spot, cache/ripresa/checksum, UTC ms/us, Parquet, controlli e manifest implementati |
| Test dati | Suite offline deterministica e piccolo smoke reale; [evidenze](../../reports/m1-data-pipeline.md) |
| Timestral | Non installato; nessuna inferenza o misura hardware |
| Dataset M1 completo | Non scaricato; periodo proposto invariato e configurabile |
| Benchmark/baseline | Da sviluppare; nessun risultato previsionale disponibile |
| Bot, rischio, execution, dashboard | Da sviluppare dopo le milestone/gate; nessuna implementazione inclusa |
| Componenti simulati eseguibili | Nessuno |
| Trading reale | Escluso dalla prima versione e dalla roadmap attuale |

## Prossimo passo

Revisionare la [pipeline OHLCV](data-pipeline.md) e congelare lo snapshot dati. Benchmark e integrazione Timestral richiedono attività successive. M1 complessiva ancora aperta, split e parametri invariati.

## Regola di aggiornamento

Ogni milestone completata deve collegare evidenze reali: commit, comandi eseguiti, ambiente, test e report. Non spuntare criteri soltanto documentati. I commit effettivi sono nella cronologia Git: evitare un SHA autoreferenziale nel file che dovrebbe contenerlo.
