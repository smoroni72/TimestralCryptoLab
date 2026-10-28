# Timestral Crypto Lab

Laboratorio quantitativo per verificare modelli previsionali crypto e, successivamente, strategie autonome **esclusivamente PAPER con capitale virtuale**.

> Stato: documentazione, struttura e piano di validazione. Nessun bot, simulatore, dashboard o benchmark implementato in questa consegna. Nessun risultato di Timestral misurato sul progetto.

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

Work opera sullo stesso remote; Codex usa il checkout Windows. La sincronizzazione avviene con commit, fetch/pull e push, non tramite accesso diretto di Work al disco Windows. Vedere [guida sincronizzazione](docs/wiki/windows-codex-github.md). La verifica sul PC rimane da effettuare da Stefano.

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

Le directory contengono soltanto README descrittivi. Dati grezzi, cache, pesi, database e segreti non vanno in Git. Manifest, checksum, protocolli e report riassuntivi rendono riproducibili gli esperimenti.

## Stack candidato

Python 3.12, NumPy/PyTorch per ricerca; pytest per test. Per il successivo MVP: SQLite, FastAPI/Uvicorn e HTML/CSS/JavaScript responsive. Nessuna dipendenza è ancora fissata o installata dal repository; lo stack è da verificare su Windows nella M1.

## Avvio e test

Non esistono ancora comandi di avvio dell'app o test applicativi. Non usare codice proveniente da prototipi esterni a questo repository come componente già approvato. Dopo la revisione documentale si potrà autorizzare la sola implementazione del benchmark M1.

PAPER permanente, nessun ordine reale eseguibile e nessuna richiesta di credenziali finanziarie sono vincoli della prima versione.
