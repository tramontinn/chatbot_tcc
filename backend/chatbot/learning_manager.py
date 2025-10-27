importjson
importos
fromtypingimportDict,List,Any,Optional
fromdatetimeimportdatetime
frompathlibimportPath
importhashlib

classLearningManager:
    """Gerencia o aprendizado do chatbot com base nas interaes dos usurios"""

def__init__(self,learning_data_path:str="learning_data"):
        self.learning_data_path=Path(learning_data_path)
self.learning_data_path.mkdir(exist_ok=True)

self.questions_file=self.learning_data_path/"questions_patterns.json"
self.responses_file=self.learning_data_path/"response_templates.json"
self.feedback_file=self.learning_data_path/"user_feedback.json"
self.conversation_file=self.learning_data_path/"conversation_history.json"

self.questions_patterns=self._load_data(self.questions_file,{})
self.response_templates=self._load_data(self.responses_file,{})
self.user_feedback=self._load_data(self.feedback_file,{})
self.conversation_history=self._load_data(self.conversation_file,[])

self._initialize_common_patterns()

def_load_data(self,file_path:Path,default_value:Any)->Any:
        """Carrega dados de um arquivo JSON"""
try:
            iffile_path.exists():
                withopen(file_path,'r',encoding='utf-8')asf:
                    returnjson.load(f)
exceptExceptionase:
            print(f"Erro ao carregar {file_path}: {e}")
returndefault_value

def_save_data(self,file_path:Path,data:Any)->bool:
        """Salva dados em um arquivo JSON"""
try:
            withopen(file_path,'w',encoding='utf-8')asf:
                json.dump(data,f,ensure_ascii=False,indent=2)
returnTrue
exceptExceptionase:
            print(f"Erro ao salvar {file_path}: {e}")
returnFalse

def_initialize_common_patterns(self):
        """Inicializa padres comuns de perguntas"""
ifnotself.questions_patterns:
            self.questions_patterns={
"horario":{
"patterns":[
"qual o horrio de trabalho",
"que horas comea o expediente",
"qual o horrio de entrada",
"quando posso sair",
"qual o horrio do almoo"
],
"keywords":["horrio","horario","trabalho","expediente","entrada","sada","saida","almoo","almoco"],
"frequency":0,
"last_used":None
},
"beneficios":{
"patterns":[
"quais so os benefcios",
"que benefcios tenho",
"qual o valor do vale refeio",
"tem plano de sade",
"quais os benefcios oferecidos"
],
"keywords":["benefcio","beneficio","vale","plano","sade","saude","odontolgico","odontologico"],
"frequency":0,
"last_used":None
},
"ferias":{
"patterns":[
"quantos dias de frias",
"como funciona as frias",
"posso dividir as frias",
"qual o adicional de frias",
"quando posso tirar frias"
],
"keywords":["frias","ferias","adicional","constitucional","perodo","periodo"],
"frequency":0,
"last_used":None
},
"comunicacao":{
"patterns":[
"como entrar em contato com o rh",
"qual o email do rh",
"como se comunicar na empresa",
"quais os canais de comunicao",
"como falar com o departamento"
],
"keywords":["comunicao","comunicacao","email","whatsapp","slack","contato","rh"],
"frequency":0,
"last_used":None
}
}
self._save_data(self.questions_file,self.questions_patterns)

deflearn_from_interaction(self,question:str,response:str,sources:List[str],
session_id:str,user_satisfaction:Optional[int]=None)->bool:
        """Aprende com uma interao do usurio"""
try:

            question_hash=hashlib.md5(question.lower().encode()).hexdigest()

conversation_entry={
"timestamp":datetime.now().isoformat(),
"session_id":session_id,
"question":question,
"response":response,
"sources":sources,
"user_satisfaction":user_satisfaction,
"question_hash":question_hash
}

self.conversation_history.append(conversation_entry)

iflen(self.conversation_history)>1000:
                self.conversation_history=self.conversation_history[-1000:]

self._update_question_patterns(question,question_hash)

self._save_data(self.conversation_file,self.conversation_history)
self._save_data(self.questions_file,self.questions_patterns)

returnTrue

exceptExceptionase:
            print(f"Erro ao aprender com interao: {e}")
returnFalse

def_update_question_patterns(self,question:str,question_hash:str):
        """Atualiza padres de perguntas baseado na pergunta atual"""
question_lower=question.lower()

best_category=None
best_score=0

forcategory,datainself.questions_patterns.items():
            score=0

forkeywordindata["keywords"]:
                ifkeywordinquestion_lower:
                    score+=1

forpatternindata["patterns"]:
                similarity=self._calculate_similarity(question_lower,pattern)
ifsimilarity>0.7:
                    score+=2

ifscore>best_score:
                best_score=score
best_category=category

ifbest_categoryandbest_score>0:
            self.questions_patterns[best_category]["frequency"]+=1
self.questions_patterns[best_category]["last_used"]=datetime.now().isoformat()

ifnotself._is_similar_to_existing_patterns(question_lower,best_category):
                self.questions_patterns[best_category]["patterns"].append(question_lower)

iflen(self.questions_patterns[best_category]["patterns"])>10:
                    self.questions_patterns[best_category]["patterns"]=self.questions_patterns[best_category]["patterns"][-10:]

eliflen(question.split())>=3:
            new_category=f"custom_{len(self.questions_patterns)}"
self.questions_patterns[new_category]={
"patterns":[question_lower],
"keywords":self._extract_keywords(question_lower),
"frequency":1,
"last_used":datetime.now().isoformat()
}

