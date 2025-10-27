
importrandom
importre
importtime
fromtypingimportDict,List,Any,Optional,Tuple
fromdatetimeimportdatetime,timedelta
fromdataclassesimportdataclass
importjson
importlogging
frompathlibimportPath

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

@dataclass
classResponseTemplate:
    """Template de resposta humanizada"""
template_id:str
category:str
question_pattern:str
templates:List[str]
context_variables:List[str]
personality_traits:Dict[str,float]
usage_count:int=0
success_rate:float=0.0
last_used:float=0.0

@dataclass
classPersonalityProfile:
    """Perfil de personalidade do chatbot"""
name:str
traits:Dict[str,float]
greeting_style:str
farewell_style:str
response_style:str

classHumanizedResponseGenerator:
    """Gerador de respostas humanizadas com personalidade e templates dinmicos"""

def__init__(self,data_dir:str="./learning_data"):
        self.data_dir=Path(data_dir)
self.data_dir.mkdir(exist_ok=True)

self.templates_file=self.data_dir/"response_templates.json"
self.personality_file=self.data_dir/"personality_profile.json"

self.personality=PersonalityProfile(
name="Assistente IA",
traits={
"amigvel":0.8,
"profissional":0.9,
"emptico":0.7,
"direto":0.6,
"prestativo":0.9,
"conversacional":0.7
},
greeting_style="warm",
farewell_style="polite",
response_style="helpful"
)

self.response_templates:Dict[str,ResponseTemplate]={}

self.context_variables={
"time_of_day":self._get_time_of_day(),
"day_of_week":datetime.now().strftime("%A"),
"user_name":None,
"session_count":0,
"last_interaction":None
}

self._initialize_default_templates()
self._load_templates()
self._load_personality()

logger.info("Gerador de respostas humanizadas inicializado")

def_get_time_of_day(self)->str:
        """Obtm perodo do dia"""
hour=datetime.now().hour
if5<=hour<12:
            return"manh"
elif12<=hour<18:
            return"tarde"
else:
            return"noite"

def_initialize_default_templates(self):
        """Inicializa templates padro"""

self.response_templates["greeting"]=ResponseTemplate(
template_id="greeting",
category="social",
question_pattern="saudao",
templates=[
"Ol! {greeting_time} Como posso ajud-lo hoje?",
"Oi! {greeting_time} Em que posso ser til?",
"Ol! {greeting_time} Estou aqui para responder suas perguntas.",
"Oi! {greeting_time} Como posso auxili-lo?",
"Ol! {greeting_time} Fico feliz em ajudar!"
],
context_variables=["greeting_time"],
personality_traits={"amigvel":0.9,"prestativo":0.9}
)

self.response_templates["farewell"]=ResponseTemplate(
template_id="farewell",
category="social",
question_pattern="despedida",
templates=[
"At logo! Foi um prazer ajud-lo.",
"Tchau! Se precisar de mais alguma coisa, estarei aqui.",
"At a prxima! Tenha um bom dia.",
"At mais! Fico  disposio para outras dvidas.",
"Tchau! Espero ter ajudado."
],
context_variables=[],
personality_traits={"amigvel":0.8,"emptico":0.7}
)

self.response_templates["thanks"]=ResponseTemplate(
template_id="thanks",
category="social",
question_pattern="agradecimento",
templates=[
"De nada! Fico feliz em ajudar.",
"Por nada! Se precisar de mais alguma coisa,  s perguntar.",
"Disponha! Estou aqui para isso.",
"De nada! Foi um prazer ajudar.",
"Por nada! Sempre  disposio."
],
context_variables=[],
personality_traits={"amigvel":0.8,"prestativo":0.9}
)

self.response_templates["horario"]=ResponseTemplate(
template_id="horario",
category="horario",
question_pattern="horrio|horario|trabalho|expediente",
templates=[
"Com base no manual do funcionrio, aqui esto as informaes sobre horrio de trabalho:\n\n{content}\n\nEsta  uma poltica importante para manter o equilbrio entre vida pessoal e profissional.",
"Sobre horrios de trabalho, encontrei estas informaes:\n\n{content}\n\nSe precisar de mais detalhes ou tiver alguma situao especfica, posso ajudar com mais informaes.",
"Aqui esto as informaes sobre horrio de trabalho:\n\n{content}\n\n importante seguir esses horrios para manter a organizao da equipe.",
"Encontrei as seguintes informaes sobre horrios:\n\n{content}\n\nSe tiver dvidas sobre horrios especiais ou excees, consulte o RH."
],
context_variables=["content"],
personality_traits={"profissional":0.9,"prestativo":0.8}
)

