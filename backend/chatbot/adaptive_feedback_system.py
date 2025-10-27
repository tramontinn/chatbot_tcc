
importjson
importos
importtime
importsqlite3
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime,timedelta
fromcollectionsimportdefaultdict,Counter
importlogging
importnumpyasnp
fromdataclassesimportdataclass,asdict
importpickle
frompathlibimportPath

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

@dataclass
classFeedbackEntry:
    """Entrada de feedback do usurio"""
id:str
session_id:str
question:str
original_response:str
satisfaction:int
feedback_text:Optional[str]=None
timestamp:float=None
category:Optional[str]=None
improved_response:Optional[str]=None
improvement_applied:bool=False

def__post_init__(self):
        ifself.timestampisNone:
            self.timestamp=time.time()

@dataclass
classResponsePattern:
    """Padro de resposta identificado"""
pattern_id:str
question_pattern:str
response_template:str
success_rate:float
usage_count:int
last_used:float
category:str
confidence:float

@dataclass
classImprovementSuggestion:
    """Sugesto de melhoria para resposta"""
suggestion_id:str
question_type:str
current_response:str
suggested_response:str
improvement_type:str
confidence:float
feedback_count:int

classAdaptiveFeedbackSystem:
    """Sistema que aprende e adapta respostas baseado no feedback"""

def__init__(self,data_dir:str="./learning_data"):
        self.data_dir=Path(data_dir)
self.data_dir.mkdir(exist_ok=True)

self.feedback_db=self.data_dir/"feedback.db"
self.patterns_file=self.data_dir/"response_patterns.json"
self.improvements_file=self.data_dir/"improvement_suggestions.json"
self.learning_stats_file=self.data_dir/"learning_stats.json"

self._init_database()

self.response_patterns:Dict[str,ResponsePattern]={}
self.improvement_suggestions:Dict[str,ImprovementSuggestion]={}
self.learning_stats=self._load_learning_stats()

self._load_patterns()
self._load_improvements()

self.min_feedback_threshold=3
self.success_rate_threshold=0.7
self.learning_rate=0.1

logger.info("Sistema de feedback adaptativo inicializado")

def_init_database(self):
        """Inicializa banco de dados SQLite para feedback"""
try:
            withsqlite3.connect(self.feedback_db)asconn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS feedback_entries (
                        id TEXT PRIMARY KEY,
                        session_id TEXT,
                        question TEXT,
                        original_response TEXT,
                        satisfaction INTEGER,
                        feedback_text TEXT,
                        timestamp REAL,
                        category TEXT,
                        improved_response TEXT,
                        improvement_applied INTEGER DEFAULT 0
                    )
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_session_id ON feedback_entries(session_id)
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_timestamp ON feedback_entries(timestamp)
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_satisfaction ON feedback_entries(satisfaction)
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_category ON feedback_entries(category)
                '''
)

conn.commit()
exceptExceptionase:
            logger.error(f"Erro ao inicializar banco de dados: {e}")

defrecord_feedback(self,session_id:str,question:str,response:str,
satisfaction:int,feedback_text:Optional[str]=None,
category:Optional[str]=None)->str:
        """Registra feedback do usurio"""
try:
            feedback_id=f"fb_{int(time.time()*1000)}_{hash(question)%10000}"

feedback_entry=FeedbackEntry(
id=feedback_id,
session_id=session_id,
question=question,
original_response=response,
satisfaction=satisfaction,
feedback_text=feedback_text,
category=category
)

withsqlite3.connect(self.feedback_db)asconn:
                conn.execute('''
                    INSERT INTO feedback_entries 
                    (id, session_id, question, original_response, satisfaction, 
                     feedback_text, timestamp, category, improved_response, improvement_applied)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
,(
feedback_entry.id,feedback_entry.session_id,feedback_entry.question,
feedback_entry.original_response,feedback_entry.satisfaction,
feedback_entry.feedback_text,feedback_entry.timestamp,
feedback_entry.category,feedback_entry.improved_response,
feedback_entry.improvement_applied
))
conn.commit()

self._process_feedback(feedback_entry)

