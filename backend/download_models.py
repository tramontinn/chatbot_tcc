import os
import requests
from sentence_transformers import SentenceTransformer
from pathlib import Path

def download_nlp_models():
    """Baixa os modelos NLP necessários para o funcionamento do chatbot."""
    
    print("Iniciando download dos modelos NLP...")
    
    models_dir = Path("nlp_models")
    models_dir.mkdir(exist_ok=True)
    
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    
    try:
        print(f"Baixando modelo: {model_name}")
        print("Este processo pode levar alguns minutos devido ao tamanho do modelo...")
        
        model = SentenceTransformer(model_name)
        model.save(str(models_dir / model_name))
        
        print(f"Modelo {model_name} baixado com sucesso!")
        print(f"Localização: {models_dir / model_name}")
        
        model_size = sum(f.stat().st_size for f in (models_dir / model_name).rglob('*') if f.is_file())
        model_size_mb = model_size / (1024 * 1024)
        print(f"Tamanho total do modelo: {model_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"Erro ao baixar o modelo: {e}")
        print("Verifique sua conexão com a internet e tente novamente.")
        return False
    
    return True

def check_models():
    """Verifica se os modelos estão disponíveis."""
    models_dir = Path("nlp_models")
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    
    if (models_dir / model_name).exists():
        print(f"Modelo {model_name} encontrado!")
        return True
    else:
        print(f"Modelo {model_name} não encontrado.")
        return False

if __name__ == "__main__":
    print("=== Download de Modelos NLP ===")
    
    if check_models():
        print("Modelos já estão disponíveis!")
    else:
        print("Modelos não encontrados. Iniciando download...")
        if download_nlp_models():
            print("Download concluído com sucesso!")
        else:
            print("Falha no download dos modelos.")
