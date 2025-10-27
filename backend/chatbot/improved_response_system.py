
importjson
importos
fromtypingimportDict,List,Optional,Any

classImprovedResponseSystem:
    def__init__(self,improvements_file:str="chatbot_improvements.json"):
        self.improvements_file=improvements_file
self.templates={}
self.keyword_matching={}
self.fallback_responses={}

self.load_improvements()

defload_improvements(self):
        """Carrega as melhorias do arquivo JSON"""
try:
            ifos.path.exists(self.improvements_file):
                withopen(self.improvements_file,'r',encoding='utf-8')asf:
                    data=json.load(f)

self.templates=data.get('templates',{})
self.keyword_matching=data.get('keyword_matching',{})
self.fallback_responses=data.get('fallback_responses',{})

print(f"Carregadas {len(self.templates)} templates melhorados")
else:
                print("Arquivo de melhorias não encontrado, usando sistema padrão")
exceptExceptionase:
            print(f"Erro ao carregar melhorias: {e}")

defmatch_keywords(self,message:str)->Optional[str]:
        """Encontra correspondência de palavras-chave na mensagem"""
message_lower=message.lower()

forcategory,datainself.keyword_matching.items():
            keywords=data.get('keywords',[])
template_name=data.get('response_template','')

forkeywordinkeywords:
                ifkeyword.lower()inmessage_lower:
                    returntemplate_name

returnNone

defget_improved_response(self,message:str,domain:str=None)->Optional[str]:
        """Gera resposta melhorada baseada na mensagem"""

template_name=self.match_keywords(message)

iftemplate_nameandtemplate_nameinself.templates:
            returnself.templates[template_name]

ifdomain:
            domain_responses=self._get_domain_specific_responses(domain,message)
ifdomain_responses:
                returndomain_responses

returnNone

def_get_domain_specific_responses(self,domain:str,message:str)->Optional[str]:
        """Gera respostas específicas por domínio"""
message_lower=message.lower()

ifdomain=="empresa":

            ifany(wordinmessage_lowerforwordin["benefício","beneficio","vale","plano"]):
                returnself.templates.get("beneficios_empresa")

ifany(wordinmessage_lowerforwordin["férias","ferias","vacation","descanso"]):
                returnself.templates.get("politica_ferias")

elifdomain=="academia":

            ifany(wordinmessage_lowerforwordin["aula","aulas","musculação","spinning","pilates","yoga"]):
                returnself.templates.get("aulas_academia")

elifdomain=="restaurante":

            ifany(wordinmessage_lowerforwordin["cardápio","cardapio","prato","menu","risotto","salmão"]):
                returnself.templates.get("cardapio_restaurante")

ifany(wordinmessage_lowerforwordin["delivery","entrega","pedido","app"]):
                returnself.templates.get("delivery_restaurante")

elifdomain=="supermercado":

            ifany(wordinmessage_lowerforwordin["fidelidade","pontos","cashback","cartão"]):
                returnself.templates.get("programa_fidelidade")

ifany(wordinmessage_lowerforwordin["troca","devolução","garantia","nota fiscal"]):
                returnself.templates.get("politica_troca")

ifany(wordinmessage_lowerforwordin["contato","telefone","whatsapp","email","site"]):
            returnself.templates.get("contatos_gerais")

returnNone

defget_fallback_response(self,message:str,context:Dict[str,Any]=None)->str:
        """Gera resposta de fallback melhorada"""

ifself.fallback_responses:
            if"generic"inself.fallback_responses:
                returnself.fallback_responses["generic"]
elif"not_found"inself.fallback_responses:
                returnself.fallback_responses["not_found"]

return"Encontrei informações relevantes nos documentos, mas preciso de mais detalhes específicos. Pode reformular sua pergunta?"

defenhance_existing_response(self,response:str,message:str,domain:str=None)->str:
        """Melhora uma resposta existente com informações adicionais"""

improved_response=self.get_improved_response(message,domain)

ifimproved_response:
            returnimproved_response

returnresponse

defget_response_quality_score(self,response:str,expected_keywords:List[str])->float:
        """Calcula score de qualidade da resposta"""
ifnotresponseornotexpected_keywords:
            return0.0

response_lower=response.lower()
keywords_found=[kwforkwinexpected_keywordsifkw.lower()inresponse_lower]

keyword_score=len(keywords_found)/len(expected_keywords)ifexpected_keywordselse0

length_score=min(len(response)/200,1.0)

specific_info_score=0.0
ifany(indicatorinresponse_lowerforindicatorin["r$","horário","horario","telefone","email","site"]):
            specific_info_score=0.3

final_score=(keyword_score*0.5+length_score*0.3+specific_info_score)

returnmin(final_score,1.0)

defmain():
    """Função principal para teste"""
print("Sistema de Respostas Inteligentes Melhoradas")
print("="*50)

response_system=ImprovedResponseSystem()

test_questions=[
"Quais são os benefícios oferecidos aos funcionários?",
"Como funciona a política de férias?",
"Que aulas são oferecidas na academia?",
"Qual é o cardápio do restaurante?",
"Como funciona o delivery?",
"Qual é o programa de fidelidade?",
"Qual é a política de troca e devolução?",
"Quais são os contatos para mais informações?"
]

print("\nTestando respostas melhoradas:")
print("-"*50)

forquestionintest_questions:
        response=response_system.get_improved_response(question)
ifresponse:
            print(f"Pergunta: {question}")
print(f"Resposta: {response[:100]}...")
print("-"*30)
else:
            print(f"Pergunta: {question}")
print("Resposta: Nenhuma resposta melhorada encontrada")
print("-"*30)

if__name__=="__main__":
    main()
