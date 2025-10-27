# GitHub Pages - Configuração

## ⚠️ IMPORTANTE: Este projeto NÃO é um site estático

Este repositório contém um **chatbot com backend Python e frontend React** que precisa ser executado localmente ou em um servidor.

## 🚫 Por que não usar GitHub Pages?

- **Backend Python**: Precisa de um servidor para executar o FastAPI
- **Modelos NLP**: Arquivos grandes que não podem ser hospedados no GitHub Pages
- **Banco de dados**: Requer persistência de dados
- **Processamento local**: IA funciona localmente, não no navegador

## ✅ Como usar este projeto:

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd chatbot_tcc
   ```

2. **Execute localmente:**
   ```bash
   # Windows
   start_system.bat
   
   # Ou manualmente:
   cd backend
   python download_models.py
   python initialize_documents.py
   uvicorn main:app --reload
   
   # Em outro terminal:
   cd frontend
   npm install
   npm start
   ```

3. **Acesse:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🔧 Configuração do GitHub Pages

Este repositório está configurado para **NÃO** usar GitHub Pages:

- ✅ `.nojekyll` - Desabilita Jekyll
- ✅ `_config.yml` - Configuração mínima
- ✅ `.gitignore` - Exclui arquivos desnecessários

## 📚 Documentação

Consulte o `README.md` para instruções completas de instalação e uso.
