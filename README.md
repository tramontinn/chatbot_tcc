# Chatbot TCC

Este é o projeto final do TCC, um chatbot inteligente com IA local para processamento de documentos internos.

## Estrutura do Projeto

O projeto é dividido em duas partes principais:

- `backend/`: Contém a lógica do chatbot, processamento de NLP, gerenciamento de documentos e a API FastAPI.
- `frontend/`: Contém a interface do usuário desenvolvida em React.

## Como Configurar e Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

Certifique-se de ter o seguinte instalado:

- Python 3.9+
- Node.js (versão LTS recomendada)
- npm ou yarn
- Git

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd chatbot_tcc
```

### 3. Configurar o Backend

Navegue até o diretório do backend, crie um ambiente virtual e instale as dependências.

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

#### Baixar Modelos NLP (OBRIGATÓRIO)

Os modelos de NLP são muito grandes para serem incluídos no repositório. Você deve baixá-los manualmente:

```bash
python download_models.py
```

**Nota:** Este processo pode levar alguns minutos devido ao tamanho dos modelos (~470MB).

#### Inicializar Documentos Internos (Opcional, mas recomendado para testes)

O chatbot pode carregar documentos de uma pasta interna. Para pré-processar os documentos de exemplo:

```bash
python initialize_documents.py
```

#### Rodar o Servidor Backend

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`.

### 4. Configurar o Frontend

Abra um novo terminal, navegue até o diretório do frontend e instale as dependências.

```bash
cd frontend
npm install # ou yarn install
```

#### Rodar o Aplicativo Frontend

```bash
npm start # ou yarn start
```

O aplicativo frontend estará disponível em `http://localhost:3000`.

### 5. Acessar o Chatbot

Abra seu navegador e acesse `http://localhost:3000` para interagir com o chatbot.

## Solução de Problemas

### Erro: "Modelo não encontrado"

Se você receber um erro indicando que o modelo NLP não foi encontrado:

1. Certifique-se de que executou `python download_models.py`
2. Verifique se o diretório `nlp_models/` foi criado no backend
3. Verifique sua conexão com a internet durante o download

### Arquivos Grandes

Os modelos de NLP são grandes (~470MB) e não são incluídos no repositório Git para evitar problemas com o GitHub. Eles são baixados automaticamente na primeira execução ou manualmente com o script `download_models.py`.

## Contribuição

Sinta-se à vontade para contribuir com melhorias, correções de bugs ou novas funcionalidades.

## Licença

Este projeto está licenciado sob a licença MIT.
