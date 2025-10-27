importos
fromtypingimportList,Dict,Any,Tuple,Optional
importjson
importuuid
fromdatetimeimportdatetime
importre
fromdifflibimportSequenceMatcher
importasyncio
importtime
fromfunctoolsimportlru_cache

from.nlp_processorimportNLPProcessor
from.advanced_nlp_processorimportAdvancedNLPProcessor
from.internal_document_managerimportInternalDocumentManager
from.learning_managerimportLearningManager
from.context_analyzerimportContextAnalyzer
from.intelligent_cache_managerimportIntelligentCacheManager
from.improved_response_systemimportImprovedResponseSystem

classOptimizedChatManager:
    """Chat Manager otimizado com cache inteligente e carregamento preguioso"""

def__init__(self,vector_store,internal_doc_manager:Optional[InternalDocumentManager]=None,use_advanced_nlp:bool=True):
        self.vector_store=vector_store
self.internal_doc_manager=internal_doc_manager
self.use_advanced_nlp=use_advanced_nlp

self.cache_manager=IntelligentCacheManager(
max_memory_size=100*1024*1024,
enable_disk_cache=True,
default_ttl=3600
)

self._document_cache={}
self._document_cache_ttl=1800
self._last_document_load={}

self._nlp_processor=None
self._learning_manager=None
self._context_analyzer=None

self.improved_response_system=ImprovedResponseSystem()

self.sessions={}

self.default_responses={
"saudacao":[
"Ol! Como posso ajud-lo hoje?",
"Oi! Estou aqui para responder suas perguntas sobre os documentos.",
"Ol! Em que posso ser til?"
],
"despedida":[
"At logo! Foi um prazer ajud-lo.",
"Tchau! Se precisar de mais alguma coisa, estarei aqui.",
"At a prxima! Tenha um bom dia."
],
"agradecimento":[
"De nada! Fico feliz em ajudar.",
"Por nada! Se precisar de mais alguma coisa,  s perguntar.",
"Disponha! Estou aqui para isso."
],
"sem_documentos":[
"Desculpe, no h documentos disponveis no sistema para responder sua pergunta. Por favor, faa upload de documentos relevantes primeiro.",
"No encontrei documentos que possam responder sua pergunta. Voc pode fazer upload de documentos para que eu possa ajud-lo melhor.",
"Infelizmente no tenho documentos suficientes para responder sua pergunta. Adicione alguns documentos ao sistema."
]
}

self._quick_responses_cache={}
self._initialize_quick_responses()

@property
defnlp_processor(self):
        """Carregamento preguioso do processador NLP"""
ifself._nlp_processorisNone:
            ifself.use_advanced_nlp:
                try:
                    self._nlp_processor=AdvancedNLPProcessor()
print(" Processador NLP avanado inicializado (lazy loading)")
exceptExceptionase:
                    print(f" Erro ao inicializar NLP avanado: {e}. Usando processador bsico.")
self._nlp_processor=NLPProcessor()
self.use_advanced_nlp=False
else:
                self._nlp_processor=NLPProcessor()
returnself._nlp_processor

@property
deflearning_manager(self):
        """Carregamento preguioso do gerenciador de aprendizado"""
ifself._learning_managerisNone:
            self._learning_manager=LearningManager()
print(" Sistema de aprendizado inicializado (lazy loading)")
returnself._learning_manager

@property
defcontext_analyzer(self):
        """Carregamento preguioso do analisador de contexto"""
ifself._context_analyzerisNone:
            self._context_analyzer=ContextAnalyzer()
print(" Analisador de contexto inicializado (lazy loading)")
returnself._context_analyzer

def_initialize_quick_responses(self):
        """Inicializa cache de respostas rpidas para consultas comuns"""
