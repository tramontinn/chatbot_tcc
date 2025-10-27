
importos
importjson
importre
importnltk
importspacy
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime
frompathlibimportPath
importpickle
fromcollectionsimportdefaultdict,Counter

try:
    nltk.data.find('tokenizers/punkt')
exceptLookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
exceptLookupError:
    nltk.download('stopwords')

fromnltk.tokenizeimportword_tokenize,sent_tokenize
fromnltk.corpusimportstopwords

classIntelligentTrainingSystem:
    """Sistema de treinamento inteligente para tornar a IA mais coerente"""

def__init__(self,internal_doc_manager=None,training_data_path:str="training_data"):
        self.internal_doc_manager=internal_doc_manager
self.training_data_path=Path(training_data_path)
self.training_data_path.mkdir(exist_ok=True)

try:
            self.nlp=spacy.load("pt_core_news_sm")
exceptOSError:
            print("Modelo spaCy portugus no encontrado. Usando modelo bsico.")
self.nlp=spacy.load("en_core_web_sm")

self.stop_words=set(stopwords.words('portuguese'))
self.stop_words.update(stopwords.words('english'))

self.knowledge_base_file=self.training_data_path/"knowledge_base.json"
self.response_templates_file=self.training_data_path/"response_templates.json"
self.question_patterns_file=self.training_data_path/"question_patterns.json"
self.entity_database_file=self.training_data_path/"entity_database.json"
self.training_stats_file=self.training_data_path/"training_stats.json"

self.knowledge_base={}
self.response_templates={}
self.question_patterns={}
self.entity_database={}
self.training_stats={}

self._load_training_data()

def_load_training_data(self):
        """Carrega dados de treinamento existentes"""
try:
            ifself.knowledge_base_file.exists():
                withopen(self.knowledge_base_file,'r',encoding='utf-8')asf:
                    self.knowledge_base=json.load(f)

ifself.response_templates_file.exists():
                withopen(self.response_templates_file,'r',encoding='utf-8')asf:
                    self.response_templates=json.load(f)

ifself.question_patterns_file.exists():
                withopen(self.question_patterns_file,'r',encoding='utf-8')asf:
                    self.question_patterns=json.load(f)

ifself.entity_database_file.exists():
                withopen(self.entity_database_file,'r',encoding='utf-8')asf:
                    self.entity_database=json.load(f)

ifself.training_stats_file.exists():
                withopen(self.training_stats_file,'r',encoding='utf-8')asf:
                    self.training_stats=json.load(f)

exceptExceptionase:
            print(f"Erro ao carregar dados de treinamento: {e}")

def_save_training_data(self):
        """Salva dados de treinamento"""
try:
            withopen(self.knowledge_base_file,'w',encoding='utf-8')asf:
                json.dump(self.knowledge_base,f,ensure_ascii=False,indent=2)

withopen(self.response_templates_file,'w',encoding='utf-8')asf:
                json.dump(self.response_templates,f,ensure_ascii=False,indent=2)

withopen(self.question_patterns_file,'w',encoding='utf-8')asf:
                json.dump(self.question_patterns,f,ensure_ascii=False,indent=2)

withopen(self.entity_database_file,'w',encoding='utf-8')asf:
                json.dump(self.entity_database,f,ensure_ascii=False,indent=2)

withopen(self.training_stats_file,'w',encoding='utf-8')asf:
                json.dump(self.training_stats,f,ensure_ascii=False,indent=2)

exceptExceptionase:
            print(f"Erro ao salvar dados de treinamento: {e}")

deftrain_from_documents(self)->Dict[str,Any]:
        """Treina a IA a partir dos documentos internos"""

print(" Iniciando treinamento da IA...")

ifnotself.internal_doc_manager:
            return{"error":"Gerenciador de documentos internos no disponvel"}

try:

            documents=self.internal_doc_manager.list_documents()

ifnotdocuments:
                return{"error":"Nenhum documento encontrado para treinamento"}

training_results={
"documents_processed":0,
"knowledge_extracted":0,
"templates_created":0,
"patterns_learned":0,
"entities_found":0,
"categories_trained":set(),
"start_time":datetime.now().isoformat()
}

