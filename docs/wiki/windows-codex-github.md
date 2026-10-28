# Windows, Codex e GitHub: un solo repository

## Riferimenti

Remote ufficiale: `https://github.com/smoroni72/TimestralCryptoLab.git`.

Directory ufficiale: `C:\Users\smoro\Documents\Codex\TimestralCryptoLab`.

Work non vede direttamente il disco Windows. Ogni checkout fa riferimento allo stesso remote; commit/pull/push collegano il lavoro. La connessione GitHub di Work non configura automaticamente le credenziali Git del PC o l'app Codex.

## 1. Prima controllare, senza sovrascrivere

In PowerShell:

```powershell
Set-Location 'C:\Users\smoro\Documents\Codex\TimestralCryptoLab'
git rev-parse --show-toplevel
git status --short --branch
git remote -v
```

Se è già un repository, il primo comando deve indicare questa directory, non un suo genitore. `origin` deve essere il remote ufficiale. Se ci sono modifiche locali, conservarle con commit o stash ragionato prima del pull; niente reset/clean. Non eseguire tutti i percorsi seguenti: scegliere quello corrispondente allo stato effettivo.

## 2A. Repository locale già collegato correttamente

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git rev-parse HEAD
git rev-parse origin/main
```

I due SHA devono coincidere se non ci sono commit locali ulteriori. Se fast-forward non è possibile, fermarsi e confrontare le cronologie; niente force push, reset distruttivo o merge automatico con storie non correlate.

## 2B. Cartella esistente vuota, senza .git

Solo dopo aver verificato che è realmente vuota e non appartiene al repository di un genitore:

```powershell
git clone https://github.com/smoroni72/TimestralCryptoLab.git .
```

Il punto finale clona direttamente nella directory ufficiale: non crea `TimestralCryptoLab\TimestralCryptoLab`. Se ci sono già file, non usare questa procedura senza prima confrontarli e preservarli.

## 2C. File o cronologia locale preesistenti, remote assente o errato

Non inizializzare un secondo repository e non cambiare remote alla cieca. Mostrare a Codex lo stato e l'elenco file, preservare il lavoro e concordare l'integrazione. Se `origin` manca davvero, si può aggiungere il remote ufficiale dopo il controllo; una cronologia locale indipendente richiede confronto prima del merge.

## 3. Aprire in Codex e verificare il round trip

Aprire nell'app Codex la directory ufficiale, poi chiedere:

> Leggi AGENTS.md, README.md e ROADMAP.md. Verifica directory, remote, branch e SHA senza implementare codice. Conferma che la prima milestone tecnica è la validazione offline Timestral su BTC/USDT e SOL/USDT e che il trading automatico è sospeso.

Verifica iniziale: Codex deve leggere gli stessi file e lo stesso SHA pubblicato da Work. Per provare anche il percorso Codex → GitHub → Work, autorizzare successivamente una piccola modifica documentale, committarla/pusharla dal PC e farla rileggere a Work. Il round trip non è completato finché questa seconda direzione non è verificata.

Autenticarsi con i normali strumenti GitHub/Git Credential Manager dell'ambiente, se richiesto. Non incollare token nella chat né inserirli nell'URL del remote. Un permesso `push` dell'account non prova che ogni client abbia credenziali disponibili.

## 4. Flusso futuro

Prima di iniziare: fetch/pull e stato pulito o modifiche preservate. Lavori separati su branch quando utili, poi commit/PR sullo stesso repository. Dopo pubblicazione: l'altro ambiente fa fetch/pull e verifica SHA. Non modificare contemporaneamente lo stesso file senza aggiornarsi.

Questa guida non afferma che il checkout Windows o l'app Codex siano già stati verificati: serve il controllo dal PC.
