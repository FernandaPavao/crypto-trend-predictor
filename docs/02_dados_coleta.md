# Dados & Coleta

## Fonte
- **CoinGecko API (gratuita)** — dados de preço BTC/USD em janelas horárias/diárias.

## Pipeline
1) Buscar dados da API.
2) Normalizar colunas e timestamps.
3) Gravar no **PostgreSQL**.

## Conexão (variáveis de ambiente)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- (Opcional) `DATABASE_URL=postgresql://USER:PASS@HOST:PORT/DB`

## Tabela (exemplo)
- `timestamp` (UTC)
- `price_usd`
- `open_24h`, `high_24h`, `low_24h`, `volume_24h`
- (campos auxiliares conforme coleta)

## Execução (local)
```bash
# venv ativada e requirements instalados
python pessoa1_data/armazenamento.py

---

