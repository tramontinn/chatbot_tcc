importre
importnltk
fromtypingimportList,Dict,Any,Tuple,Optional
fromcollectionsimportCounter
importmath
fromdifflibimportSequenceMatcher
importstring

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

classNLPProcessor:
    """Processador de Linguagem Natural local sem dependncia de APIs externas"""

def__init__(self):

        self.stop_words=set(stopwords.words('portuguese'))
self.stop_words.update(stopwords.words('english'))
self.lemmatizer=WordNetLemmatizer()

self.category_keywords={
'horario':['horrio','horario','trabalho','expediente','entrada','sada','saida','intervalo','almoo','almoco'],
'beneficios':['benefcio','beneficio','vale','plano','sade','saude','odontolgico','odontologico','gympass'],
'ferias':['frias','ferias','adicional','constitucional','perodo','periodo'],
'licenca':['licena','licenca','mdica','medica','atestado','inss','pagamento'],
'vestimenta':['vestimenta','roupa','traje','social','casual','informal'],
'comunicacao':['comunicao','comunicacao','email','whatsapp','slack','mensagem'],
'seguranca':['segurana','seguranca','carto','cartao','acesso','senha','bloquear','incidente'],
'limpeza':['limpeza','organizao','organizacao','mesa','lixo','copa','espao','espaco'],
'treinamento':['treinamento','curso','capacitao','capacitacao','workshop','desenvolvimento']
}

self.question_patterns={
'horario':r'(qual|quais|como|quando).*(horrio|horario|trabalho|expediente)',
'beneficios':r'(qual|quais|como).*(benefcio|beneficio|vale|plano)',
'ferias':r'(qual|quais|como|quando).*(frias|ferias)',
'licenca':r'(qual|quais|como).*(licena|licenca|mdica|medica)',
'vestimenta':r'(qual|quais|como).*(vestimenta|roupa|traje)',
'comunicacao':r'(qual|quais|como).*(comunicao|comunicacao|email)',
'seguranca':r'(qual|quais|como).*(segurana|seguranca)',
'limpeza':r'(qual|quais|como).*(limpeza|organizao|organizacao)',
'treinamento':r'(qual|quais|como).*(treinamento|curso|capacitao|capacitacao)'
}

defpreprocess_text(self,text:str)->str:
        """Preprocessa texto removendo caracteres especiais e normalizando"""

text=text.lower()

text=re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]',' ',text)

text=re.sub(r'\s+',' ',text)

returntext.strip()

defextract_keywords(self,text:str,max_keywords:int=10)->List[str]:
        """Extrai palavras-chave do texto"""

processed_text=self.preprocess_text(text)

tokens=word_tokenize(processed_text,language='portuguese')

keywords=[tokenfortokenintokens
iftokennotinself.stop_words
andtokennotinstring.punctuation
andlen(token)>2]

word_freq=Counter(keywords)

return[wordforword,freqinword_freq.most_common(max_keywords)]

defcategorize_question(self,question:str)->str:
        """Categoriza uma pergunta baseada em padres"""
question_lower=self.preprocess_text(question)

forcategory,patterninself.question_patterns.items():
            ifre.search(pattern,question_lower):
                returncategory

question_words=set(word_tokenize(question_lower,language='portuguese'))

category_scores={}
forcategory,keywordsinself.category_keywords.items():
            score=len(question_words.intersection(set(keywords)))
ifscore>0:
                category_scores[category]=score

ifcategory_scores:
            returnmax(category_scores,key=category_scores.get)

return'geral'

deffind_relevant_sentences(self,question:str,document_text:str,max_sentences:int=3)->List[str]:
        """Encontra sentenas relevantes no documento baseado na pergunta"""

question_category=self.categorize_question(question)

question_keywords=self.extract_keywords(question,max_keywords=5)

sentences=sent_tokenize(document_text,language='portuguese')

sentence_scores=[]

forsentenceinsentences:
            score=0
sentence_lower=sentence.lower()

ifquestion_category!='geral':
                category_keywords=self.category_keywords.get(question_category,[])
forkeywordincategory_keywords:
                    ifkeywordinsentence_lower:
                        score+=2

forkeywordinquestion_keywords:
                ifkeywordinsentence_lower:
                    score+=1

sentence_keywords=self.extract_keywords(sentence,max_keywords=10)
common_words=set(question_keywords).intersection(set(sentence_keywords))
score+=len(common_words)

sentence_scores.append((sentence,score))

sentence_scores.sort(key=lambdax:x[1],reverse=True)

relevant_sentences=[sentenceforsentence,scoreinsentence_scores[:max_sentences]ifscore>0]

returnrelevant_sentences

defgenerate_answer(self,question:str,relevant_sentences:List[str],context:str="")->str:
        """Gera uma resposta baseada nas sentenas relevantes"""
ifnotrelevant_sentences:
            return"Desculpe, no encontrei informaes especficas sobre sua pergunta nos documentos disponveis."

question_category=self.categorize_question(question)

ifany(wordinquestion.lower()forwordin['o que','quem','quando','onde','como','por que']):

            answer=f"Baseado nos documentos disponveis: {relevant_sentences[0]}"
iflen(relevant_sentences)>1:
                answer+=f" Alm disso: {relevant_sentences[1]}"
else:

            answer=f"Encontrei esta informao relevante: {relevant_sentences[0]}"
iflen(relevant_sentences)>1:
                answer+=f" Tambm h: {relevant_sentences[1]}"

ifcontextandlen(relevant_sentences)<2:
            answer+=f" {context}"

returnanswer

defcalculate_similarity(self,text1:str,text2:str)->float:
        """Calcula similaridade entre dois textos"""

text1_clean=self.preprocess_text(text1)
text2_clean=self.preprocess_text(text2)

returnSequenceMatcher(None,text1_clean,text2_clean).ratio()

defextract_entities(self,text:str)->Dict[str,List[str]]:
        """Extrai entidades nomeadas bsicas do texto"""
entities={
'dates':[],
'numbers':[],
'emails':[],
'urls':[]
}

date_pattern=r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
entities['dates']=re.findall(date_pattern,text)

number_pattern=r'\b\d+(?:\.\d+)?\b'
entities['numbers']=re.findall(number_pattern,text)

email_pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
entities['emails']=re.findall(email_pattern,text)

url_pattern=r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
entities['urls']=re.findall(url_pattern,text)

returnentities

defsummarize_text(self,text:str,max_sentences:int=3)->str:
        """Gera um resumo bsico do texto"""
sentences=sent_tokenize(text,language='portuguese')

iflen(sentences)<=max_sentences:
            returntext

sentence_scores=[]
forsentenceinsentences:

            keywords=self.extract_keywords(text,max_keywords=10)
sentence_keywords=self.extract_keywords(sentence,max_keywords=5)

score=len(set(keywords).intersection(set(sentence_keywords)))
sentence_scores.append((sentence,score))

sentence_scores.sort(key=lambdax:x[1],reverse=True)
summary_sentences=[sentenceforsentence,scoreinsentence_scores[:max_sentences]]

return' '.join(summary_sentences)

defis_question(self,text:str)->bool:
        """Verifica se o texto  uma pergunta"""
text_lower=text.lower().strip()

question_words=['o que','quem','quando','onde','como','por que','porque','qual','quais']

ifany(text_lower.startswith(word)forwordinquestion_words):
            returnTrue

iftext_lower.endswith('?'):
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
