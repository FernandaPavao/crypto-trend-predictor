# pessoa2_ml/pipeline_ml.py
import sys
import os

# Adicionar a pasta raiz ao path para importações funcionarem
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_config import conectar_banco
from pessoa1_data.armazenamento import coletar_dados
from eda import analise_exploratoria
from features import criar_features
from treino import treinar_modelo, salvar_modelo
from previsao import fazer_previsao
from datetime import datetime

def pipeline_completo():
    """
    Pipeline completo de Machine Learning para previsão de criptomoedas.
    
    Etapas:
    1. Conexão com banco de dados
    2. Coleta de dados
    3. Análise exploratória (EDA)
    4. Engenharia de features
    5. Treinamento do modelo
    6. Salvamento dos artefatos
    7. Previsões de exemplo
    """
    print("\n" + "="*70)
    print("🚀 PIPELINE DE MACHINE LEARNING - CRYPTO PRICE PREDICTION")
    print("="*70)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 1. CONECTAR AO BANCO
    print("\n[1/7] 🔌 Conectando ao banco de dados...")
    conn = conectar_banco()
    
    if not conn:
        print("\n❌ ERRO: Não foi possível conectar ao banco!")
        print("   Verifique as configurações em utils/db_config.py")
        return
    
    # 2. COLETAR DADOS
    print("\n[2/7] 📊 Coletando dados do banco...")
    df = coletar_dados(conn)
    conn.close()
    
    # Verificar se há dados suficientes
    if len(df) < 100:
        print("\n⚠️  AVISO: Poucos dados disponíveis!")
        print(f"   Atual: {len(df)} registros")
        print("   Recomendado: Pelo menos 100 registros")
        print("   Aguarde mais coletas antes de treinar o modelo.")
        return
    
    # 3. ANÁLISE EXPLORATÓRIA
    print("\n[3/7] 🔍 Realizando análise exploratória...")
    analise_exploratoria(df)
    
    # 4. CRIAR FEATURES
    print("\n[4/7] 🧩 Criando features...")
    df_features = criar_features(df)
    
    # Verificar se há features suficientes
    if len(df_features) < 50:
        print("\n⚠️  AVISO: Dados insuficientes após feature engineering!")
        print(f"   Registros válidos: {len(df_features)}")
        print("   Recomendado: Pelo menos 50 registros")
        print("   Aguarde mais coletas de dados.")
        return
    
    # 5. TREINAR MODELO
    print("\n[5/7] 🤖 Treinando modelo...")
    modelo, scaler, feature_columns = treinar_modelo(df_features)
    
    # 6. SALVAR MODELO
    print("\n[6/7] 💾 Salvando modelo e artefatos...")
    salvar_modelo(modelo, scaler, feature_columns)
    
    # 7. FAZER PREVISÕES
    print("\n[7/7] 📈 Fazendo previsões de exemplo...")
    df_previsoes = fazer_previsao(modelo, scaler, feature_columns, df_features)
    
    # RESUMO FINAL
    print("\n" + "="*70)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*70)
    print(f"⏰ Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📦 ARQUIVOS GERADOS:")
    print("   📁 models/")
    print("      - modelo_crypto_classifier.pkl")
    print("      - scaler.pkl")
    print("      - feature_columns.pkl")
    print("   📁 graficos/")
    print("      - eda_completa.png")
    print("      - matriz_confusao.png")
    print("      - feature_importance.png")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("   1. Revise os gráficos em 'graficos/'")
    print("   2. Verifique a acurácia do modelo")
    print("   3. Envie a pasta 'pessoa2_ml/' completa para Pessoa 3")
    print("   4. Inclua também a pasta 'models/' com os arquivos .pkl")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    pipeline_completo()