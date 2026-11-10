# tests

`test_data.py`: suite unittest offline con piccole fixture ZIP temporanee,
HTTP simulato per la ripresa e verifiche Parquet/manifest. Eseguire:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Smoke reale separato, mai incluso nella suite: [guida](../docs/wiki/data-pipeline.md).
Il resto del [piano test](../docs/wiki/testing.md) riguarda attività successive.
