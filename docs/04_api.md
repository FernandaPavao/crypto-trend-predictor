# API (FastAPI)

## Rodando local
```bash
python pessoa3/api_fastapi.py
# http://localhost:8000/docs (Swagger)
Endpoints
GET / — info

Retorna metadados da API.

GET /health — saúde

{"status": "ok"} se modelos carregaram.

GET /features — lista de features

Ex.: ["price_usd","delta_1h",...,"rsi"]

POST /predict — predição individual

Request (JSON):

{
  "price_usd": 64000,
  "delta_1h": 0.001,
  "...": 0.0,
  "rsi": 52.3
}


Response:

{"prediction": 1, "proba_up": 0.56}

POST /predict/batch — lote

Upload de CSV ou JSON array.

Retorna lista com prediction/proba_up por linha.

Erros comuns

422 Unprocessable Entity: JSON com chave/valor inválido.

500: modelos ausentes em models/ — rode o treino.