self.response_templates["beneficios"]=ResponseTemplate(
template_id="beneficios",
category="beneficios",
question_pattern="benefcio|beneficio|vale|plano",
templates=[
"Aqui esto todos os benefcios oferecidos pela empresa:\n\n{content}\n\nEsses benefcios so parte do pacote de remunerao e visam melhorar sua qualidade de vida.",
"Sobre os benefcios disponveis:\n\n{content}\n\nSe tiver dvidas sobre como utilizar algum deles, posso esclarecer mais detalhes.",
"Encontrei estas informaes sobre benefcios:\n\n{content}\n\nPara esclarecimentos sobre benefcios especficos, entre em contato com o departamento de RH.",
"Aqui esto os benefcios oferecidos:\n\n{content}\n\nCada benefcio tem suas regras especficas, ento no hesite em perguntar se precisar de mais detalhes."
],
context_variables=["content"],
personality_traits={"profissional":0.9,"emptico":0.7}
)

self.response_templates["ferias"]=ResponseTemplate(
template_id="ferias",
category="ferias",
question_pattern="frias|ferias|descanso",
templates=[
"Aqui esto as informaes completas sobre frias:\n\n{content}\n\nAs frias so um direito importante para seu descanso e bem-estar.",
"Sobre frias, encontrei estas informaes:\n\n{content}\n\n recomendado planejar com antecedncia e comunicar ao RH sobre suas preferncias de datas.",
"Encontrei as seguintes informaes sobre frias:\n\n{content}\n\nLembre-se de que o planejamento antecipado  fundamental para uma boa experincia.",
"Aqui esto as informaes sobre frias:\n\n{content}\n\nAs frias so essenciais para sua sade e produtividade."
],
context_variables=["content"],
personality_traits={"emptico":0.8,"profissional":0.8}
)

self.response_templates["licenca"]=ResponseTemplate(
template_id="licenca",
category="licenca",
question_pattern="licena|licenca|mdica|medica|atestado",
templates=[
"Informaes sobre licena mdica e atestados:\n\n{content}\n\nSua sade  prioridade. Em caso de necessidade, no hesite em procurar atendimento mdico.",
"Sobre licenas mdicas:\n\n{content}\n\n importante seguir os procedimentos adequados para comunicar sua ausncia.",
"Encontrei estas informaes sobre licena mdica:\n\n{content}\n\nSempre priorize sua sade e siga as orientaes mdicas.",
"Aqui esto as informaes sobre licenas:\n\n{content}\n\nEm caso de dvidas sobre procedimentos, consulte o RH."
],
context_variables=["content"],
personality_traits={"emptico":0.9,"profissional":0.8}
)

self.response_templates["vestimenta"]=ResponseTemplate(
template_id="vestimenta",
category="vestimenta",
question_pattern="vestimenta|roupa|traje|cdigo|codigo",
templates=[
"Cdigo de vestimenta da empresa:\n\n{content}\n\nO cdigo de vestimenta visa manter um ambiente profissional e respeitoso.",
"Sobre o cdigo de vestimenta:\n\n{content}\n\nEm dias especiais ou eventos, pode haver orientaes especficas do RH.",
"Encontrei estas informaes sobre vestimenta:\n\n{content}\n\n importante seguir essas diretrizes para manter a imagem profissional da empresa.",
"Aqui esto as orientaes sobre vestimenta:\n\n{content}\n\nEm caso de dvidas, consulte o RH ou seu supervisor."
],
context_variables=["content"],
personality_traits={"profissional":0.9,"direto":0.7}
)

self.response_templates["comunicacao"]=ResponseTemplate(
template_id="comunicacao",
category="comunicacao",
question_pattern="comunicao|comunicacao|contato|email",
templates=[
"Canais de comunicao interna:\n\n{content}\n\nA comunicao eficaz  fundamental para o sucesso da equipe.",
"Sobre comunicao na empresa:\n\n{content}\n\nUse o canal mais apropriado para cada tipo de assunto.",
"Encontrei estas informaes sobre comunicao:\n\n{content}\n\nUma boa comunicao  essencial para o trabalho em equipe.",
"Aqui esto os canais de comunicao:\n\n{content}\n\nCada canal tem seu propsito especfico, ento escolha o mais adequado."
],
context_variables=["content"],
personality_traits={"profissional":0.8,"prestativo":0.8}
)