self._update_learning_stats(feedback_entry)

logger.info(f"Feedback registrado: {feedback_id} (satisfao: {satisfaction})")
returnfeedback_id

exceptExceptionase:
            logger.error(f"Erro ao registrar feedback: {e}")
return""

def_process_feedback(self,feedback:FeedbackEntry):
        """Processa feedback para identificar padres e melhorias"""
try:

            iffeedback.satisfaction>=4:
                self._learn_from_positive_feedback(feedback)
eliffeedback.satisfaction<=2:
                self._learn_from_negative_feedback(feedback)

question_pattern=self._extract_question_pattern(feedback.question)
ifquestion_pattern:
                self._update_response_pattern(question_pattern,feedback)

iffeedback.satisfaction<=2andfeedback.feedback_text:
                self._generate_improvement_suggestion(feedback)

exceptExceptionase:
            logger.error(f"Erro ao processar feedback: {e}")

def_learn_from_positive_feedback(self,feedback:FeedbackEntry):
        """Aprende com feedback positivo"""
question_pattern=self._extract_question_pattern(feedback.question)
ifquestion_pattern:
            pattern_id=f"pattern_{hash(question_pattern)%10000}"

ifpattern_idinself.response_patterns:

                pattern=self.response_patterns[pattern_id]
pattern.usage_count+=1
pattern.success_rate=(pattern.success_rate*(pattern.usage_count-1)+1.0)/pattern.usage_count
pattern.last_used=time.time()
else:

                self.response_patterns[pattern_id]=ResponsePattern(
pattern_id=pattern_id,
question_pattern=question_pattern,
response_template=feedback.original_response,
success_rate=1.0,
usage_count=1,
last_used=time.time(),
category=feedback.categoryor"geral",
confidence=0.8
)

def_learn_from_negative_feedback(self,feedback:FeedbackEntry):
        """Aprende com feedback negativo"""
question_pattern=self._extract_question_pattern(feedback.question)
ifquestion_pattern:
            pattern_id=f"pattern_{hash(question_pattern)%10000}"

ifpattern_idinself.response_patterns:

                pattern=self.response_patterns[pattern_id]
pattern.usage_count+=1
pattern.success_rate=(pattern.success_rate*(pattern.usage_count-1)+0.0)/pattern.usage_count
pattern.last_used=time.time()

def_extract_question_pattern(self,question:str)->Optional[str]:
        """Extrai padro da pergunta"""
try:

            question_lower=question.lower().strip()

importre
question_clean=re.sub(r'[^\w\s]','',question_lower)

keywords=[]
important_words=[
'horrio','horario','trabalho','expediente','entrada','sada',
'benefcio','beneficio','vale','plano','sade','saude',
'frias','ferias','descanso','recesso',
'licena','licenca','mdica','medica','atestado',
'vestimenta','roupa','traje','cdigo','codigo',
'comunicao','comunicacao','email','contato',
'segurana','seguranca','carto','cartao','acesso',
'limpeza','organizao','organizacao',
'treinamento','curso','capacitao','capacitacao',
'rh','recursos','humanos','funcionrio','funcionario'
]

forwordinimportant_words:
                ifwordinquestion_clean:
                    keywords.append(word)

ifkeywords:
                returnf"question_about_{'_'.join(keywords[:3])}"

returnNone

exceptExceptionase:
            logger.error(f"Erro ao extrair padro da pergunta: {e}")
returnNone

def_update_response_pattern(self,question_pattern:str,feedback:FeedbackEntry):
        """Atualiza padro de resposta"""
pattern_id=f"pattern_{hash(question_pattern)%10000}"

ifpattern_idinself.response_patterns:
            pattern=self.response_patterns[pattern_id]

iffeedback.satisfaction>=4:

                current_template=pattern.response_template
new_response=feedback.original_response

iflen(new_response)>len(current_template)*1.2:
                    pattern.response_template=new_response
pattern.confidence=min(pattern.confidence+0.1,1.0)

def_generate_improvement_suggestion(self,feedback:FeedbackEntry):
        """Gera sugesto de melhoria baseada no feedback negativo"""