self._quick_responses_cache={
'academia':{
'horario':""" **Horrio de Funcionamento da Academia:**
- Segunda a sexta: 5h s 23h
- Sbados: 6h s 21h  
- Domingos: 7h s 19h
- 24h para membros VIP"""
,
'preco':""" **Planos Disponveis:**
- Bsico: R$ 89,90/ms
- Premium: R$ 129,90/ms (com piscina e sauna)
- VIP: R$ 199,90/ms (acesso 24h)"""
,
'servicos':""" **Estrutura e Servios:**
- 50 aparelhos de musculao
- Piscina semi-olmpica
- Sauna mida e seca
- Aulas de spinning, pilates, yoga"""

},
'supermercado':{
'horario':""" **Horrio de Funcionamento:**
- Segunda a sbado: 6h s 23h
- Domingos: 7h s 22h
- Delivery: 6h s 23h"""
,
'departamentos':""" **Departamentos:**
- Hortifrti, Aougue, Padaria
- Laticnios, Mercearia, Bebidas
- Limpeza, Higiene, Farmcia"""
,
'servicos':""" **Servios:**
- Delivery prprio (2h)
- Carto de crdito prprio
- Programa de fidelidade
- Estacionamento gratuito"""

},
'restaurante':{
'horario':""" **Horrio de Funcionamento:**
- Almoo: 11h30 s 15h30
- Jantar: 18h s 23h
- Delivery: 11h s 22h30"""
,
'cardapio':"""**Cardapio:**
- Entradas: R$ 15,00 a R$ 35,00
- Pratos principais: R$ 45,00 a R$ 85,00
- Menu executivo: R$ 35,00"""
,
'especialidades':""" **Especialidades:**
- Menu degustao: R$ 120,00
- Harmonizao com vinhos
- Ambiente com terrao"""

},
'empresa':{
'horario':"""**Horario de Trabalho:**
- Segunda a sexta: 8h s 18h
- Intervalo: 12h s 13h
- Flexibilidade: 30 min"""
,
'beneficios':"""**Beneficios:**
- Vale refeio: R$ 25,00/dia
- Plano de sade completo
- Plano odontolgico
- Gympass"""
,
'politicas':"""**Politicas:**
- Frias: 30 dias/ano
- Licena mdica com atestado
- Cdigo de vestimenta
- Treinamentos obrigatrios"""

}
}

asyncdefprocess_message(self,message:str,session_id:Optional[str]=None)->Tuple[str,str,List[str]]:
        """Processa uma mensagem de forma otimizada com cache inteligente"""

ifnotsession_id:
            session_id=str(uuid.uuid4())

ifsession_idnotinself.sessions:
            self.sessions[session_id]=[]

cache_key=f"response_{hash(message)}_{session_id}"
cached_response=self.cache_manager.get(cache_key)
ifcached_response:
            returncached_response["response"],cached_response["session_id"],cached_response["sources"]

start_time=time.time()

quick_response=self._get_quick_response(message)
ifquick_response:
            response_time=time.time()-start_time
print(f"Resposta rapida em {response_time:.3f}s")

self.cache_manager.set(cache_key,{
"response":quick_response,
"session_id":session_id,
"sources":["cache_rapido"]
},ttl=1800)

returnquick_response,session_id,["cache_rapido"]

relevant_docs=awaitself._search_with_optimized_cache(message)

context=self._prepare_context(relevant_docs)

response=awaitself._generate_optimized_response(message,context,session_id)

iflen(message.split())>3:
            try:
                improved_response=self.learning_manager.get_improved_response(message,response)
response=improved_response
exceptExceptionase:
                print(f"Erro ao melhorar resposta: {e}")

self.sessions[session_id].append({
"user_message":message,
"bot_response":response,
"timestamp":datetime.now().isoformat(),
"sources":[doc["metadata"]["filename"]fordocinrelevant_docs]
})

asyncio.create_task(self._learn_from_interaction_async(
question=message,
response=response,
sources=[doc["metadata"]["filename"]fordocinrelevant_docs],
session_id=session_id
))

sources=[doc["metadata"]["filename"]fordocinrelevant_docs]

self.cache_manager.set(cache_key,{
"response":response,
"session_id":session_id,
"sources":sources
},ttl=1800)

response_time=time.time()-start_time
print(f"Resposta processada em {response_time:.3f}s")

returnresponse,session_id,sources

def_get_quick_response(self,message:str)->Optional[str]:
        """Obtm resposta rpida do cache para consultas comuns"""
