
importasyncio
importtime
fromtypingimportDict,List,Any,Optional,Tuple
importlogging
frompathlibimportPath

from.multi_model_nlp_processorimportMultiModelNLPProcessor
from.intelligent_cache_managerimportIntelligentCacheManager,cache_manager
from.adaptive_feedback_systemimportAdaptiveFeedbackSystem,adaptive_feedback_system
from.humanized_response_generatorimportHumanizedResponseGenerator,humanized_response_generator
from.performance_optimizer_liteimportPerformanceOptimizer,performance_optimizer

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

classIntegratedChatbotSystem:
    """Sistema integrado que combina todos os mdulos de melhoria"""

def__init__(self,data_dir:str="./learning_data"):
        self.data_dir=Path(data_dir)
self.data_dir.mkdir(exist_ok=True)

logger.info(" Inicializando Sistema Integrado de Chatbot...")

self.nlp_processor=MultiModelNLPProcessor()
logger.info(" Sistema NLP Multi-Modelo inicializado")

self.cache_manager=cache_manager
logger.info(" Sistema de Cache Inteligente inicializado")

self.feedback_system=adaptive_feedback_system
logger.info(" Sistema de Feedback Adaptativo inicializado")

self.response_generator=humanized_response_generator
logger.info(" Gerador de Respostas Humanizadas inicializado")

self.performance_optimizer=performance_optimizer
logger.info(" Otimizador de Performance inicializado")

self.system_stats={
"startup_time":time.time(),
"total_requests":0,
"successful_requests":0,
"failed_requests":0,
"average_response_time":0.0,
"cache_hit_rate":0.0
}

logger.info(" Sistema Integrado inicializado com sucesso!")

@performance_optimizer.optimize_function(cache_size=256,timeout=30.0)
asyncdefprocess_message_advanced(self,message:str,session_id:Optional[str]=None,
context:Optional[Dict[str,Any]]=None)->Dict[str,Any]:
        """Processa mensagem usando todos os sistemas integrados"""
start_time=time.time()

try:

            nlp_analysis=awaitself._analyze_message_with_nlp(message)

relevant_content=awaitself._search_with_intelligent_cache(message,nlp_analysis)

response=awaitself._generate_humanized_response(message,relevant_content,nlp_analysis,context)

improved_response=awaitself._apply_feedback_improvements(message,response,nlp_analysis)

response_time=time.time()-start_time
self._update_system_stats(response_time,True)

return{
"response":improved_response,
"session_id":session_id,
"timestamp":time.time(),
"sources":relevant_content.get("sources",[]),
"nlp_analysis":nlp_analysis,
"response_time":response_time,
"cache_hit":relevant_content.get("cache_hit",False),
"improvements_applied":improved_response!=response
}

exceptExceptionase:
            logger.error(f"Erro no processamento avanado: {e}")
response_time=time.time()-start_time
self._update_system_stats(response_time,False)

return{
"response":"Desculpe, ocorreu um erro interno. Tente novamente.",
"session_id":session_id,
"timestamp":time.time(),
"sources":[],
"error":str(e),
"response_time":response_time
}

asyncdef_analyze_message_with_nlp(self,message:str)->Dict[str,Any]:
        """Analisa mensagem usando mltiplos modelos NLP"""
try:

            cache_key=f"nlp_analysis_{hash(message)}"
cached_analysis=self.cache_manager.get(cache_key)

ifcached_analysis:
                returncached_analysis

analysis={
"entities":self.nlp_processor.extract_entities_advanced(message),
"sentiment":self.nlp_processor.analyze_sentiment_advanced(message),
"category":self.nlp_processor.categorize_question_advanced(message),
"similarity_scores":{},
"keywords":[]
}

formodel_nameinself.nlp_processor.models:
                ifself.nlp_processor.models[model_name]isnotNone:
                    try:

                        reference_question="Qual o horrio de trabalho?"
