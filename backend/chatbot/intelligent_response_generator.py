
importre
importrandom
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime
importjson
from.intelligent_fallback_systemimportIntelligentFallbackSystem

classIntelligentResponseGenerator:
    """Gerador de respostas inteligentes com mltiplas camadas de fallback"""

def__init__(self):

        self.fallback_system=IntelligentFallbackSystem()

self.domain_responses={
"academia":{
"greeting":[
"Ol! Sou o assistente da Academia FitLife!  Como posso ajud-lo hoje?",
"Oi! Estou aqui para esclarecer suas dvidas sobre nossa academia! ",
"Ol! Bem-vindo  Academia FitLife! Em que posso ser til?"
],
"fallback":[
"Entendo sua pergunta sobre {topic}. Embora no tenha essa informao especfica nos nossos documentos, posso ajud-lo com outras questes sobre horrios, planos, equipamentos ou aulas!",
"tima pergunta sobre {topic}! Para informaes mais detalhadas, recomendo entrar em contato conosco pelo WhatsApp (11) 98765-4321 ou visitar nossa academia.",
"Sobre {topic}, no tenho essa informao especfica no momento. Mas posso ajudar com informaes sobre nossos planos, horrios de funcionamento ou estrutura!"
],
"suggestions":[
" **Voc pode perguntar sobre:**",
" Horrios de funcionamento",
" Planos e preos disponveis",
" Equipamentos e estrutura",
" Aulas e modalidades",
" Servios adicionais (personal trainer, nutricionista)"
]
},
"supermercado":{
"greeting":[
"Ol! Sou o assistente do Supermercado Mega Economia!  Como posso ajud-lo hoje?",
"Oi! Estou aqui para esclarecer suas dvidas sobre nosso supermercado! ",
"Ol! Bem-vindo ao Mega Economia! Em que posso ser til?"
],
"fallback":[
"Entendo sua pergunta sobre {topic}. Embora no tenha essa informao especfica nos nossos documentos, posso ajud-lo com outras questes sobre horrios, promoes, delivery ou departamentos!",
"tima pergunta sobre {topic}! Para informaes mais detalhadas, recomendo entrar em contato conosco ou visitar nossa loja.",
"Sobre {topic}, no tenho essa informao especfica no momento. Mas posso ajudar com informaes sobre nossos horrios, promoes ou servios de delivery!"
],
"suggestions":[
" **Voc pode perguntar sobre:**",
" Horrios de funcionamento",
" Promoes e ofertas da semana",
" Servio de delivery",
" Departamentos disponveis",
" Carto de crdito prprio"
]
},
"restaurante":{
"greeting":[
"Ol! Sou o assistente do Restaurante Sabor & Arte!  Como posso ajud-lo hoje?",
"Oi! Estou aqui para esclarecer suas dvidas sobre nosso restaurante! ",
"Ol! Bem-vindo ao Sabor & Arte! Em que posso ser til?"
],
"fallback":[
"Entendo sua pergunta sobre {topic}. Embora no tenha essa informao especfica nos nossos documentos, posso ajud-lo com outras questes sobre cardpio, horrios, reservas ou delivery!",
"tima pergunta sobre {topic}! Para informaes mais detalhadas, recomendo fazer uma reserva ou entrar em contato conosco.",
"Sobre {topic}, no tenho essa informao especfica no momento. Mas posso ajudar com informaes sobre nosso cardpio, horrios ou sistema de reservas!"
],
"suggestions":[
" **Voc pode perguntar sobre:**",
" Cardpio e preos",
" Horrios de funcionamento",
" Sistema de reservas",
" Especialidades do chef",
" Servio de delivery"
]
},
"empresa":{
"greeting":[
"Ola! Sou o assistente de RH da empresa! Como posso ajuda-lo hoje?",
"Oi! Estou aqui para esclarecer suas dvidas sobre polticas e procedimentos! ",
"Ol! Bem-vindo ao sistema de RH! Em que posso ser til?"
],
"fallback":[
"Entendo sua pergunta sobre {topic}. Embora no tenha essa informao especfica no manual do funcionrio, posso ajud-lo com outras questes sobre benefcios, horrios, frias ou polticas!",
"tima pergunta sobre {topic}! Para informaes mais detalhadas, recomendo entrar em contato com o RH pelo email rh@empresaexemplo.com.",
"Sobre {topic}, no tenho essa informao especfica no momento. Mas posso ajudar com informaes sobre benefcios, horrios de trabalho ou polticas da empresa!"
],
"suggestions":[
" **Voc pode perguntar sobre:**",
" Horrios de trabalho",
" Benefcios e auxlios",
" Poltica de frias",
" Licena mdica",
" Cdigo de vestimenta"
]
}
}