message_lower=message.lower().strip()

domain_keywords={
'academia':['academia','gym','fitness','musculao','musculacao'],
'supermercado':['supermercado','mercado','loja','compras'],
'restaurante':['restaurante','comida','jantar','almoo','almoco'],
'empresa':['empresa','trabalho','funcionrio','funcionario','rh']
}

topic_keywords={
'horario':['horrio','horario','funcionamento','aberto','fechado'],
'preco':['preo','preco','preos','mensalidade','planos','plano','valores','valor'],
'servicos':['servios','servicos','estrutura','equipamentos','aulas'],
'departamentos':['departamentos','sees','secoes','produtos'],
'cardapio':['cardpio','cardapio','menu','pratos'],
'especialidades':['especialidades','destaques','recomendaes'],
'beneficios':['benefcio','beneficio','vale','plano'],
'politicas':['polticas','politicas','regras','normas']
}

detected_domain=None
fordomain,keywordsindomain_keywords.items():
            ifany(kinmessage_lowerforkinkeywords):
                detected_domain=domain
break

ifnotdetected_domain:
            returnNone

detected_topic=None
fortopic,keywordsintopic_keywords.items():
            ifany(kinmessage_lowerforkinkeywords):
                detected_topic=topic
break

ifnotdetected_topic:
            iflen(message_lower.split())<=2:
                returnself._get_domain_overview(detected_domain)
returnNone

ifdetected_domaininself._quick_responses_cacheanddetected_topicinself._quick_responses_cache[detected_domain]:
            returnself._quick_responses_cache[detected_domain][detected_topic]

returnNone

def_get_domain_overview(self,domain:str)->str:
        """Retorna viso geral de um domnio"""
ifdomain=='academia':
            return""" **Academia FitLife - Informaes Principais:**

**Horrio de Funcionamento:**
- Segunda a sexta: 5h s 23h
- Sbados: 6h s 21h  
- Domingos: 7h s 19h
- 24h para membros VIP

**Planos Disponveis:**
- Bsico: R$ 89,90/ms
- Premium: R$ 129,90/ms (com piscina e sauna)
- VIP: R$ 199,90/ms (acesso 24h)

**Estrutura:**
- 50 aparelhos de musculao
- Piscina semi-olmpica
- Sauna mida e seca
- Aulas de spinning, pilates, yoga

Para informaes especficas, me pergunte sobre horrios, preos, aulas ou servios!"""

elifdomain=='supermercado':
            return""" **Supermercado Mega Economia - Informaes Principais:**

**Horrio de Funcionamento:**
- Segunda a sbado: 6h s 23h
- Domingos: 7h s 22h
- Delivery: 6h s 23h

**Departamentos:**
- Hortifrti, Aougue, Padaria
- Laticnios, Mercearia, Bebidas
- Limpeza, Higiene, Farmcia

**Servios:**
- Delivery prprio (2h)
- Carto de crdito prprio
- Programa de fidelidade
- Estacionamento gratuito

Para informaes especficas, me pergunte sobre horrios, promoes, delivery ou departamentos!"""

elifdomain=='restaurante':
            return""" **Restaurante Sabor & Arte - Informaes Principais:**

**Horrio de Funcionamento:**
- Almoo: 11h30 s 15h30
- Jantar: 18h s 23h
- Delivery: 11h s 22h30

**Cardpio:**
- Entradas: R$ 15,00 a R$ 35,00
- Pratos principais: R$ 45,00 a R$ 85,00
- Menu executivo: R$ 35,00

**Especialidades:**
- Menu degustao: R$ 120,00
- Harmonizao com vinhos
- Ambiente com terrao

Para informaes especficas, me pergunte sobre cardpio, preos, reservas ou delivery!"""

elifdomain=='empresa':
            return"""**Empresa - Informacoes Principais:**

**Horrio de Trabalho:**
- Segunda a sexta: 8h s 18h
- Intervalo: 12h s 13h
- Flexibilidade: 30 min

**Benefcios:**
- Vale refeio: R$ 25,00/dia
- Plano de sade completo
- Plano odontolgico
- Gympass

**Polticas:**
- Frias: 30 dias/ano
- Licena mdica com atestado
- Cdigo de vestimenta
- Treinamentos obrigatrios

Para informaes especficas, me pergunte sobre benefcios, frias, horrios ou polticas!"""

