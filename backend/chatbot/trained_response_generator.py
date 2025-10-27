
importjson
importre
importrandom
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime
frompathlibimportPath
fromdifflibimportSequenceMatcher

classTrainedResponseGenerator:
    """Gerador de respostas baseado no conhecimento treinado"""

def__init__(self,training_data_path:str="training_data"):
        self.training_data_path=Path(training_data_path)

self.knowledge_base={}
self.response_templates={}
self.question_patterns={}
self.entity_database={}

self._load_training_data()

def_load_training_data(self):
        """Carrega dados de treinamento"""
try:
            knowledge_file=self.training_data_path/"knowledge_base.json"
ifknowledge_file.exists():
                withopen(knowledge_file,'r',encoding='utf-8')asf:
                    self.knowledge_base=json.load(f)

templates_file=self.training_data_path/"response_templates.json"
iftemplates_file.exists():
                withopen(templates_file,'r',encoding='utf-8')asf:
                    self.response_templates=json.load(f)

patterns_file=self.training_data_path/"question_patterns.json"
ifpatterns_file.exists():
                withopen(patterns_file,'r',encoding='utf-8')asf:
                    self.question_patterns=json.load(f)

entities_file=self.training_data_path/"entity_database.json"
ifentities_file.exists():
                withopen(entities_file,'r',encoding='utf-8')asf:
                    self.entity_database=json.load(f)

exceptExceptionase:
            print(f"Erro ao carregar dados de treinamento: {e}")

defgenerate_trained_response(self,question:str,category:str=None)->Dict[str,Any]:
        """Gera resposta baseada no conhecimento treinado"""

question_analysis=self._analyze_question(question)

ifnotcategory:
            category=self._determine_category(question,question_analysis)

relevant_knowledge=self._find_relevant_knowledge(question,category,question_analysis)

relevant_templates=self._find_relevant_templates(question,category,question_analysis)

response=self._generate_response_from_knowledge(
question,category,relevant_knowledge,relevant_templates,question_analysis
)

return{
"response":response,
"category":category,
"confidence":self._calculate_confidence(relevant_knowledge,relevant_templates),
"sources":[k.get('filename','unknown')forkinrelevant_knowledge],
"knowledge_used":len(relevant_knowledge),
"templates_used":len(relevant_templates)
}

def_analyze_question(self,question:str)->Dict[str,Any]:
        """Analisa a pergunta para extrair informaes"""

question_lower=question.lower()

analysis={
"type":"general",
"keywords":[],
"entities":[],
"intent":"information",
"specificity":"medium"
}

ifany(wordinquestion_lowerforwordin["horrio","horario","funcionamento","aberto","fechado"]):
            analysis["type"]="schedule"
elifany(wordinquestion_lowerforwordin["preo","preco","valor","custo","quanto","r$"]):
            analysis["type"]="pricing"
elifany(wordinquestion_lowerforwordin["contato","telefone","email","endereo","endereco"]):
            analysis["type"]="contact"
elifany(wordinquestion_lowerforwordin["servio","servico","benefcio","beneficio","plano"]):
            analysis["type"]="service"
elifany(wordinquestion_lowerforwordin["como","onde","quando","por que","porque"]):
            analysis["type"]="how_to"

ifany(wordinquestion_lowerforwordin["tem","existe","disponvel","disponivel"]):
            analysis["intent"]="availability"
elifany(wordinquestion_lowerforwordin["qual","quais","que"]):
            analysis["intent"]="information"
elifany(wordinquestion_lowerforwordin["como","onde"]):
            analysis["intent"]="procedure"

iflen(question.split())<=3:
            analysis["specificity"]="low"
eliflen(question.split())>=10:
            analysis["specificity"]="high"

words=question_lower.split()
stop_words={"o","a","os","as","um","uma","de","da","do","das","dos","em","na","no","nas","nos","para","por","com","sem","qual","quais","como","quando","onde","porque","que","quem"}
analysis["keywords"]=[wordforwordinwordsifwordnotinstop_wordsandlen(word)>2]

returnanalysis

def_determine_category(self,question:str,analysis:Dict[str,Any])->str:
        """Determina a categoria da pergunta"""

question_lower=question.lower()