self.situation_responses={
"no_documents":[
"Ol!  Ainda no h documentos carregados no sistema, mas posso ajud-lo de outras formas!",
"Oi!  O sistema est sendo configurado. Em breve teremos todas as informaes disponveis!",
"Ol!  Estamos preparando o sistema para voc. Aguarde um momento!"
],
"unclear_question":[
"Desculpe, no consegui entender completamente sua pergunta. Poderia reformular de outra forma? ",
"Interessante pergunta!  Poderia ser mais especfico para que eu possa ajud-lo melhor?",
"No tenho certeza se entendi. Voc poderia explicar de outra forma? "
],
"complex_question":[
"Essa  uma pergunta complexa!  Vou organizar as informaes para voc da melhor forma possvel.",
"tima pergunta!  Deixe-me estruturar uma resposta completa para voc.",
"Interessante!  Vou quebrar isso em partes para explicar melhor."
],
"thank_you":[
"De nada!  Fico feliz em ajudar! Se precisar de mais alguma coisa,  s perguntar!",
"Por nada!  Estou aqui para isso! Qualquer dvida, estou  disposio!",
"Disponha!  Foi um prazer ajud-lo! Volte sempre que precisar!"
],
"goodbye":[
"At logo!  Foi um prazer conversar com voc! Tenha um timo dia!",
"Tchau!  Espero ter ajudado! Volte sempre que precisar!",
"At a prxima!  Foi timo conversar com voc!"
]
}

self.common_patterns={
"what_are_you":[
"Sou um assistente virtual inteligente!  Estou aqui para ajud-lo com informaes sobre {domain}. Posso responder perguntas sobre horrios, preos, servios e muito mais!",
"Ol! Sou seu assistente pessoal para {domain}!  Posso esclarecer dvidas, fornecer informaes e ajudar com o que precisar!",
"Sou um chatbot especializado em {domain}!  Meu objetivo  tornar sua experincia mais fcil e informativa!"
],
"what_can_you_do":[
"Posso ajud-lo com vrias coisas relacionadas a {domain}! ",
" Responder perguntas sobre horrios e funcionamento",
" Informar sobre preos e planos disponveis",
" Explicar servios e benefcios",
" Orientar sobre procedimentos e polticas",
" E muito mais! S perguntar! "
],
"help":[
"Claro! Estou aqui para ajudar! ",
"Voc pode me fazer perguntas sobre:",
" Horrios de funcionamento",
" Preos e planos",
" Servios disponveis",
" Polticas e procedimentos",
" Qualquer outra dvida que tiver!",
"Seja especfico na sua pergunta para eu poder ajud-lo melhor! "
]
}

defgenerate_intelligent_response(self,question:str,context:str,domain:str,
has_relevant_info:bool,session_history:List[Dict]=None)->str:
        """Gera resposta inteligente baseada em mltiplas camadas"""

question_lower=question.lower().strip()

chatbot_response=self._handle_chatbot_questions(question_lower,domain)
ifchatbot_response:
            returnchatbot_response

social_response=self._handle_social_interactions(question_lower)
ifsocial_response:
            returnsocial_response

ifhas_relevant_infoandcontext:
            returnself._generate_contextual_response(question,context,domain)

returnself._generate_intelligent_fallback(question,domain,session_history)

def_handle_chatbot_questions(self,question:str,domain:str)->Optional[str]:
        """Lida com perguntas sobre o prprio chatbot"""

ifany(phraseinquestionforphrasein["o que voc ","quem  voc","o que voc faz"]):
            returnrandom.choice(self.common_patterns["what_are_you"]).format(domain=domain)

ifany(phraseinquestionforphrasein["o que voc pode fazer","como voc pode ajudar","suas funes"]):
            return"\n".join(self.common_patterns["what_can_you_do"]).format(domain=domain)