self.response_templates["seguranca"]=ResponseTemplate(
template_id="seguranca",
category="seguranca",
question_pattern="segurana|seguranca|carto|cartao|acesso",
templates=[
"Polticas de segurana da empresa:\n\n{content}\n\nA segurana  responsabilidade de todos.",
"Sobre segurana no trabalho:\n\n{content}\n\nMantenha-se sempre alerta e siga as diretrizes para proteger informaes e recursos da empresa.",
"Encontrei estas informaes sobre segurana:\n\n{content}\n\n fundamental seguir todos os protocolos de segurana.",
"Aqui esto as polticas de segurana:\n\n{content}\n\nEm caso de incidentes, reporte imediatamente ao responsvel."
],
context_variables=["content"],
personality_traits={"profissional":0.9,"direto":0.8}
)

self.response_templates["limpeza"]=ResponseTemplate(
template_id="limpeza",
category="limpeza",
question_pattern="limpeza|organizao|organizacao",
templates=[
"Diretrizes de limpeza e organizao:\n\n{content}\n\nUm ambiente limpo e organizado contribui para a produtividade de toda a equipe.",
"Sobre limpeza e organizao:\n\n{content}\n\nCada um faz sua parte para manter um ambiente agradvel.",
"Encontrei estas informaes sobre limpeza:\n\n{content}\n\nA organizao  fundamental para um bom ambiente de trabalho.",
"Aqui esto as diretrizes de limpeza:\n\n{content}\n\nVamos todos colaborar para manter o ambiente organizado."
],
context_variables=["content"],
personality_traits={"amigvel":0.7,"prestativo":0.8}
)

self.response_templates["treinamento"]=ResponseTemplate(
template_id="treinamento",
category="treinamento",
question_pattern="treinamento|curso|capacitao|capacitacao",
templates=[
"Oportunidades de desenvolvimento:\n\n{content}\n\nO crescimento profissional  valorizado na empresa.",
"Sobre treinamentos e desenvolvimento:\n\n{content}\n\nAproveite as oportunidades de aprendizado para expandir suas habilidades.",
"Encontrei estas informaes sobre treinamentos:\n\n{content}\n\nO investimento em capacitao  uma prioridade da empresa.",
"Aqui esto as oportunidades de desenvolvimento:\n\n{content}\n\nParticipe ativamente dos programas de capacitao disponveis."
],
context_variables=["content"],
personality_traits={"prestativo":0.9,"emptico":0.7}
)

self.response_templates["rh"]=ResponseTemplate(
template_id="rh",
category="rh",
question_pattern="rh|recursos humanos|funcionrio|funcionario",
templates=[
"Informaes sobre recursos humanos:\n\n{content}\n\nO RH est sempre disponvel para esclarecer dvidas.",
"Sobre recursos humanos:\n\n{content}\n\nPara questes especficas, entre em contato diretamente com o RH.",
"Encontrei estas informaes sobre RH:\n\n{content}\n\nO departamento de RH  seu ponto de apoio para questes trabalhistas.",
"Aqui esto as informaes sobre recursos humanos:\n\n{content}\n\nNo hesite em procurar o RH quando precisar de orientao."
],
context_variables=["content"],
personality_traits={"profissional":0.9,"emptico":0.8}
)

self.response_templates["fallback"]=ResponseTemplate(
template_id="fallback",
category="geral",
question_pattern=".*",
templates=[
"Encontrei algumas informaes que podem ser relevantes para sua pergunta:\n\n{content}\n\nSe precisar de mais detalhes ou tiver outras dvidas, fique  vontade para perguntar!",
"Baseado nos documentos disponveis:\n\n{content}\n\nEsta  a informao mais completa que encontrei. Se precisar de esclarecimentos adicionais, posso ajudar!",
"Aqui esto as informaes que encontrei:\n\n{content}\n\nSe a resposta no foi completa o suficiente, me avise que posso buscar mais detalhes.",
"Encontrei estas informaes relevantes:\n\n{content}\n\nEspero ter ajudado! Se tiver mais perguntas, estarei aqui."
],
context_variables=["content"],
personality_traits={"prestativo":0.9,"amigvel":0.8}
)