category_keywords={
"academia":["academia","gym","ginsio","ginasio","fitness","musculao","musculacao","treino","exerccio","exercicio"],
"supermercado":["supermercado","mercado","loja","compras","produto","delivery"],
"restaurante":["restaurante","comida","jantar","almoo","almoco","cardpio","cardapio","reserva"],
"empresa":["empresa","trabalho","funcionrio","funcionario","colaborador","rh","benefcio","beneficio","salrio","salario"]
}

category_scores={}
forcategory,keywordsincategory_keywords.items():
            score=sum(1forkeywordinkeywordsifkeywordinquestion_lower)
ifscore>0:
                category_scores[category]=score

ifcategory_scores:
            returnmax(category_scores,key=category_scores.get)

return"geral"

def_find_relevant_knowledge(self,question:str,category:str,analysis:Dict[str,Any])->List[Dict[str,Any]]:
        """Encontra conhecimento relevante para a pergunta"""

relevant_knowledge=[]

ifcategorynotinself.knowledge_base:
            returnrelevant_knowledge

question_lower=question.lower()
question_keywords=set(analysis["keywords"])

forknowledge_iteminself.knowledge_base[category]:

            relevance_score=self._calculate_relevance(knowledge_item,question,question_keywords,analysis)

ifrelevance_score>0.3:
                knowledge_item["relevance_score"]=relevance_score
relevant_knowledge.append(knowledge_item)

relevant_knowledge.sort(key=lambdax:x["relevance_score"],reverse=True)

returnrelevant_knowledge[:3]

def_calculate_relevance(self,knowledge_item:Dict[str,Any],question:str,question_keywords:set,analysis:Dict[str,Any])->float:
        """Calcula relevncia de um item de conhecimento"""

content=knowledge_item.get("content","").lower()
structured_info=knowledge_item.get("structured_info",{})
knowledge_keywords=set(knowledge_item.get("keywords",[]))

score=0.0

common_keywords=question_keywords.intersection(knowledge_keywords)
ifcommon_keywords:
            score+=len(common_keywords)/max(len(question_keywords),1)*0.4

content_similarity=SequenceMatcher(None,question.lower(),content).ratio()
score+=content_similarity*0.3

ifstructured_info.get("type")==analysis["type"]:
            score+=0.2

ifstructured_info.get("entities"):
            entity_matches=sum(1forentityinstructured_info["entities"]ifentity.lower()inquestion.lower())
ifentity_matches>0:
                score+=0.1

returnmin(score,1.0)

def_find_relevant_templates(self,question:str,category:str,analysis:Dict[str,Any])->List[Dict[str,Any]]:
        """Encontra templates de resposta relevantes"""

relevant_templates=[]

ifcategorynotinself.response_templates:
            returnrelevant_templates

question_lower=question.lower()
question_keywords=set(analysis["keywords"])

fortemplateinself.response_templates[category]:

            template_relevance=self._calculate_template_relevance(template,question,question_keywords,analysis)

iftemplate_relevance>0.3:
                template["relevance_score"]=template_relevance
relevant_templates.append(template)

relevant_templates.sort(key=lambdax:x["relevance_score"],reverse=True)

returnrelevant_templates[:2]

def_calculate_template_relevance(self,template:Dict[str,Any],question:str,question_keywords:set,analysis:Dict[str,Any])->float:
        """Calcula relevncia de um template"""

template_content=template.get("content","").lower()
template_type=template.get("type","general")
template_keywords=set(template.get("keywords",[]))

score=0.0

iftemplate_type==analysis["type"]:
            score+=0.4

common_keywords=question_keywords.intersection(template_keywords)
ifcommon_keywords:
            score+=len(common_keywords)/max(len(question_keywords),1)*0.3

content_similarity=SequenceMatcher(None,question.lower(),template_content).ratio()
score+=content_similarity*0.3

returnmin(score,1.0)

def_generate_response_from_knowledge(self,question:str,category:str,knowledge:List[Dict[str,Any]],templates:List[Dict[str,Any]],analysis:Dict[str,Any])->str:
        """Gera resposta baseada no conhecimento e templates"""

ifnotknowledgeandnottemplates:
            returnself._generate_fallback_response(question,category,analysis)

response_parts=[]

