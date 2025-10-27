
importrandom
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime

classIntelligentFallbackSystem:
    """Sistema que garante que o chatbot sempre tenha uma resposta til"""

def__init__(self):

        self.fallback_responses={
"greeting":[
"Ol!  Como posso ajud-lo hoje?",
"Oi!  Estou aqui para esclarecer suas dvidas!",
"Ol!  Bem-vindo! Em que posso ser til?",
"Oi!  Fico feliz em conversar com voc!",
"Ol!  Como posso tornar seu dia melhor?"
],
"farewell":[
"At logo!  Foi um prazer conversar com voc!",
"Tchau!  Espero ter ajudado! Volte sempre!",
"At a prxima!  Tenha um timo dia!",
"At mais!  Foi timo conversar com voc!",
"At logo!  Foi um prazer ajud-lo!"
],
"thanks":[
"De nada!  Fico feliz em ajudar!",
"Por nada!  Estou aqui para isso!",
"Disponha!  Qualquer dvida,  s perguntar!",
"De nada!  Foi um prazer ajud-lo!",
"Por nada!  Estou sempre  disposio!"
],
"confusion":[
"Desculpe, no consegui entender completamente. Poderia reformular sua pergunta? ",
"Interessante pergunta! Poderia ser mais especfico para que eu possa ajud-lo melhor? ",
"No tenho certeza se entendi. Voc poderia explicar de outra forma? ",
"Essa  uma pergunta interessante! Poderia dar mais detalhes? ",
"Hmm, no consegui captar exatamente o que voc precisa. Pode tentar de outra forma? "
],
"encouragement":[
"No se preocupe! Vamos encontrar a resposta juntos! ",
"tima pergunta! Vou fazer o meu melhor para ajud-lo! ",
"Entendo sua dvida! Vamos resolver isso! ",
"No desista! Estou aqui para ajudar! ",
"Vamos juntos descobrir a melhor resposta! "
],
"general_help":[
"Posso ajud-lo com informaes sobre horrios, preos, servios e muito mais! ",
"Estou aqui para esclarecer dvidas sobre nossos produtos e servios! ",
"Posso responder perguntas sobre funcionamento, benefcios e procedimentos! ",
"Estou disponvel para ajudar com qualquer informao que precisar! ",
"Sou especialista em responder perguntas sobre nossos servios! "
],
"suggestion":[
"Que tal tentar uma pergunta mais especfica? ",
"Voc pode perguntar sobre horrios, preos ou servios! ",
"Tente ser mais especfico sobre o que precisa saber! ",
"Posso ajudar melhor se voc for mais detalhado! ",
"Seja especfico na sua pergunta para obter a melhor resposta! "
]
}

self.smart_patterns={
"what_are_you":[
"Sou um assistente virtual inteligente!  Estou aqui para ajud-lo com informaes sobre nossos servios, produtos e procedimentos.",
"Ol! Sou seu assistente pessoal!  Posso esclarecer dvidas, fornecer informaes e ajudar com o que precisar!",
"Sou um chatbot especializado em atendimento!  Meu objetivo  tornar sua experincia mais fcil e informativa!"
],
"what_can_you_do":[
"Posso ajud-lo com vrias coisas! ",
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
],
"how_are_you":[
"Estou muito bem, obrigado por perguntar!  E voc, como est?",
"timo! Estou aqui funcionando perfeitamente para ajud-lo! ",
"Muito bem! Pronto para esclarecer suas dvidas! ",
"Excelente! Estou animado para conversar com voc! ",
"Perfeito! Estou aqui e funcionando 100%! "
]
}

self.contextual_responses={
"horario":[
"Sobre horrios, posso ajud-lo! ",
"Para informaes sobre horrios, recomendo entrar em contato diretamente ou verificar nossos documentos.",
"Horrios podem variar. Posso orient-lo sobre como obter informaes atualizadas! "
],
"preco":[
"Sobre preos, posso orient-lo! ",
"Para informaes sobre preos, recomendo verificar nossos planos disponveis.",
"Preos podem variar conforme promoes. Posso ajudar com informaes gerais! "
],
"servico":[
"Sobre servios, posso explicar! ",
"Temos diversos servios disponveis. Posso detalhar os principais para voc!",
"Servios so nossa especialidade! Posso orient-lo sobre o que oferecemos! "
],
"contato":[
"Para contato, posso orient-lo! ",
"Recomendo entrar em contato diretamente para informaes especficas.",
"Posso ajud-lo a encontrar a melhor forma de contato! "
]
}

defget_intelligent_fallback(self,question:str,context:str="",domain:str="geral")->str:
        """Gera resposta de fallback inteligente baseada na pergunta"""

question_lower=question.lower().strip()

specific_response=self._check_specific_patterns(question_lower)
ifspecific_response:
            returnspecific_response

contextual_response=self._check_contextual_responses(question_lower)
ifcontextual_response:
            returncontextual_response

ifself._is_too_generic(question_lower):
            returnself._handle_generic_question(domain)

ifself._is_confusing_question(question_lower):
            returnrandom.choice(self.fallback_responses["confusion"])

returnself._generate_domain_fallback(question,domain)

