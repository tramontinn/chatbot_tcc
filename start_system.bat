@echo off
echo ========================================
echo    SISTEMA DE CHATBOT COM PLN LOCAL
echo ========================================
echo.

echo [1/4] Verificando modelos NLP...
cd backend
python download_models.py
if %errorlevel% neq 0 (
    echo AVISO: Falha ao baixar modelos NLP
    echo O sistema pode não funcionar corretamente
    echo.
)

echo.
echo [2/4] Inicializando documentos internos...
python initialize_documents.py
if %errorlevel% neq 0 (
    echo ERRO: Falha ao inicializar documentos
    pause
    exit /b 1
)

echo.
echo [3/4] Iniciando backend...
start "Backend" cmd /k "python main.py"

echo.
echo [4/4] Iniciando frontend...
cd ..\frontend
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo    SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