intro=self._get_response_intro(analysis["type"],analysis["intent"])
ifintro:
            response_parts.append(intro)

ifknowledge:
            knowledge_text=self._format_knowledge(knowledge,analysis)
ifknowledge_text:
                response_parts.append(knowledge_text)

iftemplates:
            template_text=self._format_templates(templates,analysis)
iftemplate_text:
                response_parts.append(template_text)

specific_info=self._extract_specific_information(knowledge,analysis)
ifspecific_info:
            response_parts.append(specific_info)

ifresponse_parts:
            response="\n\n".join(response_parts)
else:
            response=self._generate_fallback_response(question,category,analysis)

response=self._add_category_emoji(response,category)

returnresponse

def_get_response_intro(self,question_type:str,intent:str)->str:
        """Gera introduo baseada no tipo de pergunta"""

intros={
"schedule":{
"information":" Aqui esto as informaes sobre horrios:",
"availability":" Sobre o funcionamento:",
"procedure":" Para saber sobre horrios:"
},
"pricing":{
"information":" Aqui esto as informaes sobre preos:",
"availability":" Sobre valores e custos:",
"procedure":" Para informaes de preos:"
},
"contact":{
"information":" Aqui esto as informaes de contato:",
"availability":" Sobre como entrar em contato:",
"procedure":" Para contatar:"
},
"service":{
"information":" Aqui esto as informaes sobre servios:",
"availability":" Sobre os servios disponveis:",
"procedure":" Para informaes de servios:"
},
"general":{
"information":" Aqui esto as informaes que encontrei:",
"availability":"Sobre sua pergunta:",
"procedure":" Para esclarecer sua dvida:"
}
}

returnintros.get(question_type,{}).get(intent,"")

def_format_knowledge(self,knowledge:List[Dict[str,Any]],analysis:Dict[str,Any])->str:
        """Formata conhecimento em resposta"""

ifnotknowledge:
            return""

best_knowledge=knowledge[0]
content=best_knowledge.get("content","")

ifanalysis["type"]=="schedule":
            returnself._extract_schedule_info(content)
elifanalysis["type"]=="pricing":
            returnself._extract_pricing_info(content)
elifanalysis["type"]=="contact":
            returnself._extract_contact_info(content)
else:
            returncontent

def_extract_schedule_info(self,content:str)->str:
        """Extrai informaes de horrio do contedo"""

time_patterns=[
r'(\w+):\s*(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)',
r'(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)',
r'(\w+)\s+(?:a|s|as)\s+(\w+):\s*(\d{1,2}h(?:\s*s\s*\d{1,2}h)?)'
]

schedule_info=[]
forpatternintime_patterns:
            matches=re.findall(pattern,content,re.IGNORECASE)
formatchinmatches:
                iflen(match)==2:
                    schedule_info.append(f" {match[0]}: {match[1]}")
eliflen(match)==3:
                    schedule_info.append(f" {match[0]} a {match[1]}: {match[2]}")
else:
                    schedule_info.append(f" {match[0]}")

ifschedule_info:
            return"\n".join(schedule_info[:5])

returncontent

def_extract_pricing_info(self,content:str)->str:
        """Extrai informaes de preo do contedo"""

price_patterns=[
r'([^:]+):\s*R\$\s*(\d+(?:[.,]\d+)?)',
r'R\$\s*(\d+(?:[.,]\d+)?)\s*([^.,\n]+)',
r'(\d+(?:[.,]\d+)?)\s*reais?\s*([^.,\n]+)'
]

price_info=[]
forpatterninprice_patterns:
            matches=re.findall(pattern,content,re.IGNORECASE)
formatchinmatches:
                iflen(match)==2:
                    price_info.append(f" {match[0].strip()}: R$ {match[1]}")

ifprice_info:
            return"\n".join(price_info[:5])

returncontent

def_extract_contact_info(self,content:str)->str:
        """Extrai informaes de contato do contedo"""

contact_info=[]

emails=re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',content)
foremailinemails:
            contact_info.append(f" Email: {email}")

phones=re.findall(r'\(?\d{2}\)?\s*\d{4,5}-?\d{4}',content)
forphoneinphones:
            contact_info.append(f" Telefone: {phone}")