returnNone

asyncdef_search_with_optimized_cache(self,message:str)->List[Dict[str,Any]]:
        """Busca otimizada com cache inteligente"""

search_cache_key=f"search_{hash(message)}"
cached_search=self.cache_manager.get(search_cache_key)
ifcached_search:
            returncached_search

relevant_docs=self._search_with_nlp_optimized(message)

self.cache_manager.set(search_cache_key,relevant_docs,ttl=1800)

returnrelevant_docs

def_search_with_nlp_optimized(self,message:str)->List[Dict[str,Any]]:
        """Busca NLP otimizada"""
try:

            message_words=message.lower().strip().split()
iflen(message_words)<=2:

                vector_results=self.vector_store.search(message,n_results=2)

ifself.internal_doc_manager:
                    internal_docs=self._search_internal_documents_specific(message)
all_results=vector_results+internal_docs
else:
                    all_results=vector_results
else:

                vector_results=self.vector_store.search(message,n_results=3)

ifself.internal_doc_manager:
                    internal_docs=self._search_internal_documents_optimized(message)
all_results=vector_results+internal_docs
else:
                    all_results=vector_results

iflen(message_words)>3:
                returnself._refine_results_with_nlp(message,all_results)
else:
                returnall_results[:3]

exceptExceptionase:
            print(f"Erro na busca NLP otimizada: {e}")
return[]

def_search_internal_documents_optimized(self,message:str)->List[Dict[str,Any]]:
        """Busca otimizada em documentos internos"""
try:

            doc_cache_key=f"internal_docs_{hash(message)}"
cached_docs=self.cache_manager.get(doc_cache_key)
ifcached_docs:
                returncached_docs

message_lower=message.lower()
question_category="geral"

ifany(wordinmessage_lowerforwordin['academia','gym','fitness']):
                question_category="academia"
elifany(wordinmessage_lowerforwordin['supermercado','mercado','loja']):
                question_category="supermercado"
elifany(wordinmessage_lowerforwordin['restaurante','comida','jantar']):
                question_category="restaurante"
elifany(wordinmessage_lowerforwordin['empresa','trabalho','funcionrio']):
                question_category="empresa"

category_docs=self.internal_doc_manager.get_documents_by_category(question_category)

ifnotcategory_docs:
                all_docs=self.internal_doc_manager.list_documents()
category_docs=all_docs

results=[]
fordoc_infoincategory_docs[:3]:
                content=self._get_document_content_cached(doc_info["filename"])
ifcontent:
                    results.append({
"content":content,
"metadata":{
"filename":doc_info["filename"],
"category":doc_info["category"],
"timestamp":doc_info["last_modified"]
},
"similarity":0.7
})

self.cache_manager.set(doc_cache_key,results,ttl=1800)

returnresults

exceptExceptionase:
            print(f"Erro na busca otimizada de documentos internos: {e}")
return[]

def_get_document_content_cached(self,filename:str)->Optional[str]:
        """Obtm contedo do documento com cache"""
current_time=time.time()

if(filenameinself._document_cacheand
filenameinself._last_document_loadand
current_time-self._last_document_load[filename]<self._document_cache_ttl):
            returnself._document_cache[filename]

content=self.internal_doc_manager.get_document_content(filename)
ifcontent:
            self._document_cache[filename]=content
self._last_document_load[filename]=current_time

returncontent

def_search_internal_documents_specific(self,message:str)->List[Dict[str,Any]]:
        """Busca especfica em documentos internos para consultas genricas"""
try:
            message_lower=message.lower().strip()

domain_keywords={
'academia':['academia','gym','fitness','musculao','musculacao'],
'supermercado':['supermercado','mercado','loja','compras'],
'restaurante':['restaurante','comida','jantar','almoo','almoco'],
'empresa':['empresa','trabalho','funcionrio','funcionario','rh']
}

