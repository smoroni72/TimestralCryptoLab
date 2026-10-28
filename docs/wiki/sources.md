# Fonti ufficiali e verifica preliminare

Consultazione documentale: 28 ottobre 2026. Queste fonti non sono test di esecuzione del progetto. Ricontrollare versioni/licenze quando si implementa M1 e fissare revisioni immutabili.

## Timestral

- [Repository ufficiale](https://github.com/mistralai/timestral).
- [README ufficiale](https://github.com/mistralai/timestral/blob/main/README.md).
- [Dipendenze dichiarate](https://github.com/mistralai/timestral/blob/main/pyproject.toml).
- [Pesi 5M e model card](https://huggingface.co/mistralai/Timestral-5M).
- [Licenza pesi](https://huggingface.co/mistralai/Timestral-209M/blob/main/LICENSE).

La documentazione descrive forecasting probabilistico, CPU/GPU, contesto fino a 32.768 passi e quantili. Indica Python ≥3.10, torch ≥2.4, NumPy, safetensors e huggingface_hub. Le taglie pubblicate sono 5M/28M/123M/209M; i file pesi fp32 indicati sono circa 21/111/490/837 MB. La RAM effettiva e la latenza sul PC Windows non sono state misurate.

Codice Apache 2.0; pesi con licenza Modified MIT separata e condizioni aggiuntive. Non trattarla come MIT standard: controllare il testo della taglia/revisione scelta e l'applicabilità delle condizioni prima dell'uso. Nessun parere legale o autorizzazione implicita all'uso dei pesi.

Il forecast non è un segnale di trading, e i benchmark generali riportati dal produttore non dimostrano un vantaggio su BTC/SOL.

## Dati

- [Repository ufficiale Binance Public Data](https://github.com/binance/binance-public-data).
- [Archivio pubblico](https://data.binance.vision/).
- [Documentazione spot](https://github.com/binance/binance-spot-api-docs).

La fonte descrive archivi daily/monthly, OHLCV, checksum e possibili aggiornamenti. Segnala microsecondi per i timestamp degli archivi spot dal 2025. La M1 deve verificare disponibilità delle singole serie, condizioni d'uso e integrità dei file; nessun dataset è già stato scaricato o validato nel repository.
