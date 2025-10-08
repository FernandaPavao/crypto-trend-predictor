# Crypto Trend Predictor — Visão Geral

Sistema completo que prevê tendência de preço do Bitcoin com ML (Random Forest), servido por API (FastAPI) e Dashboard (Streamlit).

## Objetivo
- Prever subida/queda do BTC em janela curta usando 13 indicadores técnicos.
- Expor predições via API REST e UI web.
- Arquitetura modular por responsabilidade (coleta, ML, API/UI).

## Arquitetura (alto nível)
- **Coleta & Armazenamento**: `pessoa1_data/` + PostgreSQL (`utils/db_config.py`).
- **Modelagem & Treino**: `pessoa2_ml/` (EDA, features, treino, avaliação).
- **Serviço & UI**: `pessoa3/` (FastAPI + Streamlit).
- **Artefatos**: modelos em `models/` e gráficos em `graficos/`.

## Como rodar (resumo)
```bash
python -m venv .venv
# Linux/Mac: source .venv/bin/activate
# Windows:   .venv\Scripts\activate
pip install -r requirements.txt

# 1) (opcional) subir banco com Docker
# docker compose up -d db

# 2) coletar dados (se aplicável)
python pessoa1_data/armazenamento.py

# 3) treinar
python pessoa2_ml/pipeline_ml.py

# 4) API (http://localhost:8000/docs)
python pessoa3/api_fastapi.py

# 5) Dashboard (http://localhost:8501)
streamlit run pessoa3/dashboard.py
