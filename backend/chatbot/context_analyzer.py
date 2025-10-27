importre
importjson
fromtypingimportDict,List,Tuple,Optional,Any
fromdatetimeimportdatetime
importhashlib

classContextAnalyzer:
    """Analisador de contexto inteligente para melhorar respostas do chatbot"""

def__init__(self):

        self.domain_patterns={
"academia":{
"keywords":[
"academia","musculao","ginstica","personal","treino","exerccio",
"spinning","pilates","yoga","crossfit","piscina","sauna","equipamento",
"plano","mensalidade","horrio","aula","instrutor"
],
"questions":[
"horrio de funcionamento","preo","planos","equipamentos","aulas",
"personal trainer","piscina","sauna","estacionamento"
]
},
"supermercado":{
"keywords":[
"supermercado","compra","produto","preo","promoo","oferta",
"delivery","entrega","departamento","hortifrti","aougue","padaria",
"laticnios","bebida","limpeza","farmacia","carto","desconto"
],
"questions":[
"horrio","preos","promoes","delivery","departamentos",
"estacionamento","carto","troca","devoluo"
]
},
"restaurante":{
"keywords":[
"restaurante","cardpio","prato","comida","jantar","almoo",
"reserva","mesa","chef","vinho","drink","sobremesa","menu",
"delivery","takeaway","especialidade","ambiente"
],
"questions":[
"cardpio","preos","horrio","reservas","especialidades",
"delivery","ambiente","vinhos","eventos"
]
},
"empresa":{
"keywords":[
"funcionrio","empresa","trabalho","horrio","benefcio","salrio",
"frias","licena","rh","recursos humanos","poltica","manual",
"vestimenta","comunicao","segurana","treinamento"
],
"questions":[
"horrio de trabalho","benefcios","frias","licena mdica",
"cdigo de vestimenta","comunicao","segurana","treinamentos"
]
}
}

self.intent_patterns={
"informacao":[
"qual","quais","como","quando","onde","por que","o que",
"me fale sobre","explique","informao","detalhes"
],
"preco":[
"preo","valor","quanto custa","quanto ","custa quanto",
"mensalidade","taxa","desconto","promoo","oferta"
],
"horario":[
"horrio","horario","funcionamento","aberto","fechado",
"que horas","at que horas","quando abre","quando fecha"
],
"localizacao":[
"onde fica","endereo","endereco","localizao","localizacao",
"como chegar","prximo","proximo","perto de","distncia"
],
"servico":[
"servio","servico","atendimento","disponvel","disponivel",
"tem","oferece","possui","disponvel","funciona"
]
}

self.analysis_cache={}

defanalyze_question(self,question:str)->Dict[str,Any]:
        """Analisa uma pergunta e retorna contexto, domnio e inteno"""
question_lower=question.lower()

question_hash=hashlib.md5(question_lower.encode()).hexdigest()
ifquestion_hashinself.analysis_cache:
            returnself.analysis_cache[question_hash]

analysis={
"domain":self._detect_domain(question_lower),
"intent":self._detect_intent(question_lower),
"entities":self._extract_entities(question_lower),
"complexity":self._assess_complexity(question_lower),
"urgency":self._assess_urgency(question_lower),
"context_keywords":self._extract_context_keywords(question_lower),
"timestamp":datetime.now().isoformat()
}

self.analysis_cache[question_hash]=analysis

returnanalysis

def_detect_domain(self,question:str)->str:
        """Detecta o domnio da pergunta"""
domain_scores={}

fordomain,patternsinself.domain_patterns.items():
            score=0
forkeywordinpatterns["keywords"]:
                ifkeywordinquestion:
                    score+=1
domain_scores[domain]=score

ifdomain_scores:
            best_domain=max(domain_scores,key=domain_scores.get)
ifdomain_scores[best_domain]>0:
                returnbest_domain

return"geral"

def_detect_intent(self,question:str)->str:
        """Detecta a inteno da pergunta"""
intent_scores={}

forintent,patternsinself.intent_patterns.items():
            score=0
forpatterninpatterns:
                ifpatterninquestion:
                    score+=1
intent_scores[intent]=score

ifintent_scores:
            best_intent=max(intent_scores,key=intent_scores.get)
ifintent_scores[best_intent]>0:
                returnbest_intent

return"geral"

def_extract_entities(self,question:str)->List[str]:
        """Extrai entidades importantes da pergunta"""
entities=[]

numbers=re.findall(r'\b\d+(?:[.,]\d+)?\b',question)
entities.extend([f"numero:{num}"fornuminnumbers])

times=re.findall(r'\b\d{1,2}h\b',question)
entities.extend([f"horario:{time}"fortimeintimes])

days=["segunda","tera","quarta","quinta","sexta","sbado","domingo"]
fordayindays:
            ifdayinquestion:
                entities.append(f"dia:{day}")

if"reais"inquestionor"r$"inquestion:
            entities.append("moeda:reais")

returnentities

def_assess_complexity(self,question:str)->str:
        """Avalia a complexidade da pergunta"""
word_count=len(question.split())

ifword_count<=3:
            return"simples"
elifword_count<=8:
            return"media"
