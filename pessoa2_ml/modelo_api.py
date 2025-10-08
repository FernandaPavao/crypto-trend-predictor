# pessoa2_ml/modelo_api.py
import pickle
import pandas as pd
import os

# Features utilizadas no modelo (ATUALIZADAS com 13 features)
FEATURE_COLUMNS = [
    'price_usd', 'preco_variacao_1h', 'preco_variacao_6h', 
    'preco_variacao_12h', 'preco_variacao_24h',
    'media_movel_6h', 'media_movel_12h', 'media_movel_24h',
    'volatilidade_6h', 'volatilidade_24h',
    'max_24h', 'min_24h', 'rsi'
]

def carregar_modelo():
    """
    Carrega o modelo treinado e objetos necessários para predição.
    
    Returns:
        tuple: (modelo, scaler, feature_columns)
    """
    try:
        # Caminho relativo à pasta raiz do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models')
        
        modelo_path = os.path.join(models_dir, 'modelo_crypto_classifier.pkl')
        scaler_path = os.path.join(models_dir, 'scaler.pkl')
        features_path = os.path.join(models_dir, 'feature_columns.pkl')
        
        modelo = pickle.load(open(modelo_path, "rb"))
        scaler = pickle.load(open(scaler_path, "rb"))
        feature_columns = pickle.load(open(features_path, "rb"))
        
        print("✅ Modelo carregado com sucesso!")
        return modelo, scaler, feature_columns
    except FileNotFoundError as e:
        print(f"❌ Erro: Arquivo não encontrado - {e}")
        print("Execute 'python pessoa2_ml/pipeline_ml.py' primeiro para treinar o modelo.")
        return None, None, None


def prever_tendencia(dados_novos):
    """
    Faz previsão de tendência para novos dados.
    
    Args:
        dados_novos (dict): Dicionário com as 13 features necessárias
            Exemplo: {
                'price_usd': 45000.00,
                'preco_variacao_1h': 0.02,
                'preco_variacao_6h': 0.05,
                'preco_variacao_12h': 0.03,
                'preco_variacao_24h': 0.08,
                'media_movel_6h': 44500.50,
                'media_movel_12h': 44200.30,
                'media_movel_24h': 43800.00,
                'volatilidade_6h': 250.5,
                'volatilidade_24h': 450.2,
                'max_24h': 45500.00,
                'min_24h': 43000.00,
                'rsi': 65.5
            }
    
    Returns:
        dict: {
            'tendencia': int (0 ou 1),
            'probabilidade': float (0.0 a 1.0),
            'previsao_texto': str,
            'confianca': str
        }
    """
    modelo, scaler, features = carregar_modelo()
    
    if modelo is None:
        return {'erro': 'Modelo não encontrado'}
    
    # Validar se todas as features necessárias estão presentes
    missing_features = [f for f in features if f not in dados_novos]
    if missing_features:
        return {
            'erro': f'Features faltando: {missing_features}',
            'features_necessarias': features
        }
    
    # Criar DataFrame com os dados
    df = pd.DataFrame([dados_novos])
    X = df[features]
    
    # Normalizar dados
    X_scaled = scaler.transform(X)
    
    # Fazer previsão
    previsao = modelo.predict(X_scaled)[0]
    probabilidade = modelo.predict_proba(X_scaled)[0, 1]
    
    # Interpretar resultado
    previsao_texto = "⬆️  SUBIDA" if previsao == 1 else "⬇️  QUEDA"
    
    return {
        'tendencia': int(previsao),
        'probabilidade': float(probabilidade),
        'previsao_texto': previsao_texto,
        'confianca': f"{probabilidade * 100:.2f}%"
    }


