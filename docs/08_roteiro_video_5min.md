# Roteiro — Vídeo de 5 minutos

**0:00 – 0:20 | Abertura**
- Quem somos, objetivo do projeto.
- Frase-guia: “Transformamos dados de BTC em sinais de tendência via ML + API + Dashboard.”

**0:20 – 1:10 | O Problema e a Arquitetura**
- Mostrar diagrama simples (3 blocos: Dados → ML → API/UI).
- Dor: necessidade de sinais objetivos e integráveis.

**1:10 – 2:10 | Dados e Features**
- Falar da coleta (PostgreSQL) e dos 13 indicadores (RSI, MMs, volatilidades, variações).
- Print rápido do código de features e de um gráfico em `graficos/`.

**2:10 – 3:10 | Treino e Resultados**
- Mostrar pipeline (`pipeline_ml.py`), métricas (acurácia ~54%), matriz de confusão.
- Comentar que é baseline com grande espaço para melhoria.

**3:10 – 4:10 | API e Dashboard**
- Swagger da FastAPI (`/docs`): endpoints `/predict`, `/predict/batch`.
- Streamlit: aba individual (form), aba em lote (upload CSV).

**4:10 – 5:00 | Conclusão e Próximos Passos**
- Reforçar modularidade e reprodutibilidade.
- Próximos passos (tunagem, novos modelos, deploy cloud, monitoramento).
- Call-to-action: “link do GitHub + link do vídeo/contato”.