similarity=self.nlp_processor.calculate_semantic_similarity(
message,reference_question,model_name
)
analysis["similarity_scores"][model_name]=similarity
exceptExceptionase:
                        logger.warning(f"Erro ao calcular similaridade com {model_name}: {e}")

try:
                keywords=self.nlp_processor.extract_keywords_advanced(message,max_keywords=5)
analysis["keywords"]=[kw[0]forkwinkeywords]
exceptExceptionase:
                logger.warning(f"Erro ao extrair palavras-chave: {e}")

self.cache_manager.set(cache_key,analysis,ttl=3600,tags=["nlp_analysis"])

returnanalysis

exceptExceptionase:
            logger.error(f"Erro na anlise NLP: {e}")
return{
"entities":{},
"sentiment":{"combined":{"sentiment":"neutral","polarity":0.0}},
"category":("geral",0.1),
"similarity_scores":{},
"keywords":[]
}

asyncdef_search_with_intelligent_cache(self,message:str,nlp_analysis:Dict[str,Any])->Dict[str,Any]:
        """Busca contedo usando cache inteligente"""
try:

            cache_key=f"search_{hash(message)}_{hash(str(nlp_analysis.get('category','geral')))}"

cached_result=self.cache_manager.get(cache_key)
ifcached_result:
                cached_result["cache_hit"]=True
returncached_result

category,confidence=nlp_analysis.get("category",("geral",0.1))

content_templates={
"horario":"Horrio de trabalho: Segunda a sexta, 8h s 18h. Intervalo: 12h s 13h.",
"beneficios":"Benefcios: Vale refeio R$ 25/dia, plano de sade, gympass.",
"ferias":"Frias: 30 dias por ano, 1/3 adicional constitucional.",
"licenca":"Licena mdica: Atestado obrigatrio a partir do 3 dia.",
"vestimenta":"Cdigo de vestimenta: Traje social segunda a quinta, casual sexta.",
"comunicacao":"Comunicao: Email corporativo, WhatsApp, Slack disponveis.",
"seguranca":"Segurana: Carto de acesso obrigatrio, no compartilhar senhas.",
"limpeza":"Limpeza: Manter mesa organizada, participar da limpeza da copa.",
"treinamento":"Treinamento: Cursos online, workshops mensais disponveis.",
"rh":"RH: Contato rh@empresa.com para dvidas trabalhistas."
}

content=content_templates.get(category,"Informao geral disponvel nos documentos.")

result={
"content":content,
"sources":[f"manual_{category}.pdf"],
"category":category,
"confidence":confidence,
"cache_hit":False
}

self.cache_manager.set(cache_key,result,ttl=1800,tags=["search",category])

returnresult

exceptExceptionase:
            logger.error(f"Erro na busca com cache: {e}")
return{
"content":"No foi possvel encontrar informaes relevantes.",
"sources":[],
"cache_hit":False
}

asyncdef_generate_humanized_response(self,message:str,relevant_content:Dict[str,Any],
nlp_analysis:Dict[str,Any],context:Optional[Dict[str,Any]])->str:
        """Gera resposta humanizada"""
try:
            content=relevant_content.get("content","")
category=relevant_content.get("category","geral")

session_context={
"user_name":context.get("user_name")ifcontextelseNone,
"session_count":context.get("session_count",0)ifcontextelse0,
"last_interaction":context.get("last_interaction")ifcontextelseNone
}

response=self.response_generator.generate_humanized_response(
question=message,
content=content,
category=category,
session_context=session_context
)

returnresponse

exceptExceptionase:
            logger.error(f"Erro na gerao de resposta humanizada: {e}")
returnrelevant_content.get("content","Desculpe, no consegui processar sua pergunta.")

asyncdef_apply_feedback_improvements(self,message:str,response:str,
nlp_analysis:Dict[str,Any])->str:
        """Aplica melhorias baseadas no feedback"""
try:
            category,confidence=nlp_analysis.get("category",("geral",0.1))

improved_response=self.feedback_system.get_improved_response(
question=message,
original_response=response,
category=category
)

returnimproved_response

