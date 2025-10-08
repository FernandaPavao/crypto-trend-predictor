# Arquitetura — Crypto Trend Predictor

[Coleta (API pública) ] --> [PostgreSQL]
|
v
[Features + Treino (Random Forest)] --> [models/*.pkl | scaler.pkl | feature_columns.pkl]
|
v
[FastAPI + Streamlit]

## Componentes
- **Coleta & Armazenamento** (`pessoa1_data/`, `utils/db_config.py`)
  - Busca dados (CoinGecko), salva no **PostgreSQL**.
- **Modelagem & Treino** (`pessoa2_ml/`)
  - EDA, criação de 13 features, treino do **Random Forest**, avaliação.
- **Serviço & UI** (`pessoa3/`)
  - **FastAPI** expõe `/predict` e `/predict/batch`.
  - **Streamlit**: predição individual e em lote.

## Artefatos
- **models/**: `modelo_crypto_classifier.pkl`, `scaler.pkl`, `feature_columns.pkl`
- **graficos/**: EDA, matriz de confusão, importância das features.
