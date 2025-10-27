
importjson
fromtypingimportDict,List,Any,Optional
fromdatetimeimportdatetime
frompathlibimportPath

classUserGuidanceSystem:
    """Sistema que orienta usurios sobre documentos e funcionalidades disponveis"""

def__init__(self,internal_doc_manager=None):
        self.internal_doc_manager=internal_doc_manager

self.domain_descriptions={
"academia":{
"name":"Academia FitLife",
"description":"Informaes sobre horrios, planos, equipamentos e aulas",
"icon":"",
"color":"green",
"topics":[
"Horrios de funcionamento",
"Planos e preos (Bsico, Premium, VIP)",
"Equipamentos e estrutura",
"Aulas disponveis (spinning, pilates, yoga, etc.)",
"Servios adicionais (personal trainer, nutricionista)",
"Regras de uso e etiqueta",
"Localizao e contatos"
]
},
"supermercado":{
"name":"Supermercado Mega Economia",
"description":"Informaes sobre horrios, promoes, delivery e departamentos",
"icon":"",
"color":"blue",
"topics":[
"Horrios de funcionamento",
"Promoes e ofertas da semana",
"Servio de delivery",
"Departamentos (hortifrti, aougue, padaria, etc.)",
"Carto de crdito prprio",
"Programa de fidelidade",
"Localizao e contatos"
]
},
"restaurante":{
"name":"Restaurante Sabor & Arte",
"description":"Informaes sobre cardpio, horrios, reservas e especialidades",
"icon":"",
"color":"orange",
"topics":[
"Cardpio e preos",
"Horrios de funcionamento",
"Sistema de reservas",
"Especialidades do chef",
"Menu degustao",
"Servio de delivery",
"Harmonizao com vinhos"
]
},
"empresa":{
"name":"Manual do Funcionrio",
"description":"Polticas, benefcios, horrios e procedimentos da empresa",
"icon":"[EMPRESA]",
"color":"purple",
"topics":[
"Horrios de trabalho",
"Benefcios e auxlios",
"Poltica de frias",
"Licena mdica e atestados",
"Cdigo de vestimenta",
"Comunicao interna",
"Polticas de segurana",
"Treinamentos e desenvolvimento"
]
}
}

self.example_questions={
"academia":[
"Qual o horrio de funcionamento da academia?",
"Quanto custa o plano VIP?",
"Que aulas vocs oferecem?",
"Tem personal trainer disponvel?",
"Qual o endereo da academia?"
],
"supermercado":[
"Qual o horrio de funcionamento?",
"Vocs fazem delivery?",
"Quais as promoes desta semana?",
"Tem estacionamento gratuito?",
"Aceitam carto de crdito?"
],
"restaurante":[
"Qual o cardpio do dia?",
"Preciso fazer reserva?",
"Qual o horrio do almoo?",
"Tem menu vegetariano?",
"Fazem delivery?"
],
"empresa":[
"Qual o horrio de trabalho?",
"Quais so os benefcios oferecidos?",
"Como funciona a poltica de frias?",
"Qual o valor do vale refeio?",
"Como entrar em contato com o RH?"
]
}

defget_available_documents_overview(self)->str:
        """Retorna viso geral dos documentos disponveis"""

ifnotself.internal_doc_manager:
            returnself._get_no_documents_message()

try:
            documents=self.internal_doc_manager.list_documents()

ifnotdocuments:
                returnself._get_no_documents_message()

categories={}
fordocindocuments:
                category=doc.get('category','geral')
ifcategorynotincategories:
                    categories[category]=[]
categories[category].append(doc)

message_parts=[
" **Documentos Disponveis no Sistema:**\n",
"Encontrei as seguintes informaes que posso compartilhar com voc:\n"
]

forcategory,docsincategories.items():
                ifcategoryinself.domain_descriptions:
                    domain_info=self.domain_descriptions[category]
message_parts.append(f"{domain_info['icon']} **{domain_info['name']}**")
message_parts.append(f"*{domain_info['description']}*\n")

message_parts.append("**Principais tpicos:**")
fortopicindomain_info['topics'][:5]:
                        message_parts.append(f" {topic}")
message_parts.append("")

message_parts.extend([
" **Como usar:**",
" Faa perguntas especficas sobre qualquer tpico",
" Seja claro sobre o que precisa saber",
" Posso ajudar com informaes detalhadas sobre cada rea",
"",
"**Exemplo de perguntas:**",
" 'Qual o horrio da academia?'",
" 'Quanto custa o plano premium?'",
" 'Quais so os benefcios da empresa?'"
])

return"\n".join(message_parts)

exceptExceptionase:
            returnf" Erro ao verificar documentos disponveis: {str(e)}"

defget_domain_specific_guidance(self,domain:str)->str:
        """Retorna orientao especfica para um domnio"""

ifdomainnotinself.domain_descriptions:
            return"Domnio no reconhecido. Use 'documentos' para ver o que est disponvel."

domain_info=self.domain_descriptions[domain]
examples=self.example_questions.get(domain,[])

message_parts=[
f"{domain_info['icon']} **{domain_info['name']}**",
f"*{domain_info['description']}*\n",
"**Sobre o que posso ajudar:**"
]

