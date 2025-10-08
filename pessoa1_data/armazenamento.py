# pessoa1_data/armazenamento.py
import pandas as pd

def coletar_dados(conn):
    """
    Coleta todos os dados de criptomoedas do banco.
    
    Args:
        conn: Conexão com o banco de dados
        
    Returns:
        pd.DataFrame: DataFrame com os dados coletados
    """
    query = """
        SELECT coin_id, price_usd, price_brl, fetched_at 
        FROM public.raw_bitcoin_prices 
        ORDER BY coin_id, fetched_at
    """
    
    df = pd.read_sql(query, conn)
    
    print(f"📊 Dados coletados: {len(df)} registros")
    print(f"📈 Moedas: {df['coin_id'].nunique()}")
    
    if len(df) > 0:
        print(f"📅 Período: {df['fetched_at'].min()} até {df['fetched_at'].max()}")
    
    return df