fordoc_infoindocuments:
                print(f" Processando: {doc_info['filename']}")

content=self.internal_doc_manager.get_document_content(doc_info["filename"])
ifnotcontent:
                    continue

category=doc_info.get('category','geral')
training_results["categories_trained"].add(category)

doc_knowledge=self._extract_knowledge_from_document(content,category,doc_info["filename"])

doc_templates=self._extract_response_templates(content,category)

doc_patterns=self._extract_question_patterns(content,category)

doc_entities=self._extract_entities_from_document(content,category)

self._consolidate_knowledge(category,doc_knowledge,doc_templates,doc_patterns,doc_entities)

training_results["documents_processed"]+=1
training_results["knowledge_extracted"]+=len(doc_knowledge)
training_results["templates_created"]+=len(doc_templates)
training_results["patterns_learned"]+=len(doc_patterns)
training_results["entities_found"]+=len(doc_entities)

training_results["categories_trained"]=list(training_results["categories_trained"])
training_results["end_time"]=datetime.now().isoformat()

self._save_training_data()

self.training_stats={
"last_training":datetime.now().isoformat(),
"total_documents_processed":training_results["documents_processed"],
"total_knowledge_items":len(self.knowledge_base),
"total_templates":len(self.response_templates),
"total_patterns":len(self.question_patterns),
"total_entities":len(self.entity_database),
"categories_trained":training_results["categories_trained"]
}

self._save_training_data()

print(" Treinamento concludo com sucesso!")
returntraining_results

exceptExceptionase:
            print(f" Erro durante o treinamento: {e}")
return{"error":str(e)}

def_extract_knowledge_from_document(self,content:str,category:str,filename:str)->List[Dict[str,Any]]:
        """Extrai conhecimento estruturado do documento"""

knowledge_items=[]

sections=self._split_into_sections(content)

forsectioninsections:

            structured_info=self._extract_structured_information(section,category)

ifstructured_info:
                knowledge_items.append({
"content":section,
"category":category,
"filename":filename,
"structured_info":structured_info,
"keywords":self._extract_keywords(section),
"timestamp":datetime.now().isoformat()
})

returnknowledge_items

def_split_into_sections(self,content:str)->List[str]:
        """Divide o contedo em sees lgicas"""

sections=re.split(r'\n\d+\.\s+',content)

iflen(sections)<=1:
            sections=content.split('\n\n')

sections=[section.strip()forsectioninsectionsiflen(section.strip())>50]

returnsections

def_extract_structured_information(self,section:str,category:str)->Dict[str,Any]:
        """Extrai informaes estruturadas de uma seo"""

structured_info={
"type":"general",
"entities":[],
"numbers":[],
"times":[],
"prices":[],
"contacts":[],
"schedules":[]
}

section_lower=section.lower()

ifany(wordinsection_lowerforwordin["horrio","horario","funcionamento","aberto","fechado"]):
            structured_info["type"]="schedule"
structured_info["schedules"]=self._extract_schedules(section)

elifany(wordinsection_lowerforwordin["preo","preco","valor","custo","r$","reais"]):
            structured_info["type"]="pricing"
structured_info["prices"]=self._extract_prices(section)

elifany(wordinsection_lowerforwordin["telefone","email","contato","endereo","endereco"]):
            structured_info["type"]="contact"
structured_info["contacts"]=self._extract_contacts(section)

elifany(wordinsection_lowerforwordin["servio","servico","benefcio","beneficio","plano"]):
            structured_info["type"]="service"

structured_info["entities"]=self._extract_entities_from_text(section)

structured_info["numbers"]=re.findall(r'\b\d+(?:[.,]\d+)?\b',section)

structured_info["times"]=re.findall(r'\b\d{1,2}h\b',section)

returnstructured_info

def_extract_schedules(self,text:str)->List[Dict[str,str]]:
        """Extrai informaes de horrios"""

schedules=[]

time_patterns=[
r'(\w+)\s+(?:a|s|as)\s+(\w+):\s*(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)',
r'(\w+):\s*(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)',
r'(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)'
]