try:
            suggestion_id=f"suggestion_{int(time.time()*1000)}_{hash(feedback.question)%10000}"

improvement_type=self._analyze_improvement_type(feedback)

improved_response=self._generate_improved_response(feedback,improvement_type)

suggestion=ImprovementSuggestion(
suggestion_id=suggestion_id,
question_type=self._extract_question_pattern(feedback.question)or"geral",
current_response=feedback.original_response,
suggested_response=improved_response,
improvement_type=improvement_type,
confidence=0.7,
feedback_count=1
)

self.improvement_suggestions[suggestion_id]=suggestion

self._save_improvements()

exceptExceptionase:
            logger.error(f"Erro ao gerar sugesto de melhoria: {e}")

def_analyze_improvement_type(self,feedback:FeedbackEntry)->str:
        """Analisa tipo de melhoria necessria baseada no feedback"""
ifnotfeedback.feedback_text:
            return"completeness"

feedback_lower=feedback.feedback_text.lower()

ifany(wordinfeedback_lowerforwordin['claro','confuso','entender','explicar']):
            return"clarity"
elifany(wordinfeedback_lowerforwordin['completo','mais','detalhes','informao']):
            return"completeness"
elifany(wordinfeedback_lowerforwordin['tom','formal','informal','amigvel']):
            return"tone"
elifany(wordinfeedback_lowerforwordin['errado','incorreto','atualizado','preciso']):
            return"accuracy"
else:
            return"completeness"

def_generate_improved_response(self,feedback:FeedbackEntry,improvement_type:str)->str:
        """Gera resposta melhorada baseada no tipo de melhoria"""
original=feedback.original_response

ifimprovement_type=="clarity":
            returnself._improve_clarity(original)
elifimprovement_type=="completeness":
            returnself._improve_completeness(original,feedback.question)
elifimprovement_type=="tone":
            returnself._improve_tone(original)
elifimprovement_type=="accuracy":
            returnself._improve_accuracy(original)
else:
            returnoriginal

def_improve_clarity(self,response:str)->str:
        """Melhora clareza da resposta"""

ifnotresponse.startswith(('Baseado','Com base','Segundo','De acordo')):
            response=f"Com base nas informaes disponveis: {response}"

iflen(response)>200:
            sentences=response.split('. ')
iflen(sentences)>2:
                response='. '.join(sentences[:2])+'.\n\n'+'. '.join(sentences[2:])

returnresponse

def_improve_completeness(self,response:str,question:str)->str:
        """Melhora completude da resposta"""

question_lower=question.lower()

ifany(wordinquestion_lowerforwordin['horrio','horario','trabalho']):
            response+="\n\nPara mais informaes sobre horrios especiais ou excees, consulte o RH."
elifany(wordinquestion_lowerforwordin['benefcio','beneficio','vale']):
            response+="\n\nPara esclarecimentos sobre benefcios especficos, entre em contato com o departamento de RH."
elifany(wordinquestion_lowerforwordin['frias','ferias']):
            response+="\n\nLembre-se de planejar suas frias com antecedncia e comunicar ao RH."

returnresponse

def_improve_tone(self,response:str)->str:
        """Melhora tom da resposta"""

ifnotany(wordinresponse.lower()forwordin['obrigado','disponha','prazer']):
            response+="\n\nFico  disposio para esclarecer outras dvidas!"

returnresponse

def_improve_accuracy(self,response:str)->str:
        """Melhora preciso da resposta"""

if'atualizado'notinresponse.lower():
            response+="\n\n*Informaes sujeitas a alteraes. Para dados mais recentes, consulte a documentao oficial."

returnresponse

defget_improved_response(self,question:str,original_response:str,
category:Optional[str]=None)->str:
        """Obtm resposta melhorada baseada no aprendizado"""
try:

            question_pattern=self._extract_question_pattern(question)
ifquestion_pattern:
                pattern_id=f"pattern_{hash(question_pattern)%10000}"

ifpattern_idinself.response_patterns:
                    pattern=self.response_patterns[pattern_id]

