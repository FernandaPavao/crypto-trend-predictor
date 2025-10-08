# pessoa2_ml/previsao.py
import pandas as pd

def fazer_previsao(modelo, scaler, feature_columns, df_features):
    """
    Faz previsões usando o modelo treinado.
    
    Args:
        modelo: Modelo treinado
        scaler: StandardScaler ajustado
        feature_columns: Lista de features
        df_features: DataFrame com os dados
        
    Returns:
        pd.DataFrame: DataFrame com previsões adicionadas
    """
    print("\n" + "="*60)
    print("📈 FAZENDO PREVISÕES")
    print("="*60)
    
    # Preparar features
    X = df_features[feature_columns]
    X_scaled = scaler.transform(X)
    
    # Fazer previsões
    df_features['previsao'] = modelo.predict(X_scaled)
    df_features['probabilidade'] = modelo.predict_proba(X_scaled)[:, 1]
    
    # Adicionar texto descritivo
    df_features['previsao_texto'] = df_features['previsao'].apply(
        lambda x: '⬆️  SUBIDA' if x == 1 else '⬇️  QUEDA'
    )
    
    print(f"\n✅ Previsões realizadas para {len(df_features)} registros")
    
    # Mostrar exemplos
    print("\n📊 Últimas 10 previsões:")
    print("-" * 60)
    
    resultado = df_features[[
        'coin_id', 'price_usd', 'previsao_texto', 'probabilidade', 'target'
    ]].tail(10)
    
    for idx, row in resultado.iterrows():
        real = '⬆️  SUBIDA' if row['target'] == 1 else '⬇️  QUEDA'
        acerto = '✅' if row['previsao_texto'] == real else '❌'
        
        print(f"{acerto} {row['coin_id']:8s} | "
              f"Preço: ${row['price_usd']:10,.2f} | "
              f"Prev: {row['previsao_texto']:12s} | "
              f"Prob: {row['probabilidade']:.1%} | "
              f"Real: {real}")
    
    # Estatísticas
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DAS PREVISÕES")
    print("="*60)
    
    total = len(df_features)
    subidas = (df_features['previsao'] == 1).sum()
    quedas = (df_features['previsao'] == 0).sum()
    
    print(f"\n⬆️  Previsões de SUBIDA: {subidas} ({subidas/total*100:.1f}%)")
    print(f"⬇️  Previsões de QUEDA: {quedas} ({quedas/total*100:.1f}%)")
    
    # Probabilidade média por tipo de previsão
    prob_subida = df_features[df_features['previsao'] == 1]['probabilidade'].mean()
    prob_queda = df_features[df_features['previsao'] == 0]['probabilidade'].mean()
    
    print(f"\n📊 Confiança média:")
    print(f"   Subidas: {prob_subida:.1%}")
    print(f"   Quedas: {1 - prob_queda:.1%}")
    
    # Acurácia (comparando com target real)
    if 'target' in df_features.columns:
        acertos = (df_features['previsao'] == df_features['target']).sum()
        acuracia = acertos / total
        print(f"\n✅ Acurácia geral: {acuracia:.1%} ({acertos}/{total})")
    
    print("="*60)
    
    return df_features