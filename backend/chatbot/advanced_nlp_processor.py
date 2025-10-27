importre
importnltk
importspacy
fromtypingimportList,Dict,Any,Tuple,Optional
fromcollectionsimportCounter
importmath
fromdifflibimportSequenceMatcher
importstring
importnumpyasnp
fromtextblobimportTextBlob
fromsentence_transformersimportSentenceTransformer
importpickle
frompathlibimportPath

try:
    nltk.data.find('tokenizers/punkt')
exceptLookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
exceptLookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
exceptLookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('corpora/wordnet')
exceptLookupError:
    nltk.download('wordnet')

fromnltk.tokenizeimportword_tokenize,sent_tokenize
fromnltk.corpusimportstopwords
fromnltk.stemimportWordNetLemmatizer
fromnltk.tagimportpos_tag

classAdvancedNLPProcessor:
    """Processador de Linguagem Natural avanado com mltiplas tcnicas"""

def__init__(self,model_cache_dir:str="./nlp_models"):
        self.model_cache_dir=Path(model_cache_dir)
self.model_cache_dir.mkdir(exist_ok=True)

try:
            self.nlp=spacy.load("pt_core_news_sm")
exceptOSError:
            print("Modelo spaCy portugus no encontrado. Usando modelo bsico.")
self.nlp=spacy.load("en_core_web_sm")

self.stop_words=set(stopwords.words('portuguese'))
self.stop_words.update(stopwords.words('english'))
self.lemmatizer=WordNetLemmatizer()

self.embedding_model=self._load_embedding_model()

self.category_keywords={
'horario':[
'horrio','horario','trabalho','expediente','entrada','sada','saida',
'intervalo','almoo','almoco','jornada','turno','escala','folga',
'hora','tempo','ponto','presena','presenca'
],
'beneficios':[
'benefcio','beneficio','vale','plano','sade','saude','odontolgico',
'odontologico','gympass','auxlio','auxilio','bonus','bnus','premio',
'prmio','gratificao','gratificacao','adiantamento'
],
'ferias':[
'frias','ferias','adicional','constitucional','perodo','periodo',
'descanso','recesso','licena','licenca','ausncia','ausencia'
],
'licenca':[
'licena','licenca','mdica','medica','atestado','inss','pagamento',
'afastamento','doena','doenca','tratamento','consulta','exame'
],
'vestimenta':[
'vestimenta','roupa','traje','social','casual','informal','uniforme',
'cdigo','codigo','dress','code','apresentao','apresentacao'
],
'comunicacao':[
'comunicao','comunicacao','email','whatsapp','slack','mensagem',
'telefone','reunio','reuniao','meeting','conversa','contato'
],
'seguranca':[
'segurana','seguranca','carto','cartao','acesso','senha','bloquear',
'incidente','violao','violacao','hacker','malware','antivrus',
'antivirus','backup','criptografia'
],
'limpeza':[
'limpeza','organizao','organizacao','mesa','lixo','copa','espao',
'espaco','ambiente','higiene','sanitizao','sanitizacao'
],
'treinamento':[
'treinamento','curso','capacitao','capacitacao','workshop','desenvolvimento',
'aprendizado','educao','educacao','formao','formacao','certificao',
'certificacao','habilidade','competncia','competencia'
],
'rh':[
'recursos','humanos','rh','contratao','contratacao','demisso','demissao',
'admisso','admissao','funcionrio','funcionario','colaborador','empregado',
'salrio','salario','cargo','funo','funcao','departamento'
]
}

self.question_patterns={
'horario':r'(qual|quais|como|quando|que horas).*(horrio|horario|trabalho|expediente|entrada|sada)',
'beneficios':r'(qual|quais|como|quanto).*(benefcio|beneficio|vale|plano|auxlio)',
'ferias':r'(qual|quais|como|quando|quantos).*(frias|ferias|descanso|recesso)',
'licenca':r'(qual|quais|como).*(licena|licenca|mdica|medica|atestado)',
'vestimenta':r'(qual|quais|como).*(vestimenta|roupa|traje|cdigo)',
'comunicacao':r'(qual|quais|como).*(comunicao|comunicacao|email|contato)',
'seguranca':r'(qual|quais|como).*(segurana|seguranca|carto|acesso)',
'limpeza':r'(qual|quais|como).*(limpeza|organizao|organizacao)',
'treinamento':r'(qual|quais|como).*(treinamento|curso|capacitao)',
'rh':r'(qual|quais|como|quem).*(rh|recursos humanos|funcionrio|colaborador)'
}

self.embedding_cache={}
self.cache_file=self.model_cache_dir/"embedding_cache.pkl"
self._load_embedding_cache()

def_load_embedding_model(self):
        """Carrega modelo de embeddings local"""
try:

            model_name="paraphrase-multilingual-MiniLM-L12-v2"
model_path=self.model_cache_dir/model_name

ifmodel_path.exists():
                returnSentenceTransformer(str(model_path))
else:
                print("Baixando modelo de embeddings...")