fortopicindomain_info['topics']:
            message_parts.append(f" {topic}")

ifexamples:
            message_parts.extend([
"\n**Exemplos de perguntas que posso responder:**"
])
forexampleinexamples[:3]:
                message_parts.append(f" '{example}'")

message_parts.extend([
"\n **Dica:** Seja especfico na sua pergunta para obter a melhor resposta!"
])

return"\n".join(message_parts)

defget_smart_suggestions(self,question:str,domain:str=None)->List[str]:
        """Retorna sugestes inteligentes baseadas na pergunta"""

question_lower=question.lower()
suggestions=[]

ifany(wordinquestion_lowerforwordin["horrio","horario","funcionamento"]):
            suggestions.extend([
"Voc pode perguntar sobre horrios especficos de cada dia",
"Quer saber sobre horrios especiais ou feriados?",
"Precisa de informaes sobre horrios de atendimento?"
])

ifany(wordinquestion_lowerforwordin["preo","preco","valor","custo","quanto"]):
            suggestions.extend([
"Posso detalhar todos os preos e planos disponveis",
"Quer comparar diferentes opes de preos?",
"Precisa de informaes sobre promoes ou descontos?"
])

ifany(wordinquestion_lowerforwordin["servio","servico","o que","tem"]):
            suggestions.extend([
"Posso listar todos os servios disponveis",
"Quer saber sobre servios adicionais?",
"Precisa de informaes sobre como usar os servios?"
])

ifdomainanddomaininself.example_questions:
            domain_examples=self.example_questions[domain]
suggestions.extend([
f"Outras perguntas comuns sobre {self.domain_descriptions[domain]['name']}:",
f" {domain_examples[0]}",
f" {domain_examples[1]}"
])

returnsuggestions[:5]

defget_contextual_help(self,question:str,context:str,domain:str)->str:
        """Retorna ajuda contextual baseada na pergunta e contexto"""

ifnotcontextor"no h documentos"incontext.lower():
            returnself._get_no_relevant_info_help(question,domain)

returnself._get_deepening_suggestions(question,domain)

def_get_no_documents_message(self)->str:
        """Mensagem quando no h documentos"""
return""" **Sistema de Documentos**

No momento, no h documentos carregados no sistema.

**O que posso fazer por voc:**
 Responder perguntas gerais
 Orientar sobre como usar o sistema
 Explicar minhas funcionalidades

**Para carregar documentos:**
 Use a interface de upload
 Adicione documentos na pasta interna
 Entre em contato com o administrador

 **Dica:** Assim que documentos forem carregados, poderei ajud-lo com informaes especficas!"""

def_get_no_relevant_info_help(self,question:str,domain:str)->str:
        """Ajuda quando no h informaes relevantes"""

suggestions=self.get_smart_suggestions(question,domain)

message_parts=[
" **No encontrei informaes especficas sobre sua pergunta.**",
"",
"**Mas posso ajudar de outras formas:**"
]

ifsuggestions:
            message_parts.extend(suggestions)

ifdomainanddomaininself.domain_descriptions:
            domain_info=self.domain_descriptions[domain]
message_parts.extend([
"",
f"**Ou pergunte sobre {domain_info['name']}:**",
f" {self.example_questions[domain][0]}",
f" {self.example_questions[domain][1]}"
])

message_parts.extend([
"",
" **Dica:** Tente reformular sua pergunta ou ser mais especfico!"
])

return"\n".join(message_parts)

def_get_deepening_suggestions(self,question:str,domain:str)->str:
        """Sugestes para aprofundar a conversa"""

message_parts=[
" **Quer saber mais?**",
"",
"**Voc pode perguntar sobre:**"
]

ifdomainanddomaininself.domain_descriptions:
            domain_info=self.domain_descriptions[domain]

all_topics=domain_info['topics']
question_words=set(question.lower().split())

relevant_topics=[]
fortopicinall_topics:
                topic_words=set(topic.lower().split())
ifnotquestion_words.intersection(topic_words):
                    relevant_topics.append(topic)

fortopicinrelevant_topics[:3]:
                message_parts.append(f" {topic}")

message_parts.extend([
"",
"**Ou faa perguntas mais especficas:**",
" 'Me explique melhor sobre...'",
" 'Quais so os detalhes de...'",
" 'Como funciona...'"
])

return"\n".join(message_parts)

defget_system_status(self)->Dict[str,Any]:
        """Retorna status do sistema"""

status={
"timestamp":datetime.now().isoformat(),
"documents_loaded":False,
"available_domains":[],
"total_documents":0,
"system_ready":False
}

ifself.internal_doc_manager:
            try:
                documents=self.internal_doc_manager.list_documents()
status["total_documents"]=len(documents)
status["documents_loaded"]=len(documents)>0

domains=set()
fordocindocuments:
                    category=doc.get('category','geral')
ifcategoryinself.domain_descriptions:
                        domains.add(category)

status["available_domains"]=list(domains)
status["system_ready"]=len(documents)>0

exceptExceptionase:
                status["error"]=str(e)

returnstatus
