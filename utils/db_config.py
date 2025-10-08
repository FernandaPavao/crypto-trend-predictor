# utils/db_config.py
import psycopg2

# Configurações do PostgreSQL (Railway)
DB_CONFIG = {
    'user': 'postgres',
    'password': 'xweuHpgkgdimaduzQxayHpTubMsfyudQ',
    'host': 'switchyard.proxy.rlwy.net',
    'database': 'railway',
    'port': 15453
}

def conectar_banco():
    """
    Estabelece conexão com o banco PostgreSQL.
    
    Returns:
        connection: Objeto de conexão do psycopg2
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conectado ao banco de dados!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None