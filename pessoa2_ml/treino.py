# pessoa2_ml/treino.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import os

# Features que serão usadas no modelo
FEATURE_COLUMNS = [
    'price_usd', 'preco_variacao_1h', 'preco_variacao_6h', 
    'preco_variacao_12h', 'preco_variacao_24h',
    'media_movel_6h', 'media_movel_12h', 'media_movel_24h',
    'volatilidade_6h', 'volatilidade_24h',
    'max_24h', 'min_24h', 'rsi'
]

def treinar_modelo(df_features):
    """
    Treina Random Forest Classifier com validação cruzada.
    
    Args:
        df_features: DataFrame com features e target
        
    Returns:
        tuple: (modelo, scaler, feature_columns)
    """
    print("\n" + "="*60)
    print("🤖 TREINANDO MODELO DE MACHINE LEARNING")
    print("="*60)
    
    # Separar features e target
    X = df_features[FEATURE_COLUMNS]
    y = df_features['target']
    
    print(f"\n📊 Dataset:")
    print(f"   Features: {len(FEATURE_COLUMNS)}")
    print(f"   Amostras: {len(X)}")
    print(f"   Classes: {y.nunique()}")
    
    # Split treino/teste com estratificação
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📈 Divisão dos dados:")
    print(f"   Treino: {len(X_train)} amostras ({len(X_train)/len(X)*100:.1f}%)")
    print(f"   Teste: {len(X_test)} amostras ({len(X_test)/len(X)*100:.1f}%)")
    
    # Normalização dos dados
    print("\n🔄 Normalizando dados com StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Criar e treinar modelo
    print("\n🌲 Treinando Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
        verbose=0
    )
    
    modelo.fit(X_train_scaled, y_train)
    print("✅ Modelo treinado!")
    
    # Fazer previsões
    y_pred = modelo.predict(X_test_scaled)
    
    # AVALIAÇÃO DO MODELO
    print("\n" + "="*60)
    print("📊 RESULTADOS DO MODELO")
    print("="*60)
    
    # Acurácia
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Acurácia no teste: {accuracy:.2%}")
    
    # Relatório de classificação
    print("\n📋 Relatório Detalhado:")
    print(classification_report(y_test, y_pred, 
                                target_names=['⬇️  QUEDA (0)', '⬆️  SUBIDA (1)']))
    
    # Validação cruzada
    print("\n🔄 Validação Cruzada (5-fold):")
    cv_scores = cross_val_score(modelo, X_train_scaled, y_train, cv=5, scoring='accuracy')
    print(f"   Scores: {[f'{s:.2%}' for s in cv_scores]}")
    print(f"   Média: {cv_scores.mean():.2%} (±{cv_scores.std():.2%})")
    
    # Matriz de Confusão
    print("\n📊 Gerando gráficos de avaliação...")
    os.makedirs('graficos', exist_ok=True)
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu',
                xticklabels=['QUEDA', 'SUBIDA'],
                yticklabels=['QUEDA', 'SUBIDA'],
                cbar_kws={'label': 'Quantidade'})
    plt.title('Matriz de Confusão', fontsize=14, fontweight='bold')
    plt.ylabel('Real', fontsize=12)
    plt.xlabel('Previsto', fontsize=12)
    plt.tight_layout()
    plt.savefig('graficos/matriz_confusao.png', dpi=300, bbox_inches='tight')
    print("   💾 Matriz de confusão: graficos/matriz_confusao.png")
    plt.close()
    
    # Importância das Features
    importance_df = pd.DataFrame({
        'feature': FEATURE_COLUMNS,
        'importance': modelo.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔝 Top 5 Features mais importantes:")
    for idx, row in importance_df.head().iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
    plt.title('Importância das Features', fontsize=14, fontweight='bold')
    plt.xlabel('Importância', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    plt.savefig('graficos/feature_importance.png', dpi=300, bbox_inches='tight')
    print("   💾 Feature importance: graficos/feature_importance.png")
    plt.close()
    
    print("="*60)
    
    return modelo, scaler, FEATURE_COLUMNS


def salvar_modelo(modelo, scaler, feature_columns):
    """
    Salva modelo, scaler e feature_columns em arquivos pickle.
    
    Args:
        modelo: Modelo treinado
        scaler: StandardScaler ajustado
        feature_columns: Lista de colunas usadas
    """
    print("\n💾 Salvando modelo e artefatos...")
    
    # Criar pasta models
    os.makedirs("models", exist_ok=True)
    
    # Salvar modelo
    with open("models/modelo_crypto_classifier.pkl", "wb") as f:
        pickle.dump(modelo, f)
    print("   ✅ Modelo: models/modelo_crypto_classifier.pkl")
    
    # Salvar scaler
    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("   ✅ Scaler: models/scaler.pkl")
    
    # Salvar feature columns
    with open("models/feature_columns.pkl", "wb") as f:
        pickle.dump(feature_columns, f)
    print("   ✅ Features: models/feature_columns.pkl")
    
    print("\n✅ Todos os artefatos salvos com sucesso!")