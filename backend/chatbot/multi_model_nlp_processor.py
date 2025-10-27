
importos
importre
importnltk
importspacy
fromtypingimportList,Dict,Any,Tuple,Optional,Union
fromcollectionsimportCounter
importmath
importnumpyasnp
fromtextblobimportTextBlob
fromsentence_transformersimportSentenceTransformer
importpickle
frompathlibimportPath
importtorch
fromtransformersimport(
AutoTokenizer,AutoModel,
BertTokenizer,BertModel,
RobertaTokenizer,RobertaModel,
pipeline
)
importlogging

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

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

classMultiModelNLPProcessor:
    """Processador NLP com suporte a mltiplos modelos em portugus"""

def__init__(self,model_cache_dir:str="./nlp_models"):
        self.model_cache_dir=Path(model_cache_dir)
self.model_cache_dir.mkdir(exist_ok=True)

self.models_config={
'spacy':{
'name':'pt_core_news_sm',
'fallback':'en_core_web_sm',
'type':'spacy'
},
'sentence_transformer':{
'name':'paraphrase-multilingual-MiniLM-L12-v2',
'type':'sentence_transformer'
},
'bert_pt':{
'name':'neuralmind/bert-base-portuguese-cased',
'type':'bert'
},
'roberta_pt':{
'name':'neuralmind/roberta-base-portuguese-cased',
'type':'roberta'
},
'xlm_roberta':{
'name':'xlm-roberta-base',
'type':'xlm_roberta'
}
}

self.models={}
self._initialize_models()

self.stop_words=set(stopwords.words('portuguese'))
self.stop_words.update(stopwords.words('english'))
self.lemmatizer=WordNetLemmatizer()

self.embedding_cache={}
self.cache_file=self.model_cache_dir/"multi_model_cache.pkl"
self._load_embedding_cache()

