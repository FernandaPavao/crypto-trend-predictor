# pessoa2_ml/features.py
import pandas as pd
import numpy as np

def criar_features(df):
    """
    Engenharia de features avançada para classificação.
    Cria 13 features + target para cada moeda.
    
    Features criadas:
    - Variações de preço (1h, 6h, 12h, 24h)
    - Médias móveis (6h, 12h, 24h)
    - Volatilidade (6h, 24h)
    - Máximo e mínimo (24h)
    - RSI (Relative Strength Index)
    - Target: Preço sobe nas próximas 24h?
    """
    print("\n🧩 Criando features avançadas...")
    
    # Ordenar por moeda e timestamp
    df = df.sort_values(['coin_id', 'fetched_at']).reset_index(drop=True)
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])
    
    features_list = []
    
    # Processar cada moeda separadamente
    for coin in df['coin_id'].unique():
        coin_df = df[df['coin_id'] == coin].copy()
        
        print(f"  📊 Processando {coin}... ({len(coin_df)} registros)")
        
        # 1. VARIAÇÕES PERCENTUAIS
        coin_df['preco_variacao_1h'] = coin_df['price_usd'].pct_change(1)
        coin_df['preco_variacao_6h'] = coin_df['price_usd'].pct_change(6)
        coin_df['preco_variacao_12h'] = coin_df['price_usd'].pct_change(12)
        coin_df['preco_variacao_24h'] = coin_df['price_usd'].pct_change(24)
        
        # 2. MÉDIAS MÓVEIS
        coin_df['media_movel_6h'] = coin_df['price_usd'].rolling(window=6).mean()
        coin_df['media_movel_12h'] = coin_df['price_usd'].rolling(window=12).mean()
        coin_df['media_movel_24h'] = coin_df['price_usd'].rolling(window=24).mean()
        
        # 3. VOLATILIDADE (desvio padrão)
        coin_df['volatilidade_6h'] = coin_df['price_usd'].rolling(window=6).std()
        coin_df['volatilidade_24h'] = coin_df['price_usd'].rolling(window=24).std()
        
        # 4. MÁXIMO E MÍNIMO
        coin_df['max_24h'] = coin_df['price_usd'].rolling(window=24).max()
        coin_df['min_24h'] = coin_df['price_usd'].rolling(window=24).min()
        
        # 5. RSI (Relative Strength Index) - Indicador técnico
        delta = coin_df['price_usd'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        # Evitar divisão por zero
        rs = gain / loss.replace(0, np.nan)
        coin_df['rsi'] = 100 - (100 / (1 + rs))
        
        # 6. TARGET: Preço sobe ou desce nas próximas 24h?
        coin_df['preco_futuro_24h'] = coin_df['price_usd'].shift(-24)
        coin_df['target'] = (coin_df['preco_futuro_24h'] > coin_df['price_usd']).astype(int)
        
        features_list.append(coin_df)
    
    # Concatenar todas as moedas
    df_features = pd.concat(features_list, ignore_index=True)
    
    # Remover linhas com valores nulos (primeiros registros sem histórico suficiente)
    df_features = df_features.dropna()
    
    print(f"\n✅ Features criadas com sucesso!")
    print(f"📊 Total de registros válidos: {len(df_features)}")
    print(f"\n📈 Distribuição do Target:")
    print(df_features['target'].value_counts())
    print(f"\n⚖️  Balanceamento:")
    balance = df_features['target'].value_counts(normalize=True)
    print(f"  Queda (0): {balance[0]:.1%}")
    print(f"  Subida (1): {balance[1]:.1%}")
    
    # Verificar se há dados suficientes
    if len(df_features) < 50:
        print("\n⚠️  ATENÇÃO: Poucos dados para treinar modelo robusto!")
        print("   Recomendação: Aguarde mais coletas de dados.")
    
    return df_features