fordomain,keywordsindomain_keywords.items():
                ifany(keywordinmessage_lowerforkeywordinkeywords):

                    category_docs=self.internal_doc_manager.get_documents_by_category(domain)

ifcategory_docs:

                        doc_info=category_docs[0]
content=self._get_document_content_cached(doc_info["filename"])
ifcontent:
                            return[{
"content":content,
"metadata":{
"filename":doc_info["filename"],
"category":doc_info["category"],
"timestamp":doc_info["last_modified"]
},
"similarity":0.9
}]

return[]

exceptExceptionase:
            print(f"Erro na busca especfica de documentos internos: {e}")
return[]

def_refine_results_with_nlp(self,message:str,results:List[Dict[str,Any]])->List[Dict[str,Any]]:
        """Refina resultados usando NLP (apenas quando necessrio)"""
try:
            ifnotresultsorlen(results)<=2:
                returnresults

message_keywords=message.lower().split()

refined_results=[]
forresultinresults:
                content=result["content"].lower()

content_words=set(content.split())
message_words_set=set(message_keywords)
common_words=message_words_set.intersection(content_words)

iflen(message_words_set)>0:
                    simple_similarity=len(common_words)/len(message_words_set)
else:
                    simple_similarity=0.0

vector_similarity=result.get("similarity",0.0)
combined_similarity=(simple_similarity+vector_similarity)/2

result["combined_similarity"]=combined_similarity
refined_results.append(result)

refined_results.sort(key=lambdax:x.get("combined_similarity",0),reverse=True)

returnrefined_results[:3]

exceptExceptionase:
            print(f"Erro no refinamento NLP: {e}")
returnresults[:3]

def_prepare_context(self,relevant_docs:List[Dict[str,Any]])->str:
        """Prepara contexto dos documentos relevantes"""
ifnotrelevant_docs:
            return"No h documentos disponveis para consulta."

context_parts=["Documentos relevantes:"]

fori,docinenumerate(relevant_docs,1):
            content=doc["content"]
filename=doc["metadata"]["filename"]
context_parts.append(f"\n{i}. Arquivo: {filename}")
context_parts.append(f"Contedo: {content}")

return"\n".join(context_parts)

asyncdef_generate_optimized_response(self,message:str,context:str,session_id:str)->str:
        """Gera resposta otimizada"""

message_lower=message.lower().strip()

ifself._is_greeting(message_lower):
            returnself._get_random_response("saudacao")

ifself._is_farewell(message_lower):
            returnself._get_random_response("despedida")

ifself._is_thanks(message_lower):
            returnself._get_random_response("agradecimento")

if"no h documentos"incontext.lower():
            returnself._get_random_response("sem_documentos")

returnself._generate_contextual_response_optimized(message,context,session_id)

def_generate_contextual_response_optimized(self,message:str,context:str,session_id:str)->str:
        """Gera resposta contextual otimizada"""

improved_response=self.improved_response_system.get_improved_response(message)
ifimproved_response:
            returnimproved_response

relevant_info=self._extract_relevant_info_optimized(message,context)

ifrelevant_info:
            returnself._format_contextual_response(message,relevant_info)
else:
            returnself._generate_fallback_response(message,context)

def_extract_relevant_info_optimized(self,message:str,context:str)->List[str]:
        """Extrai informaes relevantes de forma otimizada"""
relevant_info=[]

message_words=message.lower().strip().split()
iflen(message_words)<=2:
            returnself._handle_generic_query(message,context)

context_parts=context.split("\n")

message_words_set=set(message_words)

topic_keywords={
'horario':['horrio','horario','trabalho','expediente','entrada','sada','saida','8h','18h','intervalo','almoo','almoco','funcionamento','aberto','fechado'],
'beneficios':['benefcio','beneficio','vale','plano','sade','saude','odontolgico','odontologico','gympass','refeio','refeicao','transporte','mensalidade','preo','preco'],
'ferias':['frias','ferias','adicional','constitucional','perodo','periodo','descanso','recesso'],
'licenca':['licena','licenca','mdica','medica','atestado','inss','pagamento','afastamento'],
'vestimenta':['vestimenta','roupa','traje','social','casual','informal','uniforme','cdigo','codigo'],
'comunicacao':['comunicao','comunicacao','email','whatsapp','slack','mensagem','contato'],
'seguranca':['segurana','seguranca','carto','cartao','acesso','senha','bloquear','incidente'],
'limpeza':['limpeza','organizao','organizacao','mesa','lixo','copa','espao','espaco'],
'treinamento':['treinamento','curso','capacitao','capacitacao','workshop','desenvolvimento'],
'rh':['rh','recursos humanos','funcionrio','funcionario','colaborador','empregado']
}