exceptExceptionase:
            logger.error(f"Erro ao aplicar melhorias de feedback: {e}")
returnresponse

defrecord_feedback(self,session_id:str,question:str,response:str,
satisfaction:int,feedback_text:Optional[str]=None)->str:
        """Registra feedback do usurio"""
try:

            category,_=self.nlp_processor.categorize_question_advanced(question)

feedback_id=self.feedback_system.record_feedback(
session_id=session_id,
question=question,
response=response,
satisfaction=satisfaction,
feedback_text=feedback_text,
category=category
)

returnfeedback_id

exceptExceptionase:
            logger.error(f"Erro ao registrar feedback: {e}")
return""

def_update_system_stats(self,response_time:float,success:bool):
        """Atualiza estatsticas do sistema"""
self.system_stats["total_requests"]+=1

ifsuccess:
            self.system_stats["successful_requests"]+=1
else:
            self.system_stats["failed_requests"]+=1

total_requests=self.system_stats["total_requests"]
current_avg=self.system_stats["average_response_time"]
self.system_stats["average_response_time"]=(
(current_avg*(total_requests-1)+response_time)/total_requests
)

cache_stats=self.cache_manager.get_stats()
self.system_stats["cache_hit_rate"]=cache_stats.get("hit_rate",0.0)

defget_system_status(self)->Dict[str,Any]:
        """Retorna status completo do sistema"""
try:

            nlp_status=self.nlp_processor.get_model_status()
cache_stats=self.cache_manager.get_stats()
feedback_insights=self.feedback_system.get_learning_insights()
template_stats=self.response_generator.get_template_statistics()
performance_health=self.performance_optimizer.check_system_health()

return{
"system_stats":self.system_stats,
"nlp_models":nlp_status,
"cache":cache_stats,
"feedback_insights":feedback_insights,
"response_templates":template_stats,
"performance_health":performance_health,
"uptime":time.time()-self.system_stats["startup_time"],
"timestamp":time.time()
}

exceptExceptionase:
            logger.error(f"Erro ao obter status do sistema: {e}")
return{
"error":str(e),
"timestamp":time.time()
}

defoptimize_system(self):
        """Executa otimizaes do sistema"""
try:
            logger.info(" Iniciando otimizao do sistema...")

self.cache_manager.optimize()
logger.info(" Cache otimizado")

self.response_generator.optimize_templates()
logger.info(" Templates otimizados")

self.feedback_system.cleanup_old_data(days=90)
logger.info(" Dados antigos de feedback removidos")

self.performance_optimizer.optimize_memory()
logger.info(" Memria otimizada")

logger.info(" Otimizao do sistema concluda!")

exceptExceptionase:
            logger.error(f"Erro na otimizao do sistema: {e}")

defexport_system_data(self,output_dir:str):
        """Exporta dados do sistema"""
try:
            output_path=Path(output_dir)
output_path.mkdir(exist_ok=True)

feedback_file=output_path/"feedback_data.json"
self.feedback_system.export_learning_data(str(feedback_file))

templates_file=output_path/"response_templates.json"
importjson
withopen(templates_file,'w',encoding='utf-8')asf:
                json.dump(self.response_generator.response_templates,f,ensure_ascii=False,indent=2,default=str)

stats_file=output_path/"system_statistics.json"
withopen(stats_file,'w',encoding='utf-8')asf:
                json.dump(self.get_system_status(),f,ensure_ascii=False,indent=2,default=str)

logger.info(f" Dados do sistema exportados para: {output_dir}")

exceptExceptionase:
            logger.error(f"Erro ao exportar dados do sistema: {e}")

defshutdown(self):
        """Encerra o sistema integrado"""
try:
            logger.info(" Encerrando sistema integrado...")

self.cache_manager.save_cache()
self.nlp_processor.save_cache()

self.performance_optimizer.shutdown()

logger.info(" Sistema integrado encerrado com sucesso")

exceptExceptionase:
            logger.error(f"Erro ao encerrar sistema: {e}")

integrated_system=IntegratedChatbotSystem()
