
#### `docs/07_storytelling.md`
```markdown
# Storytelling — Crypto Trend Predictor

## 1. Contexto
- Mercado de cripto é volátil e orientado a dados.
- Objetivo: apoiar decisão com um classificador simples de tendência (subida/queda) em janela curta.

## 2. Problema de Negócio
- Traders precisam de sinais objetivos e reprodutíveis.
- Relatórios consistentes e APIs acessíveis para integrar a outros sistemas.

## 3. Abordagem
- **Pessoa 1 (Dados):** pipeline de coleta (API pública), persistência em PostgreSQL.
- **Pessoa 2 (ML):** EDA, criação de 13 features técnicas, treino com Random Forest, avaliação.
- **Pessoa 3 (Serviço & UI):** API REST (FastAPI) e Dashboard interativo (Streamlit).
- **Artefatos:** modelos e gráficos versionados.

## 4. Jornada Técnica
- Definição de esquema e conexão segura (env).
- Engenharia de features: MM, volatilidade, RSI, máximos/mínimos, variações temporais.
- Validação com hold-out e cross-validation.
- Empacotamento do modelo (`.pkl`) e interface via `modelo_api.py`.
- Publicação de endpoints e UI para consumo humano.

## 5. Resultados
- Acurácia ~54% em baseline com RF (room to improve).
- Predição em tempo real via API e em lote via Dashboard.
- Documentação e reprodutibilidade (requirements, scripts, docs).

## 6. Próximos Passos
- Tunagem de hiperparâmetros e modelos (XGBoost/LightGBM).
- Features de ordem superior (indicadores adicionais).
- Monitoramento de drift e re-treino automático.
- Deploy em nuvem com CI/CD e storage de modelos (MLflow).

## 7. Valor
- Base sólida e modular para evoluir de POC para produção.
- Facilita integração (API), análise (dashboard) e auditoria (docs).