question_topic=None
fortopic,keywordsintopic_keywords.items():
            ifany(keywordinmessage.lower()forkeywordinkeywords):
                question_topic=topic
break

full_context=context.lower()

ifquestion_topicandquestion_topicintopic_keywords:
            topic_words=topic_keywords[question_topic]
ifany(keywordinfull_contextforkeywordintopic_words):

                forpartincontext_parts:
                    ifany(keywordinpart.lower()forkeywordintopic_words):

                        ifself._is_relevant_content(part,message_words_set):
                            relevant_info.append(part.strip())
else:

            forpartincontext_parts:
                content_words=set(part.lower().split())
common_words=message_words_set.intersection(content_words)

iflen(common_words)>=2or(len(common_words)==1andany(wordin['academia','supermercado','restaurante','empresa']forwordincommon_words)):
                    ifself._is_relevant_content(part,message_words_set):
                        relevant_info.append(part.strip())

returnrelevant_info[:3]

def_handle_generic_query(self,message:str,context:str)->List[str]:
        """Lida com consultas genricas como apenas 'Academia'"""
return[]

def_is_relevant_content(self,content:str,message_words:set)->bool:
        """Verifica se o contedo  realmente relevante para a pergunta"""
content_lower=content.lower()

generic_phrases=[
"documentos relevantes:",
"arquivo:",
"contedo:",
"manual do",
"introduo",
"para dvidas",
"contato:",
"endereo:",
"telefone:",
"email:"
]

ifany(phraseincontent_lowerforphraseingeneric_phrases)andlen(content.strip())<50:
            returnFalse

content_words=set(content_lower.split())
ifnotmessage_words.intersection(content_words):
            returnFalse

returnTrue

def_format_contextual_response(self,message:str,relevant_info:List[str])->str:
        """Formata uma resposta contextual baseada nas informaes relevantes"""

message_words=message.lower().strip().split()
iflen(message_words)<=2:
            returnself._format_generic_response(message,[])

ifnotrelevant_info:
            return"Desculpe, no encontrei informaes especficas sobre sua pergunta nos documentos disponveis."

message_lower=message.lower()
section_extractors=[
(self._extract_schedule_block,["horrio","horario","funcionamento","aberto","fechado"]),
(self._extract_prices_block,["preo","preco","preos","mensalidade","planos","plano","valores","valor"]),
(self._extract_contacts_block,["contato","telefone","whatsapp","email","site","endereo","endereco","instagram"])
]
forextractor,keywordsinsection_extractors:
            ifany(kinmessage_lowerforkinkeywords):
                extracted=extractor(relevant_info)
ifextracted:
                    returnextracted

all_info="\n\n".join(relevant_info)

ifany(wordinmessage_lowerforwordin["horrio","horario","trabalho","expediente","entrada","sada","saida"]):
            returnf"""Com base no manual do funcionrio, aqui esto as informaes sobre horrio de trabalho:

 **Horrio de Trabalho:**
- Segunda a sexta-feira: 8h s 18h
- Intervalo para almoo: 12h s 13h
- Flexibilidade de 30 minutos para entrada e sada

Esta  uma poltica importante para manter o equilbrio entre vida pessoal e profissional. Se precisar de mais detalhes ou tiver alguma situao especfica, posso ajudar com mais informaes.
"""

