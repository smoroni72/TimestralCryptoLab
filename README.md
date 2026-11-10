# Timestral Crypto Lab

Laboratorio quantitativo per verificare modelli previsionali crypto e, successivamente, strategie autonome **esclusivamente PAPER con capitale virtuale**.

> Stato: prima attività M1 implementata, limitatamente alla pipeline OHLCV storica. Nessun bot, simulatore, dashboard o benchmark previsionale. Nessuna installazione o misura di Timestral.

## Prima attività tecnica

Validare Timestral offline su **OHLCV storici BTC/USDT e SOL/USDT**, con benchmark cronologici, confronti con baseline, controllo del leakage e misure di risorse hardware. Non avviare trading automatico. Il piano è in [docs/wiki/timestral-validation.md](docs/wiki/timestral-validation.md).

## Documenti principali

| Documento | Contenuto |
| --- | --- |
| [PRD.md](PRD.md) | Requisiti completi e vincoli del prodotto |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Componenti, contratti e stack proposto |
| [ROADMAP.md](ROADMAP.md) | Milestone, dipendenze e criteri di accettazione |
| [AGENTS.md](AGENTS.md) | Istruzioni per Codex e agenti |
| [Wiki](docs/wiki/README.md) | Guide tecniche e funzionali versionate |
| [Stato](docs/wiki/status.md) | Implementato, simulato, pianificato e verifiche pendenti |

## Unico repository

Remote ufficiale: https://github.com/smoroni72/TimestralCryptoLab

Directory Windows ufficiale: `C:\Users\smoro\Documents\Codex\TimestralCryptoLab`.

Work opera sullo stesso remote; Codex usa il checkout Windows. La sincronizzazione avviene con commit, fetch/pull e push, non tramite accesso diretto di Work al disco Windows. Vedere [guida sincronizzazione](docs/wiki/windows-codex-github.md). Directory, remote e commit iniziale sono stati verificati sul PC in questa attività; nessun push eseguito.

## Struttura

```text
TimestralCryptoLab/
  README.md  PRD.md  ARCHITECTURE.md  ROADMAP.md  AGENTS.md
  docs/wiki/        # specifiche e guide, stessa cronologia del codice
  src/              # futura applicazione modulare
  benchmarks/       # futuro harness di validazione offline
  tests/            # futuri test unitari e integrazione
  config/           # futuri schemi e configurazioni non segrete
  scripts/          # future utility Windows/Linux
  infra/            # futuro packaging/containerizzazione
  reports/          # report approvati e risultati sintetici versionati
```

`src/timestral_crypto_lab` contiene la pipeline storica e `tests/test_data.py` i test offline. Le altre componenti applicative rimangono pianificate. Dati grezzi, Parquet, cache, pesi, database e segreti non vanno in Git.

## Stack candidato

Pipeline corrente: Python 3.12, PyArrow 23.0.1 e unittest. Il restante stack (NumPy/PyTorch, pytest, futuro MVP) rimane candidato e non è installato da questa attività.

## Avvio e test

Installazione PowerShell, acquisizione completa, ripresa e smoke test sono nella [guida pipeline OHLCV](docs/wiki/data-pipeline.md). Verifiche effettive e limiti sono nel [report](reports/m1-data-pipeline.md). Il checkout Windows è stato verificato al commit di partenza `23b099f449647d016db19e1b272e5ced520efa6b`; questa attività resta locale, senza push. Il benchmark previsionale richiede una successiva attività.

PAPER permanente, nessun ordine reale eseguibile e nessuna richiesta di credenziali finanziarie sono vincoli della prima versione.