def prever_batch(df_dados):
    """
    Faz previsões para múltiplos registros de uma vez.
    
    Args:
        df_dados (pd.DataFrame): DataFrame com as 13 features necessárias
    
    Returns:
        pd.DataFrame: DataFrame original com colunas de previsão adicionadas
    """
    modelo, scaler, features = carregar_modelo()
    
    if modelo is None:
        print("❌ Erro ao carregar modelo")
        return df_dados
    
    # Verificar se todas as features estão presentes
    missing_features = [f for f in features if f not in df_dados.columns]
    if missing_features:
        print(f"❌ Features faltando: {missing_features}")
        print(f"Features necessárias: {features}")
        return df_dados
    
    # Preparar dados
    X = df_dados[features]
    X_scaled = scaler.transform(X)
    
    # Fazer previsões
    df_dados['previsao'] = modelo.predict(X_scaled)
    df_dados['probabilidade'] = modelo.predict_proba(X_scaled)[:, 1]
    df_dados['previsao_texto'] = df_dados['previsao'].apply(
        lambda x: "⬆️  SUBIDA" if x == 1 else "⬇️  QUEDA"
    )
    
    print(f"✅ Previsões realizadas para {len(df_dados)} registros")
    
    # Estatísticas
    subidas = (df_dados['previsao'] == 1).sum()
    quedas = (df_dados['previsao'] == 0).sum()
    print(f"   ⬆️  Subidas previstas: {subidas} ({subidas/len(df_dados)*100:.1f}%)")
    print(f"   ⬇️  Quedas previstas: {quedas} ({quedas/len(df_dados)*100:.1f}%)")
    
    return df_dados


def verificar_modelo():
    """
    Verifica se os arquivos do modelo existem e estão acessíveis.
    
    Returns:
        dict: Status dos arquivos do modelo
    """
    # Caminho relativo à pasta raiz do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, 'models')
    
    arquivos = {
        'modelo': os.path.join(models_dir, 'modelo_crypto_classifier.pkl'),
        'scaler': os.path.join(models_dir, 'scaler.pkl'),
        'features': os.path.join(models_dir, 'feature_columns.pkl')
    }
    
    status = {}
    all_exist = True
    
    print("\n🔍 Verificando arquivos do modelo...")
    for nome, caminho in arquivos.items():
        existe = os.path.exists(caminho)
        status[nome] = existe
        emoji = "✅" if existe else "❌"
        print(f"   {emoji} {nome}: {caminho}")
        if not existe:
            all_exist = False
    
    if all_exist:
        print("\n✅ Todos os arquivos encontrados!")
    else:
        print("\n⚠️  Alguns arquivos não foram encontrados.")
        print("   Execute 'python pessoa2_ml/pipeline_ml.py' para gerar os arquivos.")
    
    return status

def obter_features_necessarias():
    """
    Retorna a lista de features que o modelo espera.
    
    Returns:
        list: Lista de nomes das features
    """
    return FEATURE_COLUMNS.copy()


# Exemplo de uso (para testes)
if __name__ == "__main__":
    print("="*70)
    print("🧪 TESTANDO FUNÇÕES DA API DO MODELO")
    print("="*70)
    
    # 1. Verificar se modelo existe
    print("\n[1/3] Verificando arquivos do modelo:")
    status = verificar_modelo()
    
    if not all(status.values()):
        print("\n❌ Execute 'python pipeline_ml.py' primeiro!")
        exit()
    
    # 2. Listar features necessárias
    print("\n[2/3] Features necessárias para previsão:")
    features = obter_features_necessarias()
    for i, feature in enumerate(features, 1):
        print(f"   {i:2d}. {feature}")
    
    # 3. Testar previsão individual
    print("\n[3/3] Testando previsão individual:")
    dados_teste = {
        'price_usd': 45000.00,
        'preco_variacao_1h': 0.02,
        'preco_variacao_6h': 0.05,
        'preco_variacao_12h': 0.03,
        'preco_variacao_24h': 0.08,
        'media_movel_6h': 44500.50,
        'media_movel_12h': 44200.30,
        'media_movel_24h': 43800.00,
        'volatilidade_6h': 250.5,
        'volatilidade_24h': 450.2,
        'max_24h': 45500.00,
        'min_24h': 43000.00,
        'rsi': 65.5
    }
    
    print("\n   Dados de entrada:")
    for key, value in dados_teste.items():
        print(f"      {key}: {value}")
    
    resultado = prever_tendencia(dados_teste)
    
    print("\n   Resultado da previsão:")
    for key, value in resultado.items():
        print(f"      {key}: {value}")
    
    print("\n" + "="*70)
    print("✅ TESTES CONCLUÍDOS!")
    print("="*70)