def_is_similar_to_existing_patterns(self,question:str,category:str)->bool:
        """Verifica se a pergunta  similar aos padres existentes"""
forpatterninself.questions_patterns[category]["patterns"]:
            ifself._calculate_similarity(question,pattern)>0.8:
                returnTrue
returnFalse

def_calculate_similarity(self,text1:str,text2:str)->float:
        """Calcula similaridade simples entre dois textos"""
words1=set(text1.split())
words2=set(text2.split())

ifnotwords1ornotwords2:
            return0.0

intersection=words1.intersection(words2)
union=words1.union(words2)

returnlen(intersection)/len(union)ifunionelse0.0

def_extract_keywords(self,text:str)->List[str]:
        """Extrai palavras-chave simples do texto"""

stop_words={
"o","a","os","as","um","uma","uns","umas","de","da","do","das","dos",
"em","na","no","nas","nos","para","por","com","sem","sobre","sob",
"qual","quais","como","quando","onde","porque","por que","que","quem",
"","so","tem","tm","posso","pode","poder","fazer","ter","ser"
}

words=text.split()
keywords=[wordforwordinwordsifwordnotinstop_wordsandlen(word)>2]

returnkeywords[:5]

defget_improved_response(self,question:str,original_response:str)->str:
        """Melhora a resposta baseada no aprendizado"""
try:
            question_lower=question.lower()

similar_responses=[]

forentryinself.conversation_history[-100:]:
                satisfaction=entry.get("user_satisfaction")
ifsatisfactionisnotNoneandsatisfaction>=4:
                    similarity=self._calculate_similarity(question_lower,entry["question"].lower())
ifsimilarity>0.6:
                        similar_responses.append({
"response":entry["response"],
"similarity":similarity,
"satisfaction":satisfaction
})

ifsimilar_responses:

                similar_responses.sort(key=lambdax:(x.get("satisfaction",0),x.get("similarity",0)),reverse=True)
best_response=similar_responses[0]["response"]

ifbest_response!=original_response:
                    returnf"{original_response}\n\n **Dica baseada em perguntas similares:** {best_response}"

question_category=self._categorize_question(question_lower)
ifquestion_categoryandquestion_categoryinself.questions_patterns:
                category_data=self.questions_patterns[question_category]

ifcategory_data["frequency"]>5:
                    returnf"{original_response}\n\n *Esta  uma pergunta comum! Se precisar de mais detalhes, posso ajudar com informaes especficas.*"

returnoriginal_response

exceptExceptionase:
            print(f"Erro ao melhorar resposta: {e}")
returnoriginal_response

def_categorize_question(self,question:str)->Optional[str]:
        """Categoriza uma pergunta baseada nos padres aprendidos"""
best_category=None
best_score=0

forcategory,datainself.questions_patterns.items():
            score=0

forkeywordindata["keywords"]:
                ifkeywordinquestion:
                    score+=1

forpatternindata["patterns"]:
                similarity=self._calculate_similarity(question,pattern)
ifsimilarity>0.7:
                    score+=2

ifscore>best_score:
                best_score=score
best_category=category

returnbest_categoryifbest_score>0elseNone

defget_learning_stats(self)->Dict[str,Any]:
        """Retorna estatsticas de aprendizado"""
total_interactions=len(self.conversation_history)

iftotal_interactions==0:
            return{"total_interactions":0}

category_frequency={}
forcategory,datainself.questions_patterns.items():
            category_frequency[category]=data["frequency"]

most_popular=sorted(category_frequency.items(),key=lambdax:x[1],reverse=True)[:5]

satisfaction_scores=[entry["user_satisfaction"]forentryinself.conversation_history
ifentry.get("user_satisfaction")isnotNone]

avg_satisfaction=sum(satisfaction_scores)/len(satisfaction_scores)ifsatisfaction_scoreselseNone

return{
"total_interactions":total_interactions,
"total_categories":len(self.questions_patterns),
"most_popular_categories":most_popular,
"average_satisfaction":avg_satisfaction,
"last_learning":self.conversation_history[-1]["timestamp"]ifself.conversation_historyelseNone
}

defrecord_user_feedback(self,session_id:str,question:str,response:str,
satisfaction:int,feedback_text:Optional[str]=None)->bool:
        """Registra feedback do usurio"""
try:
            feedback_entry={
"timestamp":datetime.now().isoformat(),
"session_id":session_id,
"question":question,
"response":response,
"satisfaction":satisfaction,
"feedback_text":feedback_text
}

if"feedback_history"notinself.user_feedback:
                self.user_feedback["feedback_history"]=[]

self.user_feedback["feedback_history"].append(feedback_entry)

iflen(self.user_feedback["feedback_history"])>500:
                self.user_feedback["feedback_history"]=self.user_feedback["feedback_history"][-500:]

if"satisfaction_stats"notinself.user_feedback:
                self.user_feedback["satisfaction_stats"]={
"total_feedback":0,
"average_satisfaction":0.0,
"satisfaction_distribution":{1:0,2:0,3:0,4:0,5:0}
}

stats=self.user_feedback["satisfaction_stats"]
stats["total_feedback"]+=1
stats["satisfaction_distribution"][satisfaction]+=1

total_score=sum(score*countforscore,countinstats["satisfaction_distribution"].items())
stats["average_satisfaction"]=total_score/stats["total_feedback"]

returnself._save_data(self.feedback_file,self.user_feedback)

exceptExceptionase:
            print(f"Erro ao registrar feedback: {e}")
returnFalse
