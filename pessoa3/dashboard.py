#pessoa3/dashboard
# dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json

# Configuração da página
st.set_page_config(
    page_title="🚀 Crypto Trend Predictor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API
API_URL = "http://localhost:8000"

# Título principal
st.title("🚀 Crypto Trend Predictor Dashboard")
st.markdown("### Previsão de tendências de criptomoedas usando Machine Learning")

# Sidebar
st.sidebar.header("⚙️ Configurações")

# Verificar status da API
try:
    response = requests.get(f"{API_URL}/health", timeout=2)
    if response.status_code == 200:
        st.sidebar.success("✅ API Online")
    else:
        st.sidebar.error("❌ API com problemas")
except:
    st.sidebar.error("❌ API Offline")
    st.error("⚠️ A API não está rodando! Execute: `python api_fastapi.py`")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Predição Individual", "📈 Predição em Lote", "ℹ️ Informações"])

# ==================== TAB 1: PREDIÇÃO INDIVIDUAL ====================
with tab1:
    st.header("📊 Fazer Predição Individual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Dados de Preço")
        price_usd = st.number_input("Preço Atual (USD)", value=45000.00, step=100.0)
        max_24h = st.number_input("Máximo 24h (USD)", value=45500.00, step=100.0)
        min_24h = st.number_input("Mínimo 24h (USD)", value=43000.00, step=100.0)
        
        st.subheader("📈 Variações de Preço (%)")
        preco_variacao_1h = st.number_input("Variação 1h", value=0.02, format="%.4f")
        preco_variacao_6h = st.number_input("Variação 6h", value=0.05, format="%.4f")
        preco_variacao_12h = st.number_input("Variação 12h", value=0.03, format="%.4f")
        preco_variacao_24h = st.number_input("Variação 24h", value=0.08, format="%.4f")
    
    with col2:
        st.subheader("📊 Médias Móveis")
        media_movel_6h = st.number_input("Média Móvel 6h", value=44500.50, step=100.0)
        media_movel_12h = st.number_input("Média Móvel 12h", value=44200.30, step=100.0)
        media_movel_24h = st.number_input("Média Móvel 24h", value=43800.00, step=100.0)
        
        st.subheader("📉 Indicadores Técnicos")
        volatilidade_6h = st.number_input("Volatilidade 6h", value=250.5, step=10.0)
        volatilidade_24h = st.number_input("Volatilidade 24h", value=450.2, step=10.0)
        rsi = st.number_input("RSI (0-100)", value=65.5, min_value=0.0, max_value=100.0)
    
    # Botão de predição
    if st.button("🔮 Fazer Predição", type="primary", use_container_width=True):
        # Preparar dados
        dados = {
            "price_usd": price_usd,
            "preco_variacao_1h": preco_variacao_1h,
            "preco_variacao_6h": preco_variacao_6h,
            "preco_variacao_12h": preco_variacao_12h,
            "preco_variacao_24h": preco_variacao_24h,
            "media_movel_6h": media_movel_6h,
            "media_movel_12h": media_movel_12h,
            "media_movel_24h": media_movel_24h,
            "volatilidade_6h": volatilidade_6h,
            "volatilidade_24h": volatilidade_24h,
            "max_24h": max_24h,
            "min_24h": min_24h,
            "rsi": rsi
        }
        
        # Fazer requisição
        with st.spinner("🔄 Processando..."):
            try:
                response = requests.post(f"{API_URL}/predict", json=dados)
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    # Mostrar resultado
                    st.success("✅ Predição realizada com sucesso!")
                    
                    # Métricas principais
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            label="🎯 Tendência Prevista",
                            value=resultado['previsao_texto']
                        )
                    
                    with col2:
                        st.metric(
                            label="📊 Confiança",
                            value=resultado['confianca']
                        )
                    
                    with col3:
                        prob_valor = resultado['probabilidade']
                        st.metric(
                            label="🎲 Probabilidade",
                            value=f"{prob_valor:.4f}"
                        )
                    
                    # Gráfico de probabilidade
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=resultado['probabilidade'] * 100,
                        title={'text': "Confiança da Predição (%)"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkgreen" if resultado['tendencia'] == 1 else "darkred"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 75], 'color': "gray"},
                                {'range': [75, 100], 'color': "darkgray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # JSON da resposta
                    with st.expander("📄 Ver JSON da Resposta"):
                        st.json(resultado)
                        
                else:
                    st.error(f"❌ Erro: {response.json()}")
                    
            except Exception as e:
                st.error(f"❌ Erro ao fazer predição: {str(e)}")

# ==================== TAB 2: PREDIÇÃO EM LOTE ====================
with tab2:
    st.header("📈 Predição em Lote (CSV)")
    
    st.markdown("""
    **Upload de arquivo CSV com as 13 features:**
    - price_usd, preco_variacao_1h, preco_variacao_6h, preco_variacao_12h, preco_variacao_24h
    - media_movel_6h, media_movel_12h, media_movel_24h
    - volatilidade_6h, volatilidade_24h
    - max_24h, min_24h, rsi
    """)
    
    # Upload de arquivo
    uploaded_file = st.file_uploader("📁 Escolha um arquivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Ler CSV
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Arquivo carregado: {len(df)} registros")
            
            # Mostrar preview
            st.subheader("👀 Preview dos Dados")
            st.dataframe(df.head(10))
            
            # Botão para fazer predições
            if st.button("🔮 Fazer Predições em Lote", type="primary"):
                with st.spinner("🔄 Processando predições..."):
                    try:
                        # Converter para lista de dicionários
                        dados_lista = df.to_dict('records')
                        
                        # Fazer requisição
                        response = requests.post(f"{API_URL}/predict/batch", json=dados_lista)
                        
                        if response.status_code == 200:
                            resultado = response.json()
                            
                            # Adicionar predições ao DataFrame
                            previsoes = resultado['previsoes']
                            df['previsao_texto'] = [p['previsao_texto'] for p in previsoes]
                            df['probabilidade'] = [p['probabilidade'] for p in previsoes]
                            df['confianca'] = [p['confianca'] for p in previsoes]
                            
                            st.success(f"✅ {resultado['total']} predições realizadas!")
                            
                            # Estatísticas
                            col1, col2, col3 = st.columns(3)
                            
                            subidas = sum(1 for p in previsoes if p['tendencia'] == 1)
                            quedas = len(previsoes) - subidas
                            
                            with col1:
                                st.metric("⬆️ Subidas Previstas", subidas)
                            
                            with col2:
                                st.metric("⬇️ Quedas Previstas", quedas)
                            
                            with col3:
                                st.metric("📊 Total", len(previsoes))
                            
                            # Mostrar resultados
                            st.subheader("📊 Resultados")
                            st.dataframe(df)
                            
                            # Download
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="💾 Download Resultados (CSV)",
                                data=csv,
                                file_name="previsoes_crypto.csv",
                                mime="text/csv"
                            )
                            
                        else:
                            st.error(f"❌ Erro: {response.json()}")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao processar: {str(e)}")
                        
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo: {str(e)}")

# ==================== TAB 3: INFORMAÇÕES ====================
with tab3:
    st.header("ℹ️ Informações do Sistema")
    
    # Buscar features da API
    try:
        response = requests.get(f"{API_URL}/features")
        if response.status_code == 200:
            features_info = response.json()
            
            st.subheader("📋 Features Necessárias")
            st.write(f"**Total:** {features_info['total']} features")
            
            # Lista de features
            for i, feature in enumerate(features_info['features'], 1):
                st.write(f"{i}. `{feature}`")
            
            # Exemplo
            st.subheader("💡 Exemplo de Dados")
            st.json(features_info['exemplo'])
            
    except Exception as e:
        st.error(f"❌ Erro ao buscar informações: {str(e)}")
    
    # Documentação
    st.subheader("📖 Documentação da API")
    st.markdown(f"**URL da API:** {API_URL}")
    st.markdown(f"**Documentação Interativa:** [{API_URL}/docs]({API_URL}/docs)")
    
    # Endpoints
    st.subheader("🔗 Endpoints Disponíveis")
    st.code("""
GET  /              - Informações da API
GET  /health        - Status do sistema
GET  /features      - Lista de features necessárias
POST /predict       - Predição individual
POST /predict/batch - Predição em lote
    """)

# Footer
st.markdown("---")
st.markdown("🚀 **Crypto Trend Predictor** | Desenvolvido com FastAPI + Streamlit")