ifpattern.success_rate>=self.success_rate_threshold:
                        returnpattern.response_template

relevant_suggestions=[]
forsuggestioninself.improvement_suggestions.values():
                ifsuggestion.question_type==question_patternorsuggestion.question_type=="geral":
                    ifsuggestion.confidence>=0.6:
                        relevant_suggestions.append(suggestion)

ifrelevant_suggestions:

                best_suggestion=max(relevant_suggestions,key=lambdas:s.confidence)
returnbest_suggestion.suggested_response

returnoriginal_response

exceptExceptionase:
            logger.error(f"Erro ao obter resposta melhorada: {e}")
returnoriginal_response

defget_learning_insights(self)->Dict[str,Any]:
        """Retorna insights de aprendizado"""
try:

            feedback_stats=self._get_feedback_stats()

successful_patterns=[
{
'pattern':pattern.question_pattern,
'success_rate':pattern.success_rate,
'usage_count':pattern.usage_count,
'category':pattern.category
}
forpatterninself.response_patterns.values()
ifpattern.success_rate>=self.success_rate_threshold
]
successful_patterns.sort(key=lambdax:x['success_rate'],reverse=True)

improvement_areas=defaultdict(int)
forsuggestioninself.improvement_suggestions.values():
                improvement_areas[suggestion.improvement_type]+=suggestion.feedback_count

low_satisfaction_categories=self._get_low_satisfaction_categories()

return{
'feedback_stats':feedback_stats,
'successful_patterns':successful_patterns[:5],
'improvement_areas':dict(improvement_areas),
'low_satisfaction_categories':low_satisfaction_categories,
'total_patterns':len(self.response_patterns),
'total_suggestions':len(self.improvement_suggestions),
'learning_rate':self.learning_rate
}

exceptExceptionase:
            logger.error(f"Erro ao obter insights de aprendizado: {e}")
return{}

def_get_feedback_stats(self)->Dict[str,Any]:
        """Obtm estatsticas de feedback"""
try:
            withsqlite3.connect(self.feedback_db)asconn:
                cursor=conn.execute('''
                    SELECT 
                        COUNT(*) as total,
                        AVG(satisfaction) as avg_satisfaction,
                        COUNT(CASE WHEN satisfaction >= 4 THEN 1 END) as positive_count,
                        COUNT(CASE WHEN satisfaction <= 2 THEN 1 END) as negative_count
                    FROM feedback_entries
                '''
)

row=cursor.fetchone()
ifrow:
                    total,avg_satisfaction,positive_count,negative_count=row
return{
'total_feedback':total,
'average_satisfaction':round(avg_satisfactionor0,2),
'positive_feedback':positive_count,
'negative_feedback':negative_count,
'positive_rate':round((positive_count/total*100)iftotal>0else0,1)
}

return{}

exceptExceptionase:
            logger.error(f"Erro ao obter estatsticas de feedback: {e}")
return{}

def_get_low_satisfaction_categories(self)->List[Dict[str,Any]]:
        """Obtm categorias com menor satisfao"""
try:
            withsqlite3.connect(self.feedback_db)asconn:
                cursor=conn.execute('''
                    SELECT 
                        category,
                        COUNT(*) as count,
                        AVG(satisfaction) as avg_satisfaction
                    FROM feedback_entries 
                    WHERE category IS NOT NULL
                    GROUP BY category
                    HAVING COUNT(*) >= 3
                    ORDER BY avg_satisfaction ASC
                    LIMIT 5
                '''
)

results=[]
forrowincursor.fetchall():
                    category,count,avg_satisfaction=row
results.append({
'category':category,
'count':count,
'avg_satisfaction':round(avg_satisfaction,2)
})

returnresults

exceptExceptionase:
            logger.error(f"Erro ao obter categorias com baixa satisfao: {e}")
return[]

def_update_learning_stats(self,feedback:FeedbackEntry):
        """Atualiza estatsticas de aprendizado"""
try:
            self.learning_stats['total_feedback']=self.learning_stats.get('total_feedback',0)+1
self.learning_stats['last_feedback']=feedback.timestamp

