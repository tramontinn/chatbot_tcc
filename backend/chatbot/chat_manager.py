importos
fromtypingimportList,Dict,Any,Tuple,Optional
importjson
importuuid
fromdatetimeimportdatetime
importre
fromdifflibimportSequenceMatcher

from.nlp_processorimportNLPProcessor
from.advanced_nlp_processorimportAdvancedNLPProcessor
from.internal_document_managerimportInternalDocumentManager
from.learning_managerimportLearningManager
from.context_analyzerimportContextAnalyzer

classChatManager:
    """Gerencia conversas com IA local e busca em documentos usando PLN avanado"""

def__init__(self,vector_store,internal_doc_manager:Optional[InternalDocumentManager]=None,use_advanced_nlp:bool=True):
        self.vector_store=vector_store
self.internal_doc_manager=internal_doc_manager
self.use_advanced_nlp=use_advanced_nlp

ifuse_advanced_nlp:
            try:
                self.nlp_processor=AdvancedNLPProcessor()
print(" Processador NLP avanado inicializado")
exceptExceptionase:
                print(f" Erro ao inicializar NLP avanado: {e}. Usando processador bsico.")
self.nlp_processor=NLPProcessor()
self.use_advanced_nlp=False
else:
            self.nlp_processor=NLPProcessor()

self.learning_manager=LearningManager()
print(" Sistema de aprendizado inicializado")

self.context_analyzer=ContextAnalyzer()
print(" Analisador de contexto inicializado")

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

asyncdefprocess_message(self,message:str,session_id:Optional[str]=None)->Tuple[str,str,List[str]]:
        """Processa uma mensagem e retorna resposta, session_id e fontes usando PLN"""

ifnotsession_id:
            session_id=str(uuid.uuid4())

ifsession_idnotinself.sessions:
            self.sessions[session_id]=[]

relevant_docs=self._search_with_nlp(message)

message_lower=message.lower()
domain_keywords={
'academia':['academia','gym','fitness','musculao','musculacao'],
'supermercado':['supermercado','mercado','loja','compras'],
'restaurante':['restaurante','comida','jantar','almoo','almoco'],
'empresa':['empresa','trabalho','funcionrio','funcionario','rh']
}
detected_domain=None
fordomain,keywordsindomain_keywords.items():
            ifany(kinmessage_lowerforkinkeywords):
                detected_domain=domain
break
ifdetected_domainandrelevant_docs:
            domain_docs=[dfordinrelevant_docsifdetected_domainind.get('metadata',{}).get('filename','').lower()ord.get('metadata',{}).get('category')==detected_domain]
ifdomain_docs:
                relevant_docs=domain_docs[:3]

context=self._prepare_context(relevant_docs)

response=awaitself._generate_nlp_response(message,context,session_id)

try:
            improved_response=self.learning_manager.get_improved_response(message,response)
exceptExceptionase:
            print(f"Erro ao melhorar resposta: {e}")
improved_response=response

self.sessions[session_id].append({
"user_message":message,
"bot_response":improved_response,
"timestamp":datetime.now().isoformat(),
"sources":[doc["metadata"]["filename"]fordocinrelevant_docs]
})

self.learning_manager.learn_from_interaction(
question=message,
response=improved_response,
sources=[doc["metadata"]["filename"]fordocinrelevant_docs],
session_id=session_id
)

sources=[doc["metadata"]["filename"]fordocinrelevant_docs]

returnimproved_response,session_id,sources

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

asyncdef_generate_local_response(self,message:str,context:str,session_id:str)->str:
        """Gera resposta usando IA local baseada em regras e contexto"""

message_lower=message.lower().strip()

ifself._is_greeting(message_lower):
            returnself._get_random_response("saudacao")

ifself._is_farewell(message_lower):
            returnself._get_random_response("despedida")

ifself._is_thanks(message_lower):
            returnself._get_random_response("agradecimento")

if"no h documentos"incontext.lower():
            returnself._get_random_response("sem_documentos")

returnself._generate_contextual_response(message,context,session_id)

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

def_generate_contextual_response(self,message:str,context:str,session_id:str)->str:
        """Gera resposta contextual baseada nos documentos"""

relevant_info=self._extract_relevant_info(message,context)

ifrelevant_info:
            returnself._format_contextual_response(message,relevant_info)
else:
            returnself._generate_fallback_response(message,context)