addresses=re.findall(r'(?:Rua|Av|Avenida|R\.|Alameda|Praa)\s+[^,\n]+',content,re.IGNORECASE)
foraddressinaddresses:
            contact_info.append(f" Endereo: {address.strip()}")

ifcontact_info:
            return"\n".join(contact_info[:5])

returncontent

def_format_templates(self,templates:List[Dict[str,Any]],analysis:Dict[str,Any])->str:
        """Formata templates em resposta"""

ifnottemplates:
            return""

best_template=templates[0]
returnbest_template.get("content","")

def_extract_specific_information(self,knowledge:List[Dict[str,Any]],analysis:Dict[str,Any])->str:
        """Extrai informaes especficas baseadas na anlise"""

ifnotknowledge:
            return""

specific_info=[]

foriteminknowledge:
            structured_info=item.get("structured_info",{})

ifanalysis["type"]=="schedule"andstructured_info.get("schedules"):
                forscheduleinstructured_info["schedules"]:
                    if"time"inschedule:
                        specific_info.append(f" {schedule.get('period','Funcionamento')}: {schedule['time']}")

elifanalysis["type"]=="pricing"andstructured_info.get("prices"):
                forpriceinstructured_info["prices"]:
                    if"price"inprice:
                        specific_info.append(f" {price.get('item','Item')}: R$ {price['price']}")

elifanalysis["type"]=="contact"andstructured_info.get("contacts"):
                forcontactinstructured_info["contacts"]:
                    if"value"incontact:
                        specific_info.append(f" {contact['type'].title()}: {contact['value']}")

ifspecific_info:
            return"\n".join(specific_info[:3])

return""

def_add_category_emoji(self,response:str,category:str)->str:
        """Adiciona emoji baseado na categoria"""

category_prefixes={
"academia":"[ACADEMIA]",
"supermercado":"[SUPERMERCADO]",
"restaurante":"[RESTAURANTE]",
"empresa":"[EMPRESA]"
}

prefix=category_prefixes.get(category,"[INFO]")

ifnotany(ord(char)>127forcharinresponse[:10]):
            response=f"{prefix} {response}"

returnresponse

def_generate_fallback_response(self,question:str,category:str,analysis:Dict[str,Any])->str:
        """Gera resposta de fallback quando no h conhecimento especfico"""

fallback_responses={
"schedule":"No encontrei informaes especficas sobre horrios nos documentos treinados. Recomendo entrar em contato diretamente para confirmar os horrios atuais.",
"pricing":"No encontrei informaes especficas sobre preos nos documentos treinados. Recomendo verificar os valores atualizados diretamente no estabelecimento.",
"contact":"No encontrei informaes especficas de contato nos documentos treinados. Recomendo verificar o site oficial ou redes sociais.",
"service":"No encontrei informaes especficas sobre servios nos documentos treinados. Recomendo entrar em contato para mais detalhes.",
"general":"No encontrei informaes especficas sobre sua pergunta nos documentos treinados. Posso ajudar com outras questes relacionadas."
}

returnfallback_responses.get(analysis["type"],fallback_responses["general"])

def_calculate_confidence(self,knowledge:List[Dict[str,Any]],templates:List[Dict[str,Any]])->float:
        """Calcula confiana da resposta"""

ifnotknowledgeandnottemplates:
            return0.0

knowledge_confidence=sum(item.get("relevance_score",0)foriteminknowledge)/max(len(knowledge),1)
template_confidence=sum(template.get("relevance_score",0)fortemplateintemplates)/max(len(templates),1)

total_confidence=(knowledge_confidence*0.7+template_confidence*0.3)

returnmin(total_confidence,1.0)

defget_training_status(self)->Dict[str,Any]:
        """Retorna status do treinamento"""

return{
"knowledge_base_loaded":len(self.knowledge_base)>0,
"templates_loaded":len(self.response_templates)>0,
"patterns_loaded":len(self.question_patterns)>0,
"entities_loaded":len(self.entity_database)>0,
"categories_available":list(self.knowledge_base.keys()),
"total_knowledge_items":sum(len(items)foritemsinself.knowledge_base.values()),
"total_templates":sum(len(templates)fortemplatesinself.response_templates.values()),
"total_patterns":sum(len(patterns)forpatternsinself.question_patterns.values())
}
