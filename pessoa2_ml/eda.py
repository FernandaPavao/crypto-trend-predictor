# pessoa2_ml/eda.py
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analise_exploratoria(df):
    """
    Análise exploratória completa dos dados.
    Gera gráficos e estatísticas descritivas.
    """
    print("\n" + "="*60)
    print("🔍 ANÁLISE EXPLORATÓRIA DE DADOS")
    print("="*60)
    
    # Criar pasta para gráficos
    os.makedirs('graficos', exist_ok=True)
    
    # 1. Informações Gerais
    print("\n1️⃣ Informações Gerais:")
    print(df.info())
    
    # 2. Estatísticas
    print("\n2️⃣ Estatísticas Descritivas:")
    print(df[['price_usd', 'price_brl']].describe())
    
    # 3. Distribuição por Moeda
    print("\n3️⃣ Distribuição por Moeda:")
    print(df['coin_id'].value_counts())
    
    # 4. Gráficos
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Evolução de preços por moeda
    for coin in df['coin_id'].unique():
        coin_data = df[df['coin_id'] == coin]
        axes[0, 0].plot(coin_data.index, coin_data['price_usd'], label=coin, linewidth=2)
    axes[0, 0].set_title('Evolução de Preços (USD)', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Índice')
    axes[0, 0].set_ylabel('Preço USD')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Boxplot de distribuição
    df.boxplot(column='price_usd', by='coin_id', ax=axes[0, 1])
    axes[0, 1].set_title('Distribuição de Preços por Moeda', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Moeda')
    axes[0, 1].set_ylabel('Preço USD')
    plt.sca(axes[0, 1])
    plt.xticks(rotation=45)
    
    # Correlação USD vs BRL
    corr = df[['price_usd', 'price_brl']].corr()
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', 
                ax=axes[1, 0], cbar_kws={'label': 'Correlação'})
    axes[1, 0].set_title('Correlação USD vs BRL', fontsize=12, fontweight='bold')
    
    # Histograma de preços
    axes[1, 1].hist(df['price_usd'], bins=50, edgecolor='black', color='skyblue')
    axes[1, 1].set_title('Distribuição de Preços (USD)', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Preço USD')
    axes[1, 1].set_ylabel('Frequência')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('graficos/eda_completa.png', dpi=300, bbox_inches='tight')
    print("\n💾 Gráfico salvo: graficos/eda_completa.png")
    plt.close()
    
    print("="*60)