def_extract_relevant_info(self,message:str,context:str)->List[str]:
        """Extrai informaes relevantes do contexto baseado na pergunta"""
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

ifidentified_domain=='academia':
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

elifidentified_domain=='supermercado':
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

elifidentified_domain=='restaurante':
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

elifidentified_domain=='empresa':
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

else:
            return""" **Informaes Disponveis:**

Temos informaes sobre:
-  **Academia**: Horrios, planos, equipamentos
-  **Supermercado**: Promoes, delivery, departamentos  
-  **Restaurante**: Cardpio, reservas, horrios
- **Empresa**: Beneficios, politicas, RH

Seja mais especfico na sua pergunta para obter informaes detalhadas!"""

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

ifany(wordinmessage_lowerforwordin["frias","ferias","descanso"]):
            returnf"""Aqui esto as informaes completas sobre frias:

 **Poltica de Frias:**
- 30 dias por ano
- 1/3 de adicional constitucional
- Pode ser dividido em at 3 perodos
- Mnimo de 5 dias consecutivos

As frias so um direito importante para seu descanso e bem-estar.  recomendado planejar com antecedncia e comunicar ao RH sobre suas preferncias de datas.
"""

ifany(wordinmessage_lowerforwordin["licena","licenca","mdica","medica","atestado"]):
            returnf"""Informaes sobre licena mdica e atestados:

 **Licena Mdica:**
- Atestado mdico obrigatrio a partir do 3 dia
- Pagamento integral at 15 dias
- Aps 15 dias, encaminhamento ao INSS

Sua sade  prioridade. Em caso de necessidade, no hesite em procurar atendimento mdico e seguir os procedimentos adequados para comunicar sua ausncia.
"""

ifany(wordinmessage_lowerforwordin["vestimenta","roupa","traje","cdigo","codigo"]):
            returnf"""Cdigo de vestimenta da empresa:

 **Poltica de Vestimenta:**
- Segunda a quinta-feira: traje social
- Sexta-feira: casual
- Evitar roupas muito informais

O cdigo de vestimenta visa manter um ambiente profissional e respeitoso. Em dias especiais ou eventos, pode haver orientaes especficas do RH.
"""

ifany(wordinmessage_lowerforwordin["comunicao","comunicacao","contato","email"]):
            returnf"""Canais de comunicao interna:

 **Comunicao na Empresa:**
- Email corporativo: para assuntos oficiais
- WhatsApp: para comunicao rpida
- Slack: para projetos especficos
- RH: rh@empresaexemplo.com (para dvidas gerais)

A comunicao eficaz  fundamental para o sucesso da equipe. Use o canal mais apropriado para cada tipo de assunto.
"""

ifany(wordinmessage_lowerforwordin["segurana","seguranca","carto","cartao","acesso"]):
            returnf"""Polticas de segurana da empresa:

 **Segurana no Trabalho:**
- Carto de acesso obrigatrio
- No compartilhar senhas
- Bloquear computador ao sair da mesa
- Relatar incidentes de segurana

A segurana  responsabilidade de todos. Mantenha-se sempre alerta e siga as diretrizes para proteger informaes e recursos da empresa.
"""

ifany(wordinmessage_lowerforwordin["limpeza","organizao","organizacao"]):
            returnf"""Diretrizes de limpeza e organizao:

 **Limpeza e Organizao:**
- Manter mesa organizada
- Descarte adequado de lixo
- Participar da limpeza da copa
- Respeitar espaos comuns

Um ambiente limpo e organizado contribui para a produtividade e bem-estar de toda a equipe. Cada um faz sua parte!
"""

ifany(wordinmessage_lowerforwordin["treinamento","curso","capacitao","capacitacao"]):
            returnf"""Oportunidades de desenvolvimento:

 **Treinamentos e Desenvolvimento:**
- Treinamento obrigatrio de integrao
- Cursos online disponveis na plataforma
- Participao em workshops mensais
- Desenvolvimento contnuo incentivado

O crescimento profissional  valorizado na empresa. Aproveite as oportunidades de aprendizado para expandir suas habilidades e conhecimentos.
"""

returnf"""Encontrei informaes relevantes para sua pergunta:
{all_info}

Esta  a informao mais completa que encontrei nos documentos disponveis. Se precisar de mais detalhes sobre algum aspecto especfico ou tiver outras dvidas, fique  vontade para perguntar!
"""