else:
            return"complexa"

def_assess_urgency(self,question:str)->str:
        """Avalia a urgncia da pergunta"""
urgent_words=["urgente","rpido","rapido","agora","imediato","emergncia"]

forwordinurgent_words:
            ifwordinquestion:
                return"alta"

return"normal"

def_extract_context_keywords(self,question:str)->List[str]:
        """Extrai palavras-chave de contexto"""

stop_words={
"o","a","os","as","um","uma","de","da","do","das","dos",
"em","na","no","nas","nos","para","por","com","sem",
"qual","quais","como","quando","onde","porque","que","quem"
}

words=question.split()
keywords=[wordforwordinwordsifwordnotinstop_wordsandlen(word)>2]

returnkeywords[:10]

defgenerate_contextual_response_template(self,analysis:Dict[str,Any])->str:
        """Gera um template de resposta baseado na anlise"""
domain=analysis["domain"]
intent=analysis["intent"]
complexity=analysis["complexity"]

templates={
("academia","preco"):"Aqui esto os preos dos nossos planos de academia:",
("academia","horario"):"Nosso horrio de funcionamento da academia :",
("academia","servico"):"Oferecemos os seguintes servios na academia:",

("supermercado","preco"):"Aqui esto as informaes sobre preos e promoes:",
("supermercado","horario"):"Nosso supermercado funciona no seguinte horrio:",
("supermercado","servico"):"Oferecemos os seguintes servios no supermercado:",

("restaurante","preco"):"Aqui est nosso cardpio com preos:",
("restaurante","horario"):"Nosso restaurante funciona no seguinte horrio:",
("restaurante","servico"):"Oferecemos os seguintes servios no restaurante:",

("empresa","preco"):"Aqui esto as informaes sobre benefcios e remunerao:",
("empresa","horario"):"O horrio de trabalho na empresa :",
("empresa","servico"):"Oferecemos os seguintes benefcios e servios:",
}

template_key=(domain,intent)
iftemplate_keyintemplates:
            returntemplates[template_key]

ifcomplexity=="simples":
            return"Aqui est a informao que voc precisa:"
elifcomplexity=="media":
            return"Vou te explicar detalhadamente:"
else:
            return"Esta  uma pergunta complexa. Vou organizar as informaes para voc:"

defget_domain_specific_enhancements(self,domain:str)->Dict[str,Any]:
        """Retorna melhorias especficas para cada domnio"""
enhancements={
"academia":{
"emoji":"[ACADEMIA]",
"color":"green",
"suggestions":[
"Voc pode agendar uma visita para conhecer nossa estrutura",
"Temos personal trainers disponveis para orientao",
"Oferecemos aulas experimentais gratuitas"
]
},
"supermercado":{
"emoji":"[SUPERMERCADO]",
"color":"blue",
"suggestions":[
"Voc pode fazer pedidos pelo nosso app",
"Temos delivery rpido e seguro",
"Confira nossas promoes da semana"
]
},
"restaurante":{
"emoji":"[RESTAURANTE]",
"color":"orange",
"suggestions":[
"Recomendamos fazer reserva para garantir sua mesa",
"Temos especialidades do chef todas as semanas",
"Oferecemos menu degustao com harmonizao"
]
},
"empresa":{
"emoji":"[EMPRESA]",
"color":"purple",
"suggestions":[
"Para mais detalhes, consulte o RH",
"Temos polticas especficas para cada situao",
"Documentos oficiais esto disponveis na intranet"
]
}
}

returnenhancements.get(domain,{
"emoji":"[INFO]",
"color":"gray",
"suggestions":[]
})

defenhance_response(self,response:str,analysis:Dict[str,Any])->str:
        """Melhora uma resposta baseada na anlise de contexto"""
domain=analysis["domain"]
intent=analysis["intent"]
complexity=analysis.get("complexity","media")
urgency=analysis.get("urgency","normal")

ifdomain=="geral":
            returnresponse

enhancements=self.get_domain_specific_enhancements(domain)
prefix=enhancements["emoji"]

enhanced_response=f"{prefix} {response}"

ifenhancements["suggestions"]andintentin["informacao","servico"]:
            suggestions_text="\n\n**Dicas adicionais:**\n"
forsuggestioninenhancements["suggestions"][:2]:
                suggestions_text+=f" {suggestion}\n"
enhanced_response+=suggestions_text

ifcomplexity=="complexa":
            enhanced_response+="\n\n*Esta  uma pergunta complexa. Se precisar de mais detalhes sobre algum aspecto especfico, posso ajudar!*"
elifcomplexity=="simples":
            enhanced_response+="\n\n*Se precisar de mais informaes sobre este tpico,  s perguntar!*"

ifurgency=="alta":
            enhanced_response+="\n\n*Entendo que  urgente. Se precisar de informaes mais especficas rapidamente, posso ajudar!*"

returnenhanced_response

defget_cache_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache"""
return{
"cache_size":len(self.analysis_cache),
"domains_analyzed":len(set(analysis["domain"]foranalysisinself.analysis_cache.values())),
"intents_analyzed":len(set(analysis["intent"]foranalysisinself.analysis_cache.values()))
}
