fromfastapiimportFastAPI,HTTPException,UploadFile,File,Form
fromfastapi.middleware.corsimportCORSMiddleware
fromfastapi.responsesimportJSONResponse
frompydanticimportBaseModel
fromtypingimportList,Optional
importos
importuvicorn
fromdotenvimportload_dotenv
importjson
fromdatetimeimportdatetime
frompathlibimportPath

fromchatbot.document_processorimportDocumentProcessor
fromchatbot.optimized_chat_managerimportOptimizedChatManager
fromchatbot.optimized_vector_storeimportOptimizedVectorStore
fromchatbot.internal_document_managerimportInternalDocumentManager

defcheck_nlp_models():
    """Verifica se os modelos NLP estão disponíveis."""
    models_dir=Path("nlp_models")
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
    
    ifnot(models_dir/model_name).exists():
        print("AVISO: Modelos NLP não encontrados!")
        print("Execute: python download_models.py")
        print("O chatbot pode não funcionar corretamente sem os modelos.")
        returnFalse
    returnTrue

load_dotenv()

ifnotcheck_nlp_models():
    print("Continuando sem verificação de modelos...")

app=FastAPI(title="Chatbot IA Local",description="Chatbot com IA local para documentos internos usando PLN")

app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

document_processor=DocumentProcessor()
vector_store=OptimizedVectorStore()
internal_doc_manager=InternalDocumentManager()
chat_manager=OptimizedChatManager(vector_store,internal_doc_manager)

classChatMessage(BaseModel):
    message:str
session_id:Optional[str]=None

classChatResponse(BaseModel):
    response:str
session_id:str
timestamp:str
sources:List[str]=[]

classFeedbackRequest(BaseModel):
    session_id:str
question:str
response:str
satisfaction:int
feedback_text:Optional[str]=None

classLearningStats(BaseModel):
    total_interactions:int
total_categories:int
most_popular_categories:List[tuple]
average_satisfaction:Optional[float]
last_learning:Optional[str]

classDocumentInfo(BaseModel):
    filename:str
content_type:str
size:int
processed:bool

@app.get("/")
asyncdefroot():
    return{"message":"Chatbot IA API está funcionando!"}

@app.post("/chat",response_model=ChatResponse)
asyncdefchat(message:ChatMessage):
    """Processa uma mensagem do usuário e retorna resposta do chatbot"""
try:
        response,session_id,sources=awaitchat_manager.process_message(
message.message,message.session_id
)

returnChatResponse(
response=response,
session_id=session_id,
timestamp=datetime.now().isoformat(),
sources=sources
)
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro no processamento: {str(e)}")

@app.post("/upload-document")
asyncdefupload_document(file:UploadFile=File(...)):
    """Faz upload e processa um documento"""