def_extract_academia_schedule_from_info(self,info_parts:List[str])->str:
        """[DEPRECATED] Mantido por compatibilidade. Use _extract_schedule_block."""
importre
joined="\n".join(info_parts)

pattern=r"1\.\s*HOR[A]RIO DE FUNCIONAMENTO[\s\S]*?(?=\n\s*2\.|\n\s*\d+\.|\Z)"
match=re.search(pattern,joined,flags=re.IGNORECASE)
ifnotmatch:

            candidates=[]
forlineinjoined.splitlines():
                ifany(kinline.lower()forkin["segunda","tera","terca","quarta","quinta","sexta","sbado","sabado","domingo","feriado","24h","h s","h as"]):
                    candidates.append(line.strip())
return"\n".join(candidates[:6])ifcandidateselse""
block=match.group(0)

block=re.sub(r"^1\.\s*HOR[A]RIO DE FUNCIONAMENTO\s*","",block,flags=re.IGNORECASE)
returnblock.strip()

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

def_generate_intelligent_fallback_response(self,message:str,context:str,analysis:Dict[str,Any])->str:
        """Gera resposta de fallback inteligente baseada na anlise de contexto"""
domain=analysis["domain"]
intent=analysis["intent"]

domain_responses={
"academia":{
"preco":"Para informaes sobre preos e planos da academia, recomendo entrar em contato diretamente. Os valores podem variar conforme promoes e planos disponveis.",
"horario":"O horrio de funcionamento da academia pode variar. Entre em contato para confirmar os horrios atuais e especiais.",
"servico":"Nossa academia oferece diversos servios. Recomendo uma visita para conhecer toda a estrutura e servios disponveis."
},
"supermercado":{
"preco":"Para informaes sobre preos e promoes do supermercado, recomendo verificar nosso site ou visitar a loja. As promoes mudam semanalmente.",
"horario":"Nosso supermercado tem horrios especficos. Entre em contato para confirmar os horrios atuais.",
"servico":"Oferecemos diversos servios no supermercado. Recomendo uma visita para conhecer todos os departamentos e servios."
},
"restaurante":{
"preco":"Para informaes sobre preos do cardpio, recomendo fazer uma reserva ou visitar nosso estabelecimento. Temos pratos para todos os gostos e bolsos.",
"horario":"Nosso restaurante tem horrios especficos para almoo e jantar. Recomendo fazer uma reserva para garantir sua mesa.",
"servico":"Oferecemos diversos servios no restaurante. Recomendo fazer uma reserva para conhecer nosso ambiente e servios."
},
"empresa":{
"preco":"Para informaes sobre benefcios e remunerao, recomendo entrar em contato com o RH. Eles tm todas as informaes atualizadas.",
"horario":"Para informaes sobre horrios de trabalho, consulte o manual do funcionrio ou entre em contato com o RH.",
"servico":"Para informaes sobre benefcios e servios da empresa, recomendo consultar o RH ou a intranet corporativa."
}
}

ifdomainindomain_responsesandintentindomain_responses[domain]:
            returndomain_responses[domain][intent]

ifdomain!="geral":
            returnf"Para informaes especficas sobre {domain}, recomendo entrar em contato diretamente com o estabelecimento ou consultar a documentao oficial."

returnself._generate_fallback_response(message,context)

def_search_with_nlp(self,message:str)->List[Dict[str,Any]]:
        """Busca documentos usando processamento NLP"""
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
                    internal_docs=self._search_internal_documents(message)
all_results=vector_results+internal_docs
else:
                    all_results=vector_results

returnself._refine_results_with_nlp(message,all_results)

exceptExceptionase:
            print(f"Erro na busca NLP: {e}")
return[]

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
content=self.internal_doc_manager.get_document_content(doc_info["filename"])
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

def_search_internal_documents(self,message:str)->List[Dict[str,Any]]:
        """Busca em documentos internos"""
try:

            ifself.use_advanced_nlp:
                question_category,confidence=self.nlp_processor.categorize_question_advanced(message)
else:
                question_category=self.nlp_processor.categorize_question(message)
confidence=0.5

category_docs=self.internal_doc_manager.get_documents_by_category(question_category)

ifnotcategory_docs:
                print(f"Nenhum documento encontrado na categoria '{question_category}', buscando em todos os documentos...")