self.category_keywords={
'horario':[
'horrio','horario','trabalho','expediente','entrada','sada','saida',
'intervalo','almoo','almoco','jornada','turno','escala','folga',
'hora','tempo','ponto','presena','presenca','funcionamento'
],
'beneficios':[
'benefcio','beneficio','vale','plano','sade','saude','odontolgico',
'odontologico','gympass','auxlio','auxilio','bonus','bnus','premio',
'prmio','gratificao','gratificacao','adiantamento','remunerao'
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

def_initialize_models(self):
        """Inicializa todos os modelos disponveis"""
logger.info(" Inicializando modelos NLP...")

try:
            self.models['spacy']=self._load_spacy_model()
logger.info(" spaCy carregado com sucesso")
exceptExceptionase:
            logger.warning(f" Erro ao carregar spaCy: {e}")
self.models['spacy']=None

try:
            self.models['sentence_transformer']=self._load_sentence_transformer()
logger.info(" Sentence Transformer carregado com sucesso")
exceptExceptionase:
            logger.warning(f" Erro ao carregar Sentence Transformer: {e}")
self.models['sentence_transformer']=None

try:
            self.models['bert_pt']=self._load_bert_model('bert_pt')
logger.info(" BERT Portugus carregado com sucesso")
exceptExceptionase:
            logger.warning(f" Erro ao carregar BERT Portugus: {e}")
self.models['bert_pt']=None

try:
            self.models['roberta_pt']=self._load_roberta_model('roberta_pt')
logger.info(" RoBERTa Portugus carregado com sucesso")
exceptExceptionase:
            logger.warning(f" Erro ao carregar RoBERTa Portugus: {e}")
self.models['roberta_pt']=None

try:
            self.models['xlm_roberta']=self._load_xlm_roberta_model()
logger.info(" XLM-RoBERTa carregado com sucesso")
exceptExceptionase:
            logger.warning(f" Erro ao carregar XLM-RoBERTa: {e}")
self.models['xlm_roberta']=None

logger.info(f" Modelos carregados: {sum(1forminself.models.values()ifmisnotNone)}/5")

def_load_spacy_model(self):
        """Carrega modelo spaCy"""
try:
            returnspacy.load(self.models_config['spacy']['name'])
exceptOSError:
            logger.warning("Modelo spaCy portugus no encontrado, usando modelo ingls")
returnspacy.load(self.models_config['spacy']['fallback'])

def_load_sentence_transformer(self):
        """Carrega modelo Sentence Transformer"""
model_name=self.models_config['sentence_transformer']['name']
model_path=self.model_cache_dir/model_name

ifmodel_path.exists():
            returnSentenceTransformer(str(model_path))
else:
            logger.info("Baixando modelo Sentence Transformer...")
model=SentenceTransformer(model_name)
model.save(str(model_path))
returnmodel

def_load_bert_model(self,model_key:str):
        """Carrega modelo BERT"""
model_name=self.models_config[model_key]['name']
model_path=self.model_cache_dir/model_name

ifmodel_path.exists():
            tokenizer=BertTokenizer.from_pretrained(str(model_path))
model=BertModel.from_pretrained(str(model_path))
else:
            logger.info(f"Baixando modelo BERT: {model_name}")
tokenizer=BertTokenizer.from_pretrained(model_name)
model=BertModel.from_pretrained(model_name)
model.save_pretrained(str(model_path))
tokenizer.save_pretrained(str(model_path))

return{'tokenizer':tokenizer,'model':model}

def_load_roberta_model(self,model_key:str):
        """Carrega modelo RoBERTa"""
model_name=self.models_config[model_key]['name']
model_path=self.model_cache_dir/model_name

ifmodel_path.exists():
            tokenizer=RobertaTokenizer.from_pretrained(str(model_path))
model=RobertaModel.from_pretrained(str(model_path))
else:
            logger.info(f"Baixando modelo RoBERTa: {model_name}")
tokenizer=RobertaTokenizer.from_pretrained(model_name)
model=RobertaModel.from_pretrained(model_name)
model.save_pretrained(str(model_path))
tokenizer.save_pretrained(str(model_path))

return{'tokenizer':tokenizer,'model':model}

def_load_xlm_roberta_model(self):
        """Carrega modelo XLM-RoBERTa"""
model_name=self.models_config['xlm_roberta']['name']
model_path=self.model_cache_dir/model_name

ifmodel_path.exists():
            tokenizer=AutoTokenizer.from_pretrained(str(model_path))
model=AutoModel.from_pretrained(str(model_path))
else:
            logger.info(f"Baixando modelo XLM-RoBERTa: {model_name}")
tokenizer=AutoTokenizer.from_pretrained(model_name)
model=AutoModel.from_pretrained(model_name)
model.save_pretrained(str(model_path))
tokenizer.save_pretrained(str(model_path))

return{'tokenizer':tokenizer,'model':model}

def_load_embedding_cache(self):
        """Carrega cache de embeddings do disco"""
try:
            ifself.cache_file.exists():
                withopen(self.cache_file,'rb')asf:
                    self.embedding_cache=pickle.load(f)
logger.info(f"Cache carregado: {len(self.embedding_cache)} entradas")
exceptExceptionase:
            logger.warning(f"Erro ao carregar cache: {e}")
self.embedding_cache={}

def_save_embedding_cache(self):
        """Salva cache de embeddings no disco"""
try:
            withopen(self.cache_file,'wb')asf:
                pickle.dump(self.embedding_cache,f)
exceptExceptionase:
            logger.warning(f"Erro ao salvar cache: {e}")

defget_text_embedding(self,text:str,model_name:str='sentence_transformer')->Optional[np.ndarray]:
        """Obtm embedding de um texto usando modelo especfico"""
ifmodel_namenotinself.modelsorself.models[model_name]isNone:
            returnNone

cache_key=f"{model_name}_{hash(text)}"
ifcache_keyinself.embedding_cache:
            returnself.embedding_cache[cache_key]

try:
            ifmodel_name=='sentence_transformer':
                embedding=self.models[model_name].encode([text])[0]
elifmodel_namein['bert_pt','roberta_pt','xlm_roberta']:
                embedding=self._get_transformer_embedding(text,model_name)
else:
                returnNone

self.embedding_cache[cache_key]=embedding
iflen(self.embedding_cache)>2000:

                keys_to_remove=list(self.embedding_cache.keys())[:200]
forkeyinkeys_to_remove:
                    delself.embedding_cache[key]

returnembedding
exceptExceptionase:
            logger.error(f"Erro ao gerar embedding com {model_name}: {e}")
returnNone

def_get_transformer_embedding(self,text:str,model_name:str)->np.ndarray:
        """Gera embedding usando modelos transformer"""
model_data=self.models[model_name]
tokenizer=model_data['tokenizer']
model=model_data['model']

inputs=tokenizer(text,return_tensors='pt',truncation=True,padding=True,max_length=512)

withtorch.no_grad():
            outputs=model(**inputs)

embeddings=outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

returnembeddings

defcalculate_semantic_similarity(self,text1:str,text2:str,model_name:str='sentence_transformer')->float:
        """Calcula similaridade semntica usando modelo especfico"""
emb1=self.get_text_embedding(text1,model_name)
emb2=self.get_text_embedding(text2,model_name)

ifemb1isnotNoneandemb2isnotNone:

            similarity=np.dot(emb1,emb2)/(np.linalg.norm(emb1)*np.linalg.norm(emb2))
returnfloat(similarity)

return0.0

defcalculate_multi_model_similarity(self,text1:str,text2:str)->Dict[str,float]:
        """Calcula similaridade usando mltiplos modelos"""
similarities={}

formodel_nameinself.models:
            ifself.models[model_name]isnotNone:
                try:
                    sim=self.calculate_semantic_similarity(text1,text2,model_name)
similarities[model_name]=sim
exceptExceptionase:
                    logger.warning(f"Erro ao calcular similaridade com {model_name}: {e}")
similarities[model_name]=0.0

returnsimilarities

defget_ensemble_similarity(self,text1:str,text2:str)->float:
        """Calcula similaridade ensemble usando todos os modelos disponveis"""
similarities=self.calculate_multi_model_similarity(text1,text2)

ifnotsimilarities:
            return0.0

model_weights={
'sentence_transformer':0.3,
'bert_pt':0.25,
'roberta_pt':0.25,
'xlm_roberta':0.15,
'spacy':0.05
}

weighted_sum=0.0
total_weight=0.0

formodel_name,similarityinsimilarities.items():
            weight=model_weights.get(model_name,0.1)
weighted_sum+=similarity*weight
total_weight+=weight

returnweighted_sum/total_weightiftotal_weight>0else0.0

defextract_entities_advanced(self,text:str)->Dict[str,List[str]]:
        """Extrai entidades usando mltiplos modelos"""
entities={
'persons':[],
'organizations':[],
'dates':[],
'numbers':[],
'emails':[],
'urls':[],
'locations':[]
}

ifself.models['spacy']isnotNone:
            try:
                doc=self.models['spacy'](text)
forentindoc.ents:
                    ifent.label_=="PER":
                        entities['persons'].append(ent.text)
elifent.label_=="ORG":
                        entities['organizations'].append(ent.text)
elifent.label_=="DATE":
                        entities['dates'].append(ent.text)
elifent.label_=="LOC":
                        entities['locations'].append(ent.text)
exceptExceptionase:
                logger.warning(f"Erro na extrao de entidades spaCy: {e}")

entities['numbers'].extend(re.findall(r'\b\d+(?:\.\d+)?\b',text))
entities['emails'].extend(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',text))
entities['urls'].extend(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text))

returnentities

defcategorize_question_advanced(self,question:str)->Tuple[str,float]:
        """Categoriza pergunta com pontuao de confiana usando mltiplos modelos"""
try:

            ifself.models['spacy']isnotNone:
                doc=self.models['spacy'](question)
question_processed=' '.join([token.lemma_.lower()fortokenindocifnottoken.is_stop])
else:
                question_processed=question.lower()

forcategory,patterninself.question_patterns.items():
                ifre.search(pattern,question_processed,re.IGNORECASE):
                    returncategory,0.9

category_scores={}

ifself.models['spacy']isnotNone:
                question_tokens=set([token.lemma_.lower()fortokenindocifnottoken.is_stop])
else:
                question_tokens=set(question.lower().split())

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
            logger.error(f"Erro na categorizao avanada: {e}")
return'geral',0.0

defanalyze_sentiment_advanced(self,text:str)->Dict[str,Any]:
        """Analisa sentimento usando mltiplas tcnicas"""
sentiment_results={}

try:
            blob=TextBlob(text)
sentiment_results['textblob']={
'polarity':blob.sentiment.polarity,
'subjectivity':blob.sentiment.subjectivity,
'sentiment':'positive'ifblob.sentiment.polarity>0.1else'negative'ifblob.sentiment.polarity<-0.1else'neutral'
}
exceptExceptionase:
            logger.warning(f"Erro na anlise de sentimento TextBlob: {e}")
sentiment_results['textblob']={'polarity':0.0,'subjectivity':0.0,'sentiment':'neutral'}

try:
            positive_words=['bom','boa','timo','otimo','excelente','perfeito','maravilhoso','fantstico','fantastico']
negative_words=['ruim','pssimo','pessimo','terrvel','terrivel','horrvel','horrivel','problema','erro']

text_lower=text.lower()
positive_count=sum(1forwordinpositive_wordsifwordintext_lower)
negative_count=sum(1forwordinnegative_wordsifwordintext_lower)

ifpositive_count>negative_count:
                keyword_sentiment='positive'
keyword_score=positive_count/(positive_count+negative_count)if(positive_count+negative_count)>0else0
elifnegative_count>positive_count:
                keyword_sentiment='negative'
keyword_score=negative_count/(positive_count+negative_count)if(positive_count+negative_count)>0else0
else:
                keyword_sentiment='neutral'
keyword_score=0.0

sentiment_results['keywords']={
'sentiment':keyword_sentiment,
'score':keyword_score
}
exceptExceptionase:
            logger.warning(f"Erro na anlise de sentimento por palavras-chave: {e}")
sentiment_results['keywords']={'sentiment':'neutral','score':0.0}

textblob_result=sentiment_results.get('textblob',{})
keyword_result=sentiment_results.get('keywords',{})

combined_polarity=textblob_result.get('polarity',0.0)
ifkeyword_result.get('sentiment')=='positive':
            combined_polarity+=0.2
elifkeyword_result.get('sentiment')=='negative':
            combined_polarity-=0.2

combined_sentiment='positive'ifcombined_polarity>0.1else'negative'ifcombined_polarity<-0.1else'neutral'

return{
'textblob':textblob_result,
'keywords':keyword_result,
'combined':{
'polarity':combined_polarity,
'sentiment':combined_sentiment,
'confidence':abs(combined_polarity)
}
}

defsave_cache(self):
        """Salva cache de embeddings"""
self._save_embedding_cache()

defget_model_status(self)->Dict[str,bool]:
        """Retorna status dos modelos"""
return{name:modelisnotNoneforname,modelinself.models.items()}

defget_cache_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache"""
return{
'cache_size':len(self.embedding_cache),
'cache_file_size':self.cache_file.stat().st_sizeifself.cache_file.exists()else0,
'models_loaded':sum(1forminself.models.values()ifmisnotNone)
}