model=SentenceTransformer(model_name)
model.save(str(model_path))
returnmodel
exceptExceptionase:
            print(f"Erro ao carregar modelo de embeddings: {e}")
returnNone

def_load_embedding_cache(self):
        """Carrega cache de embeddings do disco"""
try:
            ifself.cache_file.exists():
                withopen(self.cache_file,'rb')asf:
                    self.embedding_cache=pickle.load(f)
exceptExceptionase:
            print(f"Erro ao carregar cache de embeddings: {e}")
self.embedding_cache={}

def_save_embedding_cache(self):
        """Salva cache de embeddings no disco"""
try:
            withopen(self.cache_file,'wb')asf:
                pickle.dump(self.embedding_cache,f)
exceptExceptionase:
            print(f"Erro ao salvar cache de embeddings: {e}")

defget_text_embedding(self,text:str)->Optional[np.ndarray]:
        """Obtm embedding de um texto"""
ifnotself.embedding_model:
            returnNone

text_hash=hash(text)
iftext_hashinself.embedding_cache:
            returnself.embedding_cache[text_hash]

try:

            embedding=self.embedding_model.encode([text])[0]

self.embedding_cache[text_hash]=embedding
iflen(self.embedding_cache)>1000:

                keys_to_remove=list(self.embedding_cache.keys())[:100]
forkeyinkeys_to_remove:
                    delself.embedding_cache[key]

returnembedding
exceptExceptionase:
            print(f"Erro ao gerar embedding: {e}")
returnNone

defcalculate_semantic_similarity(self,text1:str,text2:str)->float:
        """Calcula similaridade semntica usando embeddings"""
ifnotself.embedding_model:
            returnself.calculate_similarity(text1,text2)

try:
            emb1=self.get_text_embedding(text1)
emb2=self.get_text_embedding(text2)

ifemb1isnotNoneandemb2isnotNone:

                similarity=np.dot(emb1,emb2)/(np.linalg.norm(emb1)*np.linalg.norm(emb2))
returnfloat(similarity)

exceptExceptionase:
            print(f"Erro no clculo de similaridade semntica: {e}")

return0.0

defpreprocess_text(self,text:str)->str:
        """Preprocessa texto com spaCy"""
try:

            doc=self.nlp(text)

clean_tokens=[]
fortokenindoc:
                ifnottoken.is_stopandnottoken.is_punctandnottoken.is_space:
                    clean_tokens.append(token.lemma_.lower())

return' '.join(clean_tokens)
exceptExceptionase:
            print(f"Erro no preprocessamento spaCy: {e}")

returnself._basic_preprocess(text)

def_basic_preprocess(self,text:str)->str:
        """Preprocessamento bsico como fallback"""
text=text.lower()
text=re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]',' ',text)
text=re.sub(r'\s+',' ',text)
returntext.strip()

defextract_entities(self,text:str)->Dict[str,List[str]]:
        """Extrai entidades nomeadas usando spaCy"""
try:
            doc=self.nlp(text)
entities={
'persons':[],
'organizations':[],
'dates':[],
'numbers':[],
'emails':[],
'urls':[]
}

forentindoc.ents:
                ifent.label_=="PER":
                    entities['persons'].append(ent.text)
elifent.label_=="ORG":
                    entities['organizations'].append(ent.text)
elifent.label_=="DATE":
                    entities['dates'].append(ent.text)

entities['numbers'].extend(re.findall(r'\b\d+(?:\.\d+)?\b',text))
entities['emails'].extend(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',text))
entities['urls'].extend(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text))

returnentities
exceptExceptionase:
            print(f"Erro na extrao de entidades: {e}")
return{'persons':[],'organizations':[],'dates':[],'numbers':[],'emails':[],'urls':[]}

defanalyze_sentiment(self,text:str)->Dict[str,float]:
        """Analisa sentimento do texto"""
try:
            blob=TextBlob(text)
polarity=blob.sentiment.polarity
subjectivity=blob.sentiment.subjectivity

return{
'polarity':polarity,
'subjectivity':subjectivity,
'sentiment':'positive'ifpolarity>0.1else'negative'ifpolarity<-0.1else'neutral'
}
exceptExceptionase:
            print(f"Erro na anlise de sentimento: {e}")
return{'polarity':0.0,'subjectivity':0.0,'sentiment':'neutral'}

defextract_keywords_advanced(self,text:str,max_keywords:int=10)->List[Tuple[str,float]]:
        """Extrai palavras-chave com pontuao usando spaCy"""
try:
            doc=self.nlp(text)

word_scores={}
fortokenindoc:
                if(nottoken.is_stopand
nottoken.is_punctand
nottoken.is_spaceand
len(token.text)>2):

                    pos_score=1.0
iftoken.pos_in['NOUN','PROPN']:
                        pos_score=3.0
eliftoken.pos_in['ADJ']:
                        pos_score=2.0
eliftoken.pos_in['VERB']:
                        pos_score=1.5

freq_score=1.0
iftoken.is_alpha:
                        freq_score=1.2