all_docs=self.internal_doc_manager.list_documents()
category_docs=all_docs

results=[]
fordoc_infoincategory_docs:
                content=self.internal_doc_manager.get_document_content(doc_info["filename"])
ifcontent:

                    ifself.use_advanced_nlp:
                        semantic_sim=self.nlp_processor.calculate_semantic_similarity(message,content)
similarity=(semantic_sim+confidence)/2
else:
                        similarity=0.5

results.append({
"content":content,
"metadata":{
"filename":doc_info["filename"],
"category":doc_info["category"],
"timestamp":doc_info["last_modified"]
},
"similarity":similarity
})

returnresults

exceptExceptionase:
            print(f"Erro na busca de documentos internos: {e}")
return[]

def_refine_results_with_nlp(self,message:str,results:List[Dict[str,Any]])->List[Dict[str,Any]]:
        """Refina resultados usando NLP avanado"""
try:
            ifnotresults:
                return[]

ifself.use_advanced_nlp:
                message_keywords=self.nlp_processor.extract_keywords_advanced(message,max_keywords=5)
else:
                message_keywords=self.nlp_processor.extract_keywords(message,max_keywords=5)

refined_results=[]
forresultinresults:
                content=result["content"]

ifself.use_advanced_nlp:
                    relevant_sentences=self.nlp_processor.find_relevant_sentences_advanced(message,content,max_sentences=2)
else:
                    relevant_sentences=self.nlp_processor.find_relevant_sentences(message,content,max_sentences=2)

ifrelevant_sentences:

                    ifself.use_advanced_nlp:
                        nlp_similarity=self.nlp_processor.calculate_semantic_similarity(message,content)
else:
                        nlp_similarity=self.nlp_processor.calculate_similarity(message,content)

vector_similarity=result.get("similarity",0.0)
combined_similarity=(nlp_similarity+vector_similarity)/2

result["nlp_similarity"]=nlp_similarity
result["combined_similarity"]=combined_similarity
result["relevant_sentences"]=relevant_sentences

refined_results.append(result)

refined_results.sort(key=lambdax:x.get("combined_similarity",0),reverse=True)

returnrefined_results[:3]

exceptExceptionase:
            print(f"Erro no refinamento NLP: {e}")
returnresults[:3]

asyncdef_generate_nlp_response(self,message:str,context:str,session_id:str)->str:
        """Gera resposta usando processamento NLP"""

message_lower=message.lower().strip()

ifself._is_greeting(message_lower):
            returnself._get_random_response("saudacao")

ifself._is_farewell(message_lower):
            returnself._get_random_response("despedida")

ifself._is_thanks(message_lower):
            returnself._get_random_response("agradecimento")

if"no h documentos"incontext.lower():
            returnself._get_random_response("sem_documentos")

returnself._generate_contextual_nlp_response(message,context,session_id)

def_generate_contextual_nlp_response(self,message:str,context:str,session_id:str)->str:
        """Gera resposta contextual usando NLP avanado e anlise de contexto"""
try:

            analysis=self.context_analyzer.analyze_question(message)

relevant_info=self._extract_relevant_info(message,context)

ifrelevant_info:

                ifself.use_advanced_nlp:

                    relevant_sentences=[(info,0.8)forinfoinrelevant_info]
base_response=self.nlp_processor.generate_advanced_answer(message,relevant_sentences,context)
else:
                    base_response=self.nlp_processor.generate_answer(message,relevant_info,context)

enhanced_response=self.context_analyzer.enhance_response(base_response,analysis)
returnenhanced_response
else:

                message_words=message.lower().strip().split()
iflen(message_words)<=2:
                    returnself._format_generic_response(message,[])
else:

                    fallback_response=self._generate_intelligent_fallback_response(message,context,analysis)
returnfallback_response

exceptExceptionase:
            print(f"Erro na gerao de resposta NLP: {e}")
returnself._generate_fallback_response(message,context)

def_prepare_conversation_history(self,session_id:str)->str:
        """Prepara histrico da conversa para contexto"""
ifsession_idnotinself.sessionsornotself.sessions[session_id]:
            return"Nenhuma conversa anterior."

history_parts=[]
forentryinself.sessions[session_id][-5:]:
            history_parts.append(f"Usurio: {entry['user_message']}")
history_parts.append(f"Assistente: {entry['bot_response']}")

return"\n".join(history_parts)

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
