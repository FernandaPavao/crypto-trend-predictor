
---

## 3) `docs/03_modelagem_ml.md` (features, modelo e métricas)
```markdown
# Modelagem de ML

## Target
- Binário: `0 = queda`, `1 = subida` (definido a partir de variação futura curta).

## Features (13)
- `price_usd`
- Variações: `delta_1h`, `delta_6h`, `delta_12h`, `delta_24h`
- Médias móveis: `mm_6h`, `mm_12h`, `mm_24h`
- Volatilidades: `vol_6h`, `vol_24h`
- `max_24h`, `min_24h`
- `rsi`

## Pipeline
1) EDA (`eda.py`): análise rápida e gráficos.
2) Engenharia de features (`features.py`).
3) Treino (`treino.py`): **Random Forest (100 árvores, max_depth=10)**.
4) Avaliação (`previsao.py`): hold-out 80/20 + cross-validation (5-fold).
5) Export: `modelo_crypto_classifier.pkl`, `scaler.pkl`, `feature_columns.pkl`.

## Métricas (baseline)
- **Acurácia ~54%** (MVP, espaço para melhorar).
- Matriz de confusão e feature importance em `graficos/`.

## Próximos passos
- Tuning (grid/random search).
- Modelos alternativos (XGBoost/LightGBM/LSTM).
- Backtesting com janela deslizante (walk-forward).