try:

        allowed_types=["application/pdf","text/plain","application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
iffile.content_typenotinallowed_types:
            raiseHTTPException(status_code=400,detail="Tipo de arquivo não suportado")

content=awaitdocument_processor.process_file(file)

vector_store.add_documents([content],[file.filename])

return{
"message":"Documento processado com sucesso",
"filename":file.filename,
"content_type":file.content_type,
"size":len(content)
}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro no processamento do documento: {str(e)}")

@app.get("/documents",response_model=List[DocumentInfo])
asyncdeflist_documents():
    """Lista todos os documentos processados"""
try:
        documents=vector_store.list_documents()
returndocuments
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao listar documentos: {str(e)}")

@app.delete("/documents/{filename}")
asyncdefdelete_document(filename:str):
    """Remove um documento do sistema"""
try:
        success=vector_store.delete_document(filename)
ifsuccess:
            return{"message":f"Documento {filename} removido com sucesso"}
else:
            raiseHTTPException(status_code=404,detail="Documento não encontrado")
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao remover documento: {str(e)}")

@app.get("/chat-history/{session_id}")
asyncdefget_chat_history(session_id:str):
    """Retorna o histórico de uma sessão de chat"""
try:
        history=chat_manager.get_session_history(session_id)
return{"session_id":session_id,"history":history}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao buscar histórico: {str(e)}")

@app.delete("/chat-history/{session_id}")
asyncdefclear_chat_history(session_id:str):
    """Limpa o histórico de uma sessão de chat"""
try:
        chat_manager.clear_session_history(session_id)
return{"message":"Histórico limpo com sucesso"}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao limpar histórico: {str(e)}")

@app.get("/internal-documents")
asyncdeflist_internal_documents():
    """Lista todos os documentos internos"""
try:
        documents=internal_doc_manager.list_documents()
return{"documents":documents}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao listar documentos internos: {str(e)}")

@app.post("/internal-documents/add")
asyncdefadd_internal_document(file:UploadFile=File(...)):
    """Adiciona um documento à pasta interna"""
try:

        allowed_types=["application/pdf","text/plain","text/markdown",
"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
"application/rtf"]
iffile.content_typenotinallowed_types:
            raiseHTTPException(status_code=400,detail="Tipo de arquivo não suportado")

temp_path=f"temp_{file.filename}"
withopen(temp_path,"wb")asbuffer:
            content=awaitfile.read()
buffer.write(content)

success=internal_doc_manager.add_document(temp_path,file.filename)

os.remove(temp_path)

ifsuccess:

            doc_content=internal_doc_manager.get_document_content(file.filename)
ifdoc_content:

                chunks=document_processor.split_text(doc_content)
vector_store.add_documents(chunks,[file.filename]*len(chunks))
internal_doc_manager.mark_as_processed(file.filename,True)

return{
"message":"Documento interno adicionado com sucesso",
"filename":file.filename,
"content_type":file.content_type
}
else:
            raiseHTTPException(status_code=400,detail="Erro ao adicionar documento interno")

exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao adicionar documento interno: {str(e)}")

@app.delete("/internal-documents/{filename}")
asyncdefremove_internal_document(filename:str):
    """Remove um documento interno"""
try:
        success=internal_doc_manager.remove_document(filename)
ifsuccess:

            vector_store.delete_document_by_filename(filename)
return{"message":f"Documento interno {filename} removido com sucesso"}
else:
            raiseHTTPException(status_code=404,detail="Documento interno não encontrado")
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao remover documento interno: {str(e)}")

@app.get("/internal-documents/statistics")
asyncdefget_internal_documents_statistics():
    """Retorna estatísticas dos documentos internos"""
try:
        stats=internal_doc_manager.get_statistics()
vector_stats=vector_store.get_statistics()

return{
"internal_documents":stats,
"vector_store":vector_stats
}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter estatísticas: {str(e)}")

@app.get("/internal-documents/categories")
asyncdefget_document_categories():
    """Retorna categorias de documentos disponíveis"""
try:
        stats=internal_doc_manager.get_statistics()
return{"categories":stats.get("categories",{})}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter categorias: {str(e)}")

@app.get("/internal-documents/category/{category}")
asyncdefget_documents_by_category(category:str):
    """Retorna documentos de uma categoria específica"""
try:
        documents=internal_doc_manager.get_documents_by_category(category)
return{"category":category,"documents":documents}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao buscar documentos por categoria: {str(e)}")

@app.post("/feedback")
asyncdefrecord_feedback(feedback:FeedbackRequest):
    """Registra feedback do usuário"""
try:
        success=chat_manager.record_user_feedback(
session_id=feedback.session_id,
question=feedback.question,
response=feedback.response,
satisfaction=feedback.satisfaction,
feedback_text=feedback.feedback_text
)

ifsuccess:
            return{"message":"Feedback registrado com sucesso"}
else:
            raiseHTTPException(status_code=400,detail="Erro ao registrar feedback")
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao registrar feedback: {str(e)}")

@app.get("/learning/stats",response_model=LearningStats)
asyncdefget_learning_stats():
    """Retorna estatísticas de aprendizado"""
try:
        stats=chat_manager.get_learning_stats()
returnLearningStats(**stats)
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter estatísticas de aprendizado: {str(e)}")

@app.get("/learning/suggestions")
asyncdefget_suggested_questions(limit:int=5):
    """Retorna perguntas sugeridas baseadas no aprendizado"""
try:
        suggestions=chat_manager.get_suggested_questions(limit)
return{"suggested_questions":suggestions}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter sugestões: {str(e)}")

@app.get("/performance/stats")
asyncdefget_performance_stats():
    """Retorna estatísticas de performance do sistema"""
try:
        cache_stats=chat_manager.get_cache_stats()
vector_stats=vector_store.get_statistics()

return{
"cache_stats":cache_stats,
"vector_store_stats":vector_stats,
"system_optimized":True
}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter estatísticas de performance: {str(e)}")

@app.post("/cache/clear")
asyncdefclear_cache():
    """Limpa todos os caches do sistema"""
try:
        chat_manager.clear_cache()
vector_store.clear_cache()
return{"message":"Cache limpo com sucesso"}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao limpar cache: {str(e)}")

@app.get("/cache/stats")
asyncdefget_cache_stats():
    """Retorna estatísticas detalhadas do cache"""
try:
        chat_cache_stats=chat_manager.get_cache_stats()
vector_cache_stats=vector_store.get_cache_stats()

return{
"chat_manager_cache":chat_cache_stats,
"vector_store_cache":vector_cache_stats
}
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao obter estatísticas do cache: {str(e)}")

@app.post("/system/rebuild-index")
asyncdefrebuild_vector_index():
    """Reconstrói o índice vetorial para otimizar buscas"""
try:
        success=vector_store.rebuild_index()
ifsuccess:
            return{"message":"Índice vetorial reconstruído com sucesso"}
else:
            raiseHTTPException(status_code=500,detail="Erro ao reconstruir índice")
exceptExceptionase:
        raiseHTTPException(status_code=500,detail=f"Erro ao reconstruir índice: {str(e)}")

if__name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