forpatternintime_patterns:
            matches=re.findall(pattern,text,re.IGNORECASE)
formatchinmatches:
                iflen(match)==3:
                    schedules.append({
"day":match[0],
"period":match[1],
"time":match[2]
})
eliflen(match)==2:
                    schedules.append({
"period":match[0],
"time":match[1]
})
else:
                    schedules.append({
"time":match[0]
})

returnschedules

def_extract_prices(self,text:str)->List[Dict[str,str]]:
        """Extrai informaes de preos"""

prices=[]

price_patterns=[
r'([^:]+):\s*R\$\s*(\d+(?:[.,]\d+)?)',
r'R\$\s*(\d+(?:[.,]\d+)?)\s*([^.,\n]+)',
r'(\d+(?:[.,]\d+)?)\s*reais?\s*([^.,\n]+)'
]

forpatterninprice_patterns:
            matches=re.findall(pattern,text,re.IGNORECASE)
formatchinmatches:
                iflen(match)==2:
                    prices.append({
"item":match[0].strip(),
"price":match[1].strip()
})

returnprices

def_extract_contacts(self,text:str)->List[Dict[str,str]]:
        """Extrai informaes de contato"""

contacts=[]

emails=re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',text)
foremailinemails:
            contacts.append({"type":"email","value":email})

phones=re.findall(r'\(?\d{2}\)?\s*\d{4,5}-?\d{4}',text)
forphoneinphones:
            contacts.append({"type":"phone","value":phone})

addresses=re.findall(r'(?:Rua|Av|Avenida|R\.|Alameda|Praa)\s+[^,\n]+',text,re.IGNORECASE)
foraddressinaddresses:
            contacts.append({"type":"address","value":address.strip()})

returncontacts

def_extract_entities_from_text(self,text:str)->List[str]:
        """Extrai entidades nomeadas do texto"""

doc=self.nlp(text)
entities=[]

forentindoc.ents:
            ifent.label_in["PER","ORG","LOC","MISC"]:
                entities.append(ent.text)

returnentities

def_extract_keywords(self,text:str)->List[str]:
        """Extrai palavras-chave do texto"""

doc=self.nlp(text)
keywords=[]

fortokenindoc:
            if(nottoken.is_stopand
nottoken.is_punctand
nottoken.is_spaceand
len(token.text)>2and
token.pos_in['NOUN','PROPN','ADJ']):
                keywords.append(token.lemma_.lower())

returnkeywords[:10]

def_extract_response_templates(self,content:str,category:str)->List[Dict[str,Any]]:
        """Extrai templates de resposta do documento"""

templates=[]

sentences=sent_tokenize(content)

forsentenceinsentences:
            iflen(sentence.strip())>20:

                sentence_lower=sentence.lower()

template_type="general"
ifany(wordinsentence_lowerforwordin["horrio","horario","funcionamento"]):
                    template_type="schedule"
elifany(wordinsentence_lowerforwordin["preo","preco","valor","r$"]):
                    template_type="pricing"
elifany(wordinsentence_lowerforwordin["contato","telefone","email"]):
                    template_type="contact"
elifany(wordinsentence_lowerforwordin["servio","servico","benefcio"]):
                    template_type="service"

templates.append({
"content":sentence.strip(),
"type":template_type,
"category":category,
"keywords":self._extract_keywords(sentence),
"timestamp":datetime.now().isoformat()
})

returntemplates

def_extract_question_patterns(self,content:str,category:str)->List[Dict[str,Any]]:
        """Extrai padres de perguntas baseados no contedo"""

patterns=[]

questions=self._generate_questions_from_content(content,category)

forquestioninquestions:
            patterns.append({
"question":question,
"category":category,
"keywords":self._extract_keywords(question),
"timestamp":datetime.now().isoformat()
})

returnpatterns

def_generate_questions_from_content(self,content:str,category:str)->List[str]:
        """Gera perguntas baseadas no contedo"""

questions=[]