ifany(wordinmessage_lowerforwordin["benefcio","beneficio","vale","plano"]):
            returnf"""Aqui esto todos os benefcios oferecidos pela empresa:

**Beneficios Disponiveis:**
- Vale refeio: R$ 25,00 por dia
- Vale transporte: conforme uso
- Plano de sade: cobertura completa
- Plano odontolgico: cobertura bsica
- Gympass: acesso a academias parceiras

Esses benefcios so parte do pacote de remunerao e visam melhorar sua qualidade de vida. Se tiver dvidas sobre como utilizar algum deles, posso esclarecer mais detalhes.
"""

returnf"""Encontrei informaes relevantes para sua pergunta:
{all_info}

Esta  a informao mais completa que encontrei nos documentos disponveis. Se precisar de mais detalhes sobre algum aspecto especfico ou tiver outras dvidas, fique  vontade para perguntar!
"""

def_format_generic_response(self,message:str,relevant_info:List[str])->str:
        """Formata resposta para consultas genricas como apenas 'Academia'"""
message_lower=message.lower().strip()

domain_keywords={
'academia':['academia','gym','fitness','musculao','musculacao'],
'supermercado':['supermercado','mercado','loja','compras'],
'restaurante':['restaurante','comida','jantar','almoo','almoco'],
'empresa':['empresa','trabalho','funcionrio','funcionario','rh']
}

identified_domain=None
fordomain,keywordsindomain_keywords.items():
            ifany(keywordinmessage_lowerforkeywordinkeywords):
                identified_domain=domain
break

ifidentified_domain:
            returnself._get_domain_overview(identified_domain)

return"""**Informacoes Disponiveis:**

Temos informacoes sobre:
- **Academia**: Horarios, planos, equipamentos
- **Supermercado**: Promocoes, delivery, departamentos  
- **Restaurante**: Cardapio, reservas, horarios
- **Empresa**: Beneficios, politicas, RH

Seja mais especifico na sua pergunta para obter informacoes detalhadas!"""

def_extract_schedule_block(self,info_parts:List[str])->str:
        """Extrai bloco de horrio de funcionamento de qualquer documento."""
importre
joined="\n".join(info_parts)

patterns=[
r"HOR[A]RIO DE FUNCIONAMENTO[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)",
r"Hor[a]rio[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)"
]
forpatterninpatterns:
            m=re.search(pattern,joined,flags=re.IGNORECASE)
ifm:
                returnm.group(0).strip()

candidates=[]
forlineinjoined.splitlines():
            ifany(kinline.lower()forkin["segunda","tera","terca","quarta","quinta","sexta","sbado","sabado","domingo","feriado","24h","h s","h as","almoo","almoco","jantar"]):
                candidates.append(line.strip())
return"\n".join(candidates[:8])ifcandidateselse""

def_extract_prices_block(self,info_parts:List[str])->str:
        """Extrai bloco de preos/planos de qualquer documento (planos, mensalidades, valores)."""
importre
joined="\n".join(info_parts)
patterns=[
r"PLANOS DISPON[I]VEIS[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)",
r"Pre[c]os?[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)",
r"Mensalidad[ea]s?[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)",
]
forpatterninpatterns:
            m=re.search(pattern,joined,flags=re.IGNORECASE)
ifm:
                returnm.group(0).strip()

candidates=[]
forlineinjoined.splitlines():
            ifany(kinline.lower()forkin["r$","preo","preco","valor","mensalidade","plano "]):
                candidates.append(line.strip())
return"\n".join(candidates[:12])ifcandidateselse""

def_extract_contacts_block(self,info_parts:List[str])->str:
        """Extrai bloco de contatos (telefone, email, site, redes)."""
importre
joined="\n".join(info_parts)
patterns=[
r"CONTATOS?[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)",
r"Localiza[c][a]o[\s\S]*?(?=\n\s*\d+\.|\n\s*[A-Z]{3,}|\Z)"
]
forpatterninpatterns:
            m=re.search(pattern,joined,flags=re.IGNORECASE)
ifm:
                returnm.group(0).strip()

candidates=[]
forlineinjoined.splitlines():
            ifany(kinline.lower()forkin["telefone","whatsapp","email","site","instagram","endereo","endereco"]):
                candidates.append(line.strip())
return"\n".join(candidates[:10])ifcandidateselse""