current_avg=self.learning_stats.get('avg_satisfaction',0)
total=self.learning_stats['total_feedback']
new_avg=(current_avg*(total-1)+feedback.satisfaction)/total
self.learning_stats['avg_satisfaction']=new_avg

self._save_learning_stats()

exceptExceptionase:
            logger.error(f"Erro ao atualizar estatsticas de aprendizado: {e}")

def_load_patterns(self):
        """Carrega padres de resposta"""
try:
            ifself.patterns_file.exists():
                withopen(self.patterns_file,'r',encoding='utf-8')asf:
                    data=json.load(f)
self.response_patterns={
k:ResponsePattern(**v)fork,vindata.items()
}
exceptExceptionase:
            logger.error(f"Erro ao carregar padres: {e}")
self.response_patterns={}

def_save_patterns(self):
        """Salva padres de resposta"""
try:
            data={k:asdict(v)fork,vinself.response_patterns.items()}
withopen(self.patterns_file,'w',encoding='utf-8')asf:
                json.dump(data,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            logger.error(f"Erro ao salvar padres: {e}")

def_load_improvements(self):
        """Carrega sugestes de melhoria"""
try:
            ifself.improvements_file.exists():
                withopen(self.improvements_file,'r',encoding='utf-8')asf:
                    data=json.load(f)
self.improvement_suggestions={
k:ImprovementSuggestion(**v)fork,vindata.items()
}
exceptExceptionase:
            logger.error(f"Erro ao carregar sugestes: {e}")
self.improvement_suggestions={}

def_save_improvements(self):
        """Salva sugestes de melhoria"""
try:
            data={k:asdict(v)fork,vinself.improvement_suggestions.items()}
withopen(self.improvements_file,'w',encoding='utf-8')asf:
                json.dump(data,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            logger.error(f"Erro ao salvar sugestes: {e}")

def_load_learning_stats(self)->Dict[str,Any]:
        """Carrega estatsticas de aprendizado"""
try:
            ifself.learning_stats_file.exists():
                withopen(self.learning_stats_file,'r',encoding='utf-8')asf:
                    returnjson.load(f)
exceptExceptionase:
            logger.error(f"Erro ao carregar estatsticas: {e}")

return{}

def_save_learning_stats(self):
        """Salva estatsticas de aprendizado"""
try:
            withopen(self.learning_stats_file,'w',encoding='utf-8')asf:
                json.dump(self.learning_stats,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            logger.error(f"Erro ao salvar estatsticas: {e}")

defcleanup_old_data(self,days:int=90):
        """Remove dados antigos"""
try:
            cutoff_time=time.time()-(days*24*60*60)

withsqlite3.connect(self.feedback_db)asconn:
                cursor=conn.execute('DELETE FROM feedback_entries WHERE timestamp < ?',(cutoff_time,))
deleted_count=cursor.rowcount
conn.commit()

old_patterns=[
pattern_idforpattern_id,patterninself.response_patterns.items()
ifpattern.last_used<cutoff_timeandpattern.usage_count<5
]

forpattern_idinold_patterns:
                delself.response_patterns[pattern_id]

ifold_patterns:
                self._save_patterns()

logger.info(f"Limpeza concluda: {deleted_count} feedbacks removidos, {len(old_patterns)} padres removidos")

exceptExceptionase:
            logger.error(f"Erro na limpeza de dados: {e}")

defexport_learning_data(self,output_file:str):
        """Exporta dados de aprendizado"""
try:
            export_data={
'patterns':{k:asdict(v)fork,vinself.response_patterns.items()},
'suggestions':{k:asdict(v)fork,vinself.improvement_suggestions.items()},
'stats':self.learning_stats,
'export_timestamp':time.time()
}

withopen(output_file,'w',encoding='utf-8')asf:
                json.dump(export_data,f,ensure_ascii=False,indent=2)

logger.info(f"Dados de aprendizado exportados para: {output_file}")

exceptExceptionase:
            logger.error(f"Erro ao exportar dados: {e}")

adaptive_feedback_system=AdaptiveFeedbackSystem()