word=token.lemma_.lower()
word_scores[word]=word_scores.get(word,0)+(pos_score*freq_score)

sorted_words=sorted(word_scores.items(),key=lambdax:x[1],reverse=True)
returnsorted_words[:max_keywords]

exceptExceptionase:
            print(f"Erro na extrao avanada de palavras-chave: {e}")
return[]

defcategorize_question_advanced(self,question:str)->Tuple[str,float]:
        """Categoriza pergunta com pontuao de confiana"""
try:

            doc=self.nlp(question)
question_processed=self.preprocess_text(question)

forcategory,patterninself.question_patterns.items():
                ifre.search(pattern,question_processed,re.IGNORECASE):
                    returncategory,0.9

category_scores={}
question_tokens=set([token.lemma_.lower()fortokenindocifnottoken.is_stop])

forcategory,keywordsinself.category_keywords.items():
                score=0
forkeywordinkeywords:
                    ifkeywordinquestion_tokens:
                        score+=1

ifscore>0:
                    category_scores[category]=score/len(keywords)

ifcategory_scores:
                best_category=max(category_scores,key=category_scores.get)
confidence=category_scores[best_category]
returnbest_category,confidence

return'geral',0.1

exceptExceptionase:
            print(f"Erro na categorizao avanada: {e}")
return'geral',0.0

deffind_relevant_sentences_advanced(self,question:str,document_text:str,max_sentences:int=3)->List[Tuple[str,float]]:
        """Encontra sentenas relevantes com pontuao de relevncia"""
try:

            question_category,confidence=self.categorize_question_advanced(question)

doc=self.nlp(document_text)
sentences=[sent.textforsentindoc.sents]

sentence_scores=[]

forsentenceinsentences:
                score=0.0

semantic_sim=self.calculate_semantic_similarity(question,sentence)
score+=semantic_sim*3.0

ifquestion_category!='geral'andconfidence>0.3:
                    category_keywords=self.category_keywords.get(question_category,[])
forkeywordincategory_keywords:
                        ifkeywordinsentence.lower():
                            score+=2.0*confidence

question_keywords=self.extract_keywords_advanced(question,max_keywords=5)
sentence_keywords=self.extract_keywords_advanced(sentence,max_keywords=10)

question_words=set([kw[0]forkwinquestion_keywords])
sentence_words=set([kw[0]forkwinsentence_keywords])

common_words=question_words.intersection(sentence_words)
score+=len(common_words)*0.5

sentence_scores.append((sentence,score))

sentence_scores.sort(key=lambdax:x[1],reverse=True)

relevant_sentences=[(sent,score)forsent,scoreinsentence_scores[:max_sentences]ifscore>0]

returnrelevant_sentences

exceptExceptionase:
            print(f"Erro na busca avanada de sentenas: {e}")
return[]

defgenerate_advanced_answer(self,question:str,relevant_sentences:List[Tuple[str,float]],context:str="")->str:
        """Gera resposta avanada baseada nas sentenas relevantes"""
ifnotrelevant_sentences:
            return"Desculpe, no encontrei informaes especficas sobre sua pergunta nos documentos disponveis."

sentiment=self.analyze_sentiment(question)

question_category,confidence=self.categorize_question_advanced(question)

best_sentence,best_score=relevant_sentences[0]

ifany(wordinquestion.lower()forwordin['o que','quem','quando','onde','como','por que']):

            ifsentiment['sentiment']=='positive':
                answer=f"tima pergunta! Baseado nos documentos: {best_sentence}"
else:
                answer=f"Baseado nos documentos disponveis: {best_sentence}"
else:

            answer=f"Encontrei esta informao relevante: {best_sentence}"

iflen(relevant_sentences)>1:
            second_sentence,second_score=relevant_sentences[1]
ifsecond_score>0.3:
                answer+=f" Tambm h: {second_sentence}"

ifcontextandlen(relevant_sentences)<2:
            answer+=f" {context}"

returnanswer

defcalculate_similarity(self,text1:str,text2:str)->float:
        """Calcula similaridade bsica entre dois textos"""
text1_clean=self.preprocess_text(text1)
text2_clean=self.preprocess_text(text2)
returnSequenceMatcher(None,text1_clean,text2_clean).ratio()

defis_question(self,text:str)->bool:
        """Verifica se o texto  uma pergunta usando spaCy"""
try:
            doc=self.nlp(text)

iftext.strip().endswith('?'):
                returnTrue

question_words=['o que','quem','quando','onde','como','por que','porque','qual','quais']
text_lower=text.lower()

ifany(text_lower.startswith(word)forwordinquestion_words):
                returnTrue

question_patterns=[
r'voc pode.*\?',
r'voc sabe.*\?',
r' possvel.*\?',
r'como fao.*\?',
r'onde posso.*\?'
]

forpatterninquestion_patterns:
                ifre.search(pattern,text_lower):
                    returnTrue

returnFalse

exceptExceptionase:
            print(f"Erro na verificao de pergunta: {e}")
returnFalse

defsave_cache(self):
        """Salva cache de embeddings"""
self._save_embedding_cache()