def_check_specific_patterns(self,question:str)->Optional[str]:
        """Verifica padres especficos de perguntas"""

ifany(phraseinquestionforphrasein["o que voc ","quem  voc"]):
            returnrandom.choice(self.smart_patterns["what_are_you"])

ifany(phraseinquestionforphrasein["o que voc pode fazer","como voc pode ajudar"]):
            return"\n".join(self.smart_patterns["what_can_you_do"])

ifany(phraseinquestionforphrasein["ajuda","help","como usar"]):
            return"\n".join(self.smart_patterns["help"])

ifany(phraseinquestionforphrasein["como voc est","tudo bem","como vai"]):
            returnrandom.choice(self.smart_patterns["how_are_you"])

returnNone

def_check_contextual_responses(self,question:str)->Optional[str]:
        """Verifica respostas contextuais baseadas em palavras-chave"""

forkeyword,responsesinself.contextual_responses.items():
            ifkeywordinquestion:
                returnrandom.choice(responses)

returnNone

def_is_too_generic(self,question:str)->bool:
        """Verifica se a pergunta  muito genrica"""

generic_patterns=[
len(question.split())<=2,
questionin["oi","ol","ola","oi","hey","ei"],
questionin["ajuda","help","socorro"],
questionin["o que","como","quando","onde","por que"]
]

returnany(generic_patterns)

def_is_confusing_question(self,question:str)->bool:
        """Verifica se a pergunta  confusa ou mal formulada"""

confusing_patterns=[
len(question.split())>20,
question.count("?")>2,
"no sei"inquestion,
"confuso"inquestion,
"no entendi"inquestion
]

returnany(confusing_patterns)

def_handle_generic_question(self,domain:str)->str:
        """Lida com perguntas muito genricas"""

base_response=random.choice(self.fallback_responses["general_help"])

ifdomain!="geral":
            domain_specific=self._get_domain_specific_guidance(domain)
returnf"{base_response}\n\n{domain_specific}"

returnf"{base_response}\n\n{random.choice(self.fallback_responses['suggestion'])}"

def_get_domain_specific_guidance(self,domain:str)->str:
        """Retorna orientao especfica do domnio"""

domain_guidance={
"academia":" **Sobre a Academia:** Posso ajudar com horrios, planos, equipamentos e aulas!",
"supermercado":" **Sobre o Supermercado:** Posso ajudar com horrios, promoes e delivery!",
"restaurante":" **Sobre o Restaurante:** Posso ajudar com cardpio, horrios e reservas!",
"empresa":"**Sobre a Empresa:** Posso ajudar com beneficios, horarios e politicas!"
}

returndomain_guidance.get(domain," **Dica:** Seja especfico na sua pergunta para obter a melhor resposta!")

def_generate_domain_fallback(self,question:str,domain:str)->str:
        """Gera resposta de fallback baseada no domnio"""

topic=self._extract_topic(question)

base_responses=[
f"Entendo sua pergunta sobre '{topic}'. Embora no tenha essa informao especfica no momento, posso ajud-lo de outras formas! ",
f"tima pergunta sobre '{topic}'! Para informaes mais detalhadas, recomendo entrar em contato diretamente. ",
f"Sobre '{topic}', no tenho essa informao especfica agora. Mas posso ajudar com outras questes relacionadas! "
]

response=random.choice(base_responses)

ifdomain!="geral":
            domain_guidance=self._get_domain_specific_guidance(domain)
response+=f"\n\n{domain_guidance}"

suggestions=[
" **Voc pode:**",
" Reformular sua pergunta de outra forma",
" Fazer uma pergunta mais especfica",
" Perguntar sobre outros tpicos relacionados",
" Entrar em contato diretamente para informaes especficas"
]

response+=f"\n\n{chr(10).join(suggestions)}"

returnresponse

def_extract_topic(self,question:str)->str:
        """Extrai o tpico principal da pergunta"""

stop_words={
"qual","quais","como","quando","onde","por que","porque","o que","que",
"voc","pode","me","falar","sobre","de","da","do","das","dos",
"","so","tem","tm","posso","pode","poder","fazer","ter","ser"
}

words=question.lower().split()
topic_words=[wordforwordinwordsifwordnotinstop_wordsandlen(word)>2]

iftopic_words:
            return" ".join(topic_words[:3])

return"sua pergunta"

defget_encouragement_response(self)->str:
        """Retorna resposta de encorajamento"""
returnrandom.choice(self.fallback_responses["encouragement"])

defget_social_response(self,interaction_type:str)->str:
        """Retorna resposta social apropriada"""
returnrandom.choice(self.fallback_responses.get(interaction_type,self.fallback_responses["general_help"]))

defenhance_with_emojis(self,response:str,domain:str="geral")->str:
        """Adiciona emojis apropriados  resposta"""

ifany(ord(char)>127forcharinresponse[:20]):
            returnresponse

domain_prefixes={
"academia":"[ACADEMIA]",
"supermercado":"[SUPERMERCADO]",
"restaurante":"[RESTAURANTE]",
"empresa":"[EMPRESA]"
}

prefix=domain_prefixes.get(domain,"[INFO]")
returnf"{prefix} {response}"