question_templates={
"academia":[
"Qual o horrio de funcionamento da academia?",
"Quanto custa o plano {item}?",
"Que equipamentos tem na academia?",
"Tem {servio} disponvel?",
"Qual o endereo da academia?"
],
"supermercado":[
"Qual o horrio de funcionamento do supermercado?",
"Tem delivery no supermercado?",
"Quais as promoes de {dia}?",
"Qual o pedido mnimo para delivery?",
"Tem estacionamento gratuito?"
],
"restaurante":[
"Qual o horrio de funcionamento do restaurante?",
"Qual o cardpio do restaurante?",
"Preciso fazer reserva?",
"Tem delivery no restaurante?",
"Qual o endereo do restaurante?"
],
"empresa":[
"Qual o horrio de trabalho?",
"Quais so os benefcios oferecidos?",
"Como funciona a poltica de frias?",
"Qual o valor do vale refeio?",
"Como entrar em contato com o RH?"
]
}

ifcategoryinquestion_templates:
            questions.extend(question_templates[category])

if"horrio"incontent.lower()or"horario"incontent.lower():
            questions.append(f"Qual o horrio de funcionamento?")

if"preo"incontent.lower()or"preco"incontent.lower()or"r$"incontent:
            questions.append(f"Quais so os preos?")

if"contato"incontent.lower()or"telefone"incontent.lower():
            questions.append(f"Como entrar em contato?")

returnquestions

def_extract_entities_from_document(self,content:str,category:str)->List[Dict[str,Any]]:
        """Extrai entidades do documento"""

entities=[]

doc=self.nlp(content)

forentindoc.ents:
            entities.append({
"text":ent.text,
"label":ent.label_,
"category":category,
"context":ent.sent.textifhasattr(ent,'sent')else"",
"timestamp":datetime.now().isoformat()
})

returnentities

def_consolidate_knowledge(self,category:str,knowledge:List[Dict],templates:List[Dict],patterns:List[Dict],entities:List[Dict]):
        """Consolida conhecimento extrado"""

ifcategorynotinself.knowledge_base:
            self.knowledge_base[category]=[]

self.knowledge_base[category].extend(knowledge)

ifcategorynotinself.response_templates:
            self.response_templates[category]=[]

self.response_templates[category].extend(templates)

ifcategorynotinself.question_patterns:
            self.question_patterns[category]=[]

self.question_patterns[category].extend(patterns)

forentityinentities:
            entity_key=f"{entity['text']}_{entity['label']}"
ifentity_keynotinself.entity_database:
                self.entity_database[entity_key]=entity

defget_training_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas do treinamento"""

return{
"training_stats":self.training_stats,
"knowledge_base_size":len(self.knowledge_base),
"response_templates_size":len(self.response_templates),
"question_patterns_size":len(self.question_patterns),
"entity_database_size":len(self.entity_database),
"categories_available":list(self.knowledge_base.keys())
}

defget_knowledge_for_category(self,category:str)->Dict[str,Any]:
        """Retorna conhecimento para uma categoria especfica"""

return{
"knowledge":self.knowledge_base.get(category,[]),
"templates":self.response_templates.get(category,[]),
"patterns":self.question_patterns.get(category,[]),
"entities":[entityforentityinself.entity_database.values()ifentity.get('category')==category]
}

defgenerate_training_report(self)->str:
        """Gera relatrio de treinamento"""

stats=self.get_training_statistics()

report=f"""
 RELATRIO DE TREINAMENTO DA IA
{'='*50}

 ltimo Treinamento:
{stats['training_stats'].get('last_training','Nunca')}
 Documentos Processados:
{stats['training_stats'].get('total_documents_processed',0)}
 Itens de Conhecimento:
{stats['knowledge_base_size']}
 Templates de Resposta:
{stats['response_templates_size']}
 Padres de Perguntas:
{stats['question_patterns_size']}
 Entidades Identificadas:
{stats['entity_database_size']}

 Categorias Treinadas:
"""

forcategoryinstats['categories_available']:
            category_stats=self.get_knowledge_for_category(category)
report+=f"   {category}: {len(category_stats['knowledge'])} itens de conhecimento\n"

returnreport
