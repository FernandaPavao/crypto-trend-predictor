#pessoa3/api_fastapi

# api_fastapi.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import sys
import os


# Adicionar a pasta raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pessoa2_ml.modelo_api import (
    prever_tendencia,
    verificar_modelo,
    obter_features_necessarias,
    carregar_modelo
)

# Criar aplicação FastAPI
app = FastAPI(
    title="🚀 Crypto Trend Predictor API",
    description="API para prever tendências de criptomoedas (SUBIDA/QUEDA)",
    version="1.0.0"
)

# Modelo de dados para entrada
class DadosCrypto(BaseModel):
    price_usd: float = Field(..., description="Preço atual em USD", example=45000.00)
    preco_variacao_1h: float = Field(..., description="Variação % 1h", example=0.02)
    preco_variacao_6h: float = Field(..., description="Variação % 6h", example=0.05)
    preco_variacao_12h: float = Field(..., description="Variação % 12h", example=0.03)
    preco_variacao_24h: float = Field(..., description="Variação % 24h", example=0.08)
    media_movel_6h: float = Field(..., description="Média móvel 6h", example=44500.50)
    media_movel_12h: float = Field(..., description="Média móvel 12h", example=44200.30)
    media_movel_24h: float = Field(..., description="Média móvel 24h", example=43800.00)
    volatilidade_6h: float = Field(..., description="Volatilidade 6h", example=250.5)
    volatilidade_24h: float = Field(..., description="Volatilidade 24h", example=450.2)
    max_24h: float = Field(..., description="Máximo 24h", example=45500.00)
    min_24h: float = Field(..., description="Mínimo 24h", example=43000.00)
    rsi: float = Field(..., description="RSI (0-100)", example=65.5)

    class Config:
        schema_extra = {
            "example": {
                "price_usd": 45000.00,
                "preco_variacao_1h": 0.02,
                "preco_variacao_6h": 0.05,
                "preco_variacao_12h": 0.03,
                "preco_variacao_24h": 0.08,
                "media_movel_6h": 44500.50,
                "media_movel_12h": 44200.30,
                "media_movel_24h": 43800.00,
                "volatilidade_6h": 250.5,
                "volatilidade_24h": 450.2,
                "max_24h": 45500.00,
                "min_24h": 43000.00,
                "rsi": 65.5
            }
        }


# Modelo de resposta
class RespostaPrevisao(BaseModel):
    tendencia: int = Field(..., description="0 = QUEDA, 1 = SUBIDA")
    probabilidade: float = Field(..., description="Probabilidade (0.0 a 1.0)")
    previsao_texto: str = Field(..., description="Texto descritivo")
    confianca: str = Field(..., description="Confiança em %")


@app.get("/")
def home():
    """Endpoint raiz - Informações da API"""
    return {
        "mensagem": "🚀 Crypto Trend Predictor API",
        "versao": "1.0.0",
        "status": "online",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "features": "/features",
            "predict": "/predict (POST)"
        }
    }


@app.get("/health")
def health_check():
    """Verifica se a API e o modelo estão funcionando"""
    status = verificar_modelo()
    
    if all(status.values()):
        return {
            "status": "healthy",
            "modelo": "✅ OK",
            "scaler": "✅ OK",
            "features": "✅ OK"
        }
    else:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "arquivos": status,
                "mensagem": "Execute 'python pessoa2_ml/pipeline_ml.py' para gerar os arquivos"
            }
        )


@app.get("/features")
def listar_features():
    """Lista as 13 features necessárias para predição"""
    features = obter_features_necessarias()
    return {
        "total": len(features),
        "features": features,
        "exemplo": {
            "price_usd": 45000.00,
            "preco_variacao_1h": 0.02,
            "preco_variacao_6h": 0.05,
            "preco_variacao_12h": 0.03,
            "preco_variacao_24h": 0.08,
            "media_movel_6h": 44500.50,
            "media_movel_12h": 44200.30,
            "media_movel_24h": 43800.00,
            "volatilidade_6h": 250.5,
            "volatilidade_24h": 450.2,
            "max_24h": 45500.00,
            "min_24h": 43000.00,
            "rsi": 65.5
        }
    }


@app.post("/predict", response_model=RespostaPrevisao)
def fazer_previsao(dados: DadosCrypto):
    """
    Faz predição de tendência para uma criptomoeda
    
    - **Entrada**: 13 features da criptomoeda
    - **Saída**: Tendência (SUBIDA/QUEDA) + Probabilidade
    """
    try:
        # Converter para dicionário
        dados_dict = dados.dict()
        
        # Fazer predição
        resultado = prever_tendencia(dados_dict)
        
        # Verificar se houve erro
        if 'erro' in resultado:
            raise HTTPException(
                status_code=400,
                detail=resultado
            )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "erro": str(e),
                "mensagem": "Erro ao fazer predição"
            }
        )


@app.post("/predict/batch")
def fazer_previsao_batch(dados_lista: List[DadosCrypto]):
    """
    Faz predições para múltiplas criptomoedas de uma vez
    
    - **Entrada**: Lista de dados de criptomoedas
    - **Saída**: Lista de predições
    """
    try:
        resultados = []
        
        for dados in dados_lista:
            dados_dict = dados.dict()
            resultado = prever_tendencia(dados_dict)
            resultados.append(resultado)
        
        return {
            "total": len(resultados),
            "previsoes": resultados
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "erro": str(e),
                "mensagem": "Erro ao fazer predições em lote"
            }
        )


# Executar com: uvicorn api_fastapi:app --reload
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API na porta 8000...")
    print("📖 Documentação: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)