def_load_templates(self):
        """Carrega templates do arquivo"""
try:
            ifself.templates_file.exists():
                withopen(self.templates_file,'r',encoding='utf-8')asf:
                    data=json.load(f)
self.response_templates={
k:ResponseTemplate(**v)fork,vindata.items()
}
exceptExceptionase:
            logger.error(f"Erro ao carregar templates: {e}")

def_save_templates(self):
        """Salva templates no arquivo"""
try:
            data={k:{
"template_id":v.template_id,
"category":v.category,
"question_pattern":v.question_pattern,
"templates":v.templates,
"context_variables":v.context_variables,
"personality_traits":v.personality_traits,
"usage_count":v.usage_count,
"success_rate":v.success_rate,
"last_used":v.last_used
}fork,vinself.response_templates.items()}

withopen(self.templates_file,'w',encoding='utf-8')asf:
                json.dump(data,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            logger.error(f"Erro ao salvar templates: {e}")

def_load_personality(self):
        """Carrega perfil de personalidade"""
try:
            ifself.personality_file.exists():
                withopen(self.personality_file,'r',encoding='utf-8')asf:
                    data=json.load(f)
self.personality=PersonalityProfile(**data)
exceptExceptionase:
            logger.error(f"Erro ao carregar personalidade: {e}")

def_save_personality(self):
        """Salva perfil de personalidade"""
try:
            data={
"name":self.personality.name,
"traits":self.personality.traits,
"greeting_style":self.personality.greeting_style,
"farewell_style":self.personality.farewell_style,
"response_style":self.personality.response_style
}

withopen(self.personality_file,'w',encoding='utf-8')asf:
                json.dump(data,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            logger.error(f"Erro ao salvar personalidade: {e}")

def_get_greeting_time(self)->str:
        """Obtm saudao baseada no horrio"""
time_of_day=self.context_variables["time_of_day"]

iftime_of_day=="manh":
            return"Bom dia!"
eliftime_of_day=="tarde":
            return"Boa tarde!"
else:
            return"Boa noite!"

def_select_template(self,category:str,question:str)->ResponseTemplate:
        """Seleciona template apropriado baseado na categoria e pergunta"""

ifcategoryinself.response_templates:
            template=self.response_templates[category]

ifre.search(template.question_pattern,question.lower()):
                returntemplate

fortemplateinself.response_templates.values():
            ifre.search(template.question_pattern,question.lower()):
                returntemplate

returnself.response_templates["fallback"]

def_apply_personality_modifications(self,template:str,category:str)->str:
        """Aplica modificaes baseadas na personalidade"""
modified_template=template

ifself.personality.traits.get("amigvel",0)>0.7:

            friendly_additions=[
" "," Espero ter ajudado!"," Fico feliz em ajudar!",
" Qualquer dvida,  s perguntar!"
]
ifrandom.random()<0.3:
                modified_template+=random.choice(friendly_additions)

ifself.personality.traits.get("emptico",0)>0.7:

            empathetic_additions=[
" Entendo sua preocupao."," Sei que isso  importante para voc.",
" Compreendo sua situao."," Espero que isso ajude."
]
ifrandom.random()<0.2:
                modified_template+=random.choice(empathetic_additions)

ifself.personality.traits.get("profissional",0)>0.8:

            ifnotany(wordinmodified_template.lower()forwordin["obrigado","disponha","prazer"]):
                professional_endings=[
" Fico  disposio para esclarecer outras dvidas.",
" Para mais informaes, consulte a documentao oficial.",
" Em caso de dvidas adicionais, entre em contato com o RH."
]
ifrandom.random()<0.4:
                    modified_template+=random.choice(professional_endings)

returnmodified_template

def_fill_template_variables(self,template:str,content:str="",**kwargs)->str:
        """Preenche variveis do template"""
filled_template=template

variables={
"content":content,
"greeting_time":self._get_greeting_time(),
"time_of_day":self.context_variables["time_of_day"],
"day_of_week":self.context_variables["day_of_week"],
**kwargs
}

forvar_name,var_valueinvariables.items():
            placeholder=f"{{var_name}}"
ifplaceholderinfilled_template:
                filled_template=filled_template.replace(placeholder,str(var_value))

returnfilled_template

defgenerate_humanized_response(self,question:str,content:str,
category:Optional[str]=None,
session_context:Optional[Dict[str,Any]]=None)->str:
        """Gera resposta humanizada baseada no template apropriado"""
try:

            ifsession_context:
                self.context_variables.update(session_context)

ifnotcategory:
                category=self._categorize_question(question)

template_obj=self._select_template(category,question)

template=random.choice(template_obj.templates)

filled_template=self._fill_template_variables(template,content)

humanized_response=self._apply_personality_modifications(filled_template,category)

template_obj.usage_count+=1
template_obj.last_used=time.time()

self._save_templates()

returnhumanized_response

exceptExceptionase:
            logger.error(f"Erro ao gerar resposta humanizada: {e}")
returncontent

def_categorize_question(self,question:str)->str:
        """Categoriza pergunta para seleo de template"""
question_lower=question.lower()

category_keywords={
"horario":["horrio","horario","trabalho","expediente","entrada","sada"],
"beneficios":["benefcio","beneficio","vale","plano","sade","saude"],
"ferias":["frias","ferias","descanso","recesso"],
"licenca":["licena","licenca","mdica","medica","atestado"],
"vestimenta":["vestimenta","roupa","traje","cdigo","codigo"],
"comunicacao":["comunicao","comunicacao","contato","email"],
"seguranca":["segurana","seguranca","carto","cartao","acesso"],
"limpeza":["limpeza","organizao","organizacao"],
"treinamento":["treinamento","curso","capacitao","capacitacao"],
"rh":["rh","recursos humanos","funcionrio","funcionario"]
}

forcategory,keywordsincategory_keywords.items():
            ifany(keywordinquestion_lowerforkeywordinkeywords):
                returncategory

return"geral"

defupdate_personality_trait(self,trait:str,value:float):
        """Atualiza trao de personalidade"""
if0<=value<=1:
            self.personality.traits[trait]=value
self._save_personality()
logger.info(f"Trao de personalidade '{trait}' atualizado para {value}")

defadd_custom_template(self,category:str,question_pattern:str,
templates:List[str],personality_traits:Dict[str,float]):
        """Adiciona template personalizado"""
template_id=f"custom_{category}_{int(time.time())}"

new_template=ResponseTemplate(
template_id=template_id,
category=category,
question_pattern=question_pattern,
templates=templates,
context_variables=["content"],
personality_traits=personality_traits
)

self.response_templates[template_id]=new_template
self._save_templates()

logger.info(f"Template personalizado adicionado: {template_id}")

defget_template_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas dos templates"""
stats={
"total_templates":len(self.response_templates),
"categories":{},
"most_used":[],
"personality_traits":self.personality.traits
}

fortemplateinself.response_templates.values():
            category=template.category
ifcategorynotinstats["categories"]:
                stats["categories"][category]={
"count":0,
"total_usage":0,
"avg_success_rate":0.0
}

stats["categories"][category]["count"]+=1
stats["categories"][category]["total_usage"]+=template.usage_count

forcategory,datainstats["categories"].items():
            templates_in_category=[
tfortinself.response_templates.values()
ift.category==category
]
iftemplates_in_category:
                data["avg_success_rate"]=sum(t.success_ratefortintemplates_in_category)/len(templates_in_category)

most_used=sorted(
self.response_templates.values(),
key=lambdat:t.usage_count,
reverse=True
)[:5]

stats["most_used"]=[
{
"template_id":t.template_id,
"category":t.category,
"usage_count":t.usage_count,
"success_rate":t.success_rate
}
fortinmost_used
]

returnstats

defoptimize_templates(self):
        """Otimiza templates baseado no uso e sucesso"""
try:

            current_time=time.time()
cutoff_time=current_time-(30*24*60*60)

templates_to_remove=[]
fortemplate_id,templateinself.response_templates.items():
                if(template.last_used<cutoff_timeand
template.usage_count<5and
template_id.startswith("custom_")):
                    templates_to_remove.append(template_id)

fortemplate_idintemplates_to_remove:
                delself.response_templates[template_id]

fortemplateinself.response_templates.values():
                iftemplate.usage_count>0:

                    template.templates.sort(key=lambdat:random.random())

self._save_templates()

iftemplates_to_remove:
                logger.info(f"Otimizao concluda: {len(templates_to_remove)} templates removidos")

exceptExceptionase:
            logger.error(f"Erro na otimizao de templates: {e}")

humanized_response_generator=HumanizedResponseGenerator()