ifany(phraseinquestionforphrasein["ajuda","help","como usar"]):
            return"\n".join(self.common_patterns["help"])

returnNone

def_handle_social_interactions(self,question:str)->Optional[str]:
        """Lida com interaes sociais"""

greetings=["ol","oi","ola","hey","ei","bom dia","boa tarde","boa noite","hello","hi"]
ifany(greetinginquestionforgreetingingreetings):
            returnrandom.choice(self.situation_responses["thank_you"])

farewells=["tchau","adeus","at logo","at mais","bye","goodbye","see you"]
ifany(farewellinquestionforfarewellinfarewells):
            returnrandom.choice(self.situation_responses["goodbye"])

thanks=["obrigado","obrigada","valeu","thanks","thank you","grato"]
ifany(thankinquestionforthankinthanks):
            returnrandom.choice(self.situation_responses["thank_you"])

returnNone

def_generate_contextual_response(self,question:str,context:str,domain:str)->str:
        """Gera resposta contextual quando h informaes relevantes"""

relevant_parts=self._extract_most_relevant_parts(question,context)

ifnotrelevant_parts:
            returnself._generate_intelligent_fallback(question,domain)

response_parts=[]

ifdomaininself.domain_responses:
            intro=f"Encontrei informaes relevantes para sua pergunta! {random.choice(['','',''])}"
response_parts.append(intro)

fori,partinenumerate(relevant_parts[:2],1):
            ifi==1:
                response_parts.append(f"\n**{part}**")
else:
                response_parts.append(f"\n**Tambm encontrei:**\n{part}")

ifdomaininself.domain_responses:
            suggestions=self.domain_responses[domain]["suggestions"]
response_parts.append(f"\n{chr(10).join(suggestions)}")

return"\n".join(response_parts)

def_extract_most_relevant_parts(self,question:str,context:str)->List[str]:
        """Extrai as partes mais relevantes do contexto"""

sections=context.split("\n")
relevant_sections=[]

question_words=set(question.lower().split())

forsectioninsections:
            iflen(section.strip())<10:
                continue

section_words=set(section.lower().split())
common_words=question_words.intersection(section_words)

iflen(common_words)>=2orany(keywordinsection.lower()forkeywordin
["horrio","preo","benefcio","plano","servio","poltica"]):
                relevant_sections.append(section.strip())

returnrelevant_sections[:3]

def_generate_intelligent_fallback(self,question:str,domain:str,session_history:List[Dict]=None)->str:
        """Gera resposta de fallback inteligente"""

topic=self._extract_topic_from_question(question)

ifdomaininself.domain_responses:
            fallback_responses=self.domain_responses[domain]["fallback"]
base_response=random.choice(fallback_responses).format(topic=topic)

suggestions=self.domain_responses[domain]["suggestions"]
full_response=f"{base_response}\n\n{chr(10).join(suggestions)}"

returnfull_response

returnself.fallback_system.get_intelligent_fallback(question,context,domain)

def_extract_topic_from_question(self,question:str)->str:
        """Extrai o tpico principal da pergunta"""

stop_words={
"qual","quais","como","quando","onde","por que","porque","o que","que",
"voc","pode","me","falar","sobre","de","da","do","das","dos"
}

words=question.lower().split()
topic_words=[wordforwordinwordsifwordnotinstop_wordsandlen(word)>2]

iftopic_words:
            return" ".join(topic_words[:3])

return"sua pergunta"

defget_domain_specific_greeting(self,domain:str)->str:
        """Retorna saudao especfica do domnio"""
ifdomaininself.domain_responses:
            returnrandom.choice(self.domain_responses[domain]["greeting"])

return"Ol! Como posso ajud-lo hoje?"

defenhance_response_with_emojis(self,response:str,domain:str)->str:
        """Adiciona prefixos apropriados baseados no domnio"""

domain_prefixes={
"academia":"[ACADEMIA]",
"supermercado":"[SUPERMERCADO]",
"restaurante":"[RESTAURANTE]",
"empresa":"[EMPRESA]"
}

ifdomainindomain_prefixes:

            ifnotany(ord(char)>127forcharinresponse[:10]):
                response=f"{domain_prefixes[domain]} {response}"

returnresponse