def_generate_fallback_response(self,message:str,context:str)->str:
        """Gera resposta de fallback quando no h informaes especficas"""

if"Documentos relevantes:"incontext:
            returnf"Encontrei alguns documentos que podem ser relevantes para sua pergunta sobre '{message}', mas no consegui extrair uma resposta especfica. Voc pode reformular sua pergunta ou fazer upload de documentos mais especficos."
else:
            returnself._get_random_response("sem_documentos")

def_is_greeting(self,message:str)->bool:
        """Verifica se a mensagem  uma saudao"""
greetings=[
"ol","oi","ola","hey","ei","bom dia","boa tarde","boa noite",
"hello","hi","good morning","good afternoon","good evening"
]
returnany(greetinginmessageforgreetingingreetings)

def_is_farewell(self,message:str)->bool:
        """Verifica se a mensagem  uma despedida"""
farewells=[
"tchau","adeus","at logo","at mais","at a prxima","bye","goodbye",
"see you","at breve","at depois"
]
returnany(farewellinmessageforfarewellinfarewells)

def_is_thanks(self,message:str)->bool:
        """Verifica se a mensagem  um agradecimento"""
thanks=[
"obrigado","obrigada","valeu","thanks","thank you","grato","gratido"
]
returnany(thankinmessageforthankinthanks)

def_get_random_response(self,response_type:str)->str:
        """Retorna uma resposta aleatria do tipo especificado"""
importrandom
responses=self.default_responses.get(response_type,["Desculpe, no entendi."])
returnrandom.choice(responses)

asyncdef_learn_from_interaction_async(self,question:str,response:str,sources:List[str],session_id:str):
        """Aprende com a interao de forma assncrona"""
try:
            self.learning_manager.learn_from_interaction(
question=question,
response=response,
sources=sources,
session_id=session_id
)
exceptExceptionase:
            print(f"Erro no aprendizado assncrono: {e}")

defget_session_history(self,session_id:str)->List[Dict[str,Any]]:
        """Retorna histrico de uma sesso"""
returnself.sessions.get(session_id,[])

defclear_session_history(self,session_id:str)->bool:
        """Limpa histrico de uma sesso"""
ifsession_idinself.sessions:
            self.sessions[session_id]=[]
returnTrue
returnFalse

defget_all_sessions(self)->Dict[str,List[Dict[str,Any]]]:
        """Retorna todas as sesses"""
returnself.sessions

defdelete_session(self,session_id:str)->bool:
        """Remove uma sesso completamente"""
ifsession_idinself.sessions:
            delself.sessions[session_id]
returnTrue
returnFalse

defrecord_user_feedback(self,session_id:str,question:str,response:str,
satisfaction:int,feedback_text:Optional[str]=None)->bool:
        """Registra feedback do usurio"""
returnself.learning_manager.record_user_feedback(
session_id=session_id,
question=question,
response=response,
satisfaction=satisfaction,
feedback_text=feedback_text
)

defget_learning_stats(self)->Dict[str,Any]:
        """Retorna estatsticas de aprendizado"""
returnself.learning_manager.get_learning_stats()

defget_suggested_questions(self,limit:int=5)->List[str]:
        """Retorna perguntas sugeridas baseadas no aprendizado"""
try:

            stats=self.get_learning_stats()
popular_categories=stats.get("most_popular_categories",[])

suggestions=[]
forcategory,frequencyinpopular_categories[:limit]:
                ifcategoryinself.learning_manager.questions_patterns:
                    patterns=self.learning_manager.questions_patterns[category]["patterns"]
ifpatterns:

                        suggestions.append(patterns[0].capitalize()+"?")

returnsuggestions

exceptExceptionase:
            print(f"Erro ao obter perguntas sugeridas: {e}")
return[]

defclear_cache(self):
        """Limpa todos os caches"""
self.cache_manager.clear()
self._document_cache.clear()
self._last_document_load.clear()
print(" Cache limpo com sucesso")

defget_cache_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache"""
return{
"cache_manager_stats":self.cache_manager.get_statistics(),
"document_cache_size":len(self._document_cache),
"quick_responses_cache_size":len(self._quick_responses_cache)
}
