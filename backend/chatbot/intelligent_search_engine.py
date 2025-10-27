
importre
importnltk
importspacy
fromtypingimportList,Dict,Any,Optional,Tuple,Set
fromcollectionsimportCounter,defaultdict
importnumpyasnp
fromdifflibimportSequenceMatcher
importstring
fromdatetimeimportdatetime

try:
    nltk.data.find('tokenizers/punkt')
exceptLookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
exceptLookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
exceptLookupError:
    nltk.download('wordnet')

fromnltk.tokenizeimportword_tokenize,sent_tokenize
fromnltk.corpusimportstopwords
fromnltk.stemimportWordNetLemmatizer
fromnltk.tagimportpos_tag

classIntelligentSearchEngine:
    """Sistema de busca inteligente com extrao expandida de palavras-chave"""

def__init__(self,vector_store=None,internal_doc_manager=None):
        self.vector_store=vector_store
self.internal_doc_manager=internal_doc_manager

try:
            self.nlp=spacy.load("pt_core_news_sm")
exceptOSError:
            print("Modelo spaCy portugus no encontrado. Usando modelo bsico.")
self.nlp=spacy.load("en_core_web_sm")

self.stop_words=set(stopwords.words('portuguese'))
self.stop_words.update(stopwords.words('english'))
self.lemmatizer=WordNetLemmatizer()

self.synonyms_dict={

"academia":["gym","ginsio","ginasio","fitness","musculao","musculacao","treino","exerccio","exercicio"],
"horrio":["horario","funcionamento","aberto","fechado","expediente","jornada"],
"plano":["mensalidade","preo","preco","valor","custo","taxa","pacote"],
"equipamento":["aparelho","mquina","maquina","instrumento","ferramenta"],
"aula":["modalidade","atividade","treinamento","curso","classe"],
"personal":["personal trainer","instrutor","professor","treinador"],

"supermercado":["mercado","loja","estabelecimento","comrcio","comercio"],
"produto":["item","artigo","mercadoria","bem","coisa"],
"preo":["preco","valor","custo","preo","taxa","tarifa"],
"promoo":["promocao","oferta","desconto","reduo","reducao","liquidao","liquidacao"],
"delivery":["entrega","delivery","envio","distribuio","distribuicao"],
"departamento":["seo","secao","rea","area","setor","diviso","divisao"],

"restaurante":["estabelecimento","casa","local","lugar","espao","espaco"],
"cardpio":["cardapio","menu","lista","opes","opcoes","pratos"],
"prato":["comida","refeio","refeicao","alimento","culinria","culinaria"],
"reserva":["agendamento","marcao","marcacao","booking","reservar"],
"chef":["cozinheiro","chef","mestre","especialista"],

"empresa":["organizao","organizacao","instituio","instituicao","corporao","corporacao"],
"funcionrio":["funcionario","colaborador","empregado","trabalhador","pessoa"],
"benefcio":["beneficio","vantagem","auxlio","auxilio","ajuda","suporte"],
"salrio":["salario","remunerao","remuneracao","pagamento","vencimento"],
"frias":["ferias","descanso","recesso","licena","licenca","ausncia","ausencia"],
"horrio":["horario","jornada","expediente","turno","escala"],
"trabalho":["emprego","ocupao","ocupacao","atividade","funo","funcao"],

"informao":["informacao","dados","detalhes","especificaes","especificacoes"],
"contato":["telefone","email","endereo","endereco","localizao","localizacao"],
"servio":["servico","atendimento","assistncia","assistencia","suporte"],
"poltica":["politica","regra","norma","procedimento","protocolo"],
"segurana":["seguranca","proteo","protecao","defesa","cuidado"]
}

self.context_relations={
"horrio":["funcionamento","aberto","fechado","expediente","jornada","turno","escala"],
"preo":["valor","custo","mensalidade","taxa","tarifa","desconto","promoo"],
"benefcio":["vantagem","auxlio","plano","vale","suporte","ajuda"],
"servio":["atendimento","assistncia","suporte","funcionalidade","recurso"],
"contato":["telefone","email","endereo","localizao","como chegar"],
"regra":["poltica","norma","procedimento","protocolo","cdigo"],
"equipamento":["aparelho","mquina","instrumento","ferramenta","estrutura"],
"aula":["modalidade","atividade","treinamento","curso","classe","exerccio"]
}

self.search_cache={}
self.cache_size_limit=100

defintelligent_search(self,query:str,n_results:int=5,search_all_documents:bool=True)->List[Dict[str,Any]]:
        """Busca inteligente com extrao expandida de palavras-chave"""

cache_key=f"{query.lower()}_{n_results}_{search_all_documents}"
ifcache_keyinself.search_cache:
            returnself.search_cache[cache_key]

expanded_keywords=self._extract_expanded_keywords(query)

search_queries=self._generate_search_queries(query,expanded_keywords)

all_results=[]

forsearch_queryinsearch_queries:

            ifself.vector_store:
                vector_results=self.vector_store.search(search_query,n_results=n_results*2,min_similarity=0.05)
all_results.extend(vector_results)

ifself.internal_doc_managerandsearch_all_documents:
                internal_results=self._search_internal_documents_intelligent(search_query,expanded_keywords)
all_results.extend(internal_results)

processed_results=self._process_and_rank_results(all_results,query,expanded_keywords)

final_results=processed_results[:n_results]

iflen(self.search_cache)<self.cache_size_limit:
            self.search_cache[cache_key]=final_results

returnfinal_results

def_extract_expanded_keywords(self,query:str)->Dict[str,List[str]]:
        """Extrai palavras-chave expandidas da query"""

doc=self.nlp(query)

main_keywords=[]
fortokenindoc:
            if(nottoken.is_stopand
nottoken.is_punctand
nottoken.is_spaceand
len(token.text)>2and
token.pos_in['NOUN','PROPN','ADJ','VERB']):
                main_keywords.append(token.lemma_.lower())

expanded_keywords={
"main":main_keywords,
"synonyms":[],
"related":[],
"context":[]
}

forkeywordinmain_keywords:
            ifkeywordinself.synonyms_dict:
                expanded_keywords["synonyms"].extend(self.synonyms_dict[keyword])

forkeywordinmain_keywords:
            ifkeywordinself.context_relations:
                expanded_keywords["related"].extend(self.context_relations[keyword])

contextual_terms=self._extract_contextual_terms(query,doc)
expanded_keywords["context"]=contextual_terms

forkeyinexpanded_keywords:
            expanded_keywords[key]=list(set(expanded_keywords[key]))

returnexpanded_keywords

def_extract_contextual_terms(self,query:str,doc)->List[str]:
        """Extrai termos contextuais baseados na anlise semntica"""

contextual_terms=[]

forentindoc.ents:
            ifent.label_in["PER","ORG","LOC","MISC"]:
                contextual_terms.append(ent.text.lower())

patterns={
r'\b\d+(?:[.,]\d+)?\b':"numbers",
r'\b\d{1,2}h\b':"times",
r'\b(?:segunda|tera|quarta|quinta|sexta|sbado|domingo)\b':"days",
r'\b(?:reais?|r\$|rs)\b':"currency",
r'\b(?:email|@|\.com)\b':"contact",
r'\b(?:telefone|fone|celular|whatsapp)\b':"phone"
}

forpattern,categoryinpatterns.items():
            matches=re.findall(pattern,query.lower())
contextual_terms.extend(matches)

returnlist(set(contextual_terms))

def_generate_search_queries(self,original_query:str,expanded_keywords:Dict[str,List[str]])->List[str]:
        """Gera mltiplas queries de busca baseadas nas palavras-chave expandidas"""

queries=[original_query]

ifexpanded_keywords["main"]:
            main_query=" ".join(expanded_keywords["main"])
ifmain_query!=original_query.lower():
                queries.append(main_query)

ifexpanded_keywords["synonyms"]:
            synonym_query=" ".join(expanded_keywords["synonyms"][:5])
queries.append(synonym_query)

ifexpanded_keywords["related"]:
            related_query=" ".join(expanded_keywords["related"][:5])
queries.append(related_query)

ifexpanded_keywords["main"]andexpanded_keywords["synonyms"]:
            combined_terms=expanded_keywords["main"][:3]+expanded_keywords["synonyms"][:3]
combined_query=" ".join(combined_terms)
queries.append(combined_query)

ifexpanded_keywords["context"]:
            context_query=" ".join(expanded_keywords["context"])
queries.append(context_query)

unique_queries=[]
forqueryinqueries:
            ifqueryandlen(query.strip())>2:

                is_similar=False
forexisting_queryinunique_queries:
                    similarity=SequenceMatcher(None,query.lower(),existing_query.lower()).ratio()
ifsimilarity>0.8:
                        is_similar=True
break

ifnotis_similar:
                    unique_queries.append(query)

returnunique_queries[:6]

def_search_internal_documents_intelligent(self,query:str,expanded_keywords:Dict[str,List[str]])->List[Dict[str,Any]]:
        """Busca inteligente em documentos internos"""

ifnotself.internal_doc_manager:
            return[]

try:

            all_documents=self.internal_doc_manager.list_documents()

results=[]

fordoc_infoinall_documents:
                content=self.internal_doc_manager.get_document_content(doc_info["filename"])
ifnotcontent:
                    continue

relevance_score=self._calculate_document_relevance(
content,query,expanded_keywords,doc_info
)

ifrelevance_score>0.1:
                    results.append({
"content":content,
"metadata":{
"filename":doc_info["filename"],
"category":doc_info["category"],
"timestamp":doc_info["last_modified"]
},
"similarity":relevance_score,
"source":"internal"
})

results.sort(key=lambdax:x["similarity"],reverse=True)

returnresults[:10]

exceptExceptionase:
            print(f"Erro na busca inteligente em documentos internos: {e}")
return[]

def_calculate_document_relevance(self,content:str,query:str,expanded_keywords:Dict[str,List[str]],doc_info:Dict)->float:
        """Calcula relevncia de um documento usando mltiplos critrios"""

content_lower=content.lower()
query_lower=query.lower()

basic_similarity=SequenceMatcher(None,query_lower,content_lower).ratio()

main_keyword_score=0
forkeywordinexpanded_keywords["main"]:
            ifkeywordincontent_lower:
                main_keyword_score+=1
main_keyword_score=main_keyword_score/max(len(expanded_keywords["main"]),1)

synonym_score=0
forsynonyminexpanded_keywords["synonyms"]:
            ifsynonymincontent_lower:
                synonym_score+=0.5
synonym_score=synonym_score/max(len(expanded_keywords["synonyms"]),1)

related_score=0
forrelated_terminexpanded_keywords["related"]:
            ifrelated_termincontent_lower:
                related_score+=0.3
related_score=related_score/max(len(expanded_keywords["related"]),1)

context_score=0
forcontext_terminexpanded_keywords["context"]:
            ifcontext_termincontent_lower:
                context_score+=0.2
context_score=context_score/max(len(expanded_keywords["context"]),1)

category_bonus=0
ifdoc_info.get("category"):
            category=doc_info["category"]

ifany(keywordincategoryforkeywordinexpanded_keywords["main"]):
                category_bonus=0.2

total_score=(
basic_similarity*0.3+
main_keyword_score*0.4+
synonym_score*0.15+
related_score*0.1+
context_score*0.05+
category_bonus
)

returnmin(total_score,1.0)

def_process_and_rank_results(self,all_results:List[Dict[str,Any]],original_query:str,expanded_keywords:Dict[str,List[str]])->List[Dict[str,Any]]:
        """Processa e rankeia todos os resultados"""

unique_results=[]
seen_contents=set()

forresultinall_results:
            content_hash=hash(result["content"][:100])
ifcontent_hashnotinseen_contents:
                seen_contents.add(content_hash)
unique_results.append(result)

forresultinunique_results:

            expanded_similarity=self._calculate_expanded_similarity(
result["content"],original_query,expanded_keywords
)
result["expanded_similarity"]=expanded_similarity
result["final_score"]=(result.get("similarity",0)+expanded_similarity)/2

unique_results.sort(key=lambdax:x["final_score"],reverse=True)

returnunique_results

def_calculate_expanded_similarity(self,content:str,query:str,expanded_keywords:Dict[str,List[str]])->float:
        """Calcula similaridade expandida considerando todas as palavras-chave"""

content_lower=content.lower()

original_similarity=SequenceMatcher(None,query.lower(),content_lower).ratio()

keyword_matches=0
total_keywords=0

forcategory,keywordsinexpanded_keywords.items():
            forkeywordinkeywords:
                total_keywords+=1
ifkeywordincontent_lower:

                    ifcategory=="main":
                        keyword_matches+=1.0
elifcategory=="synonyms":
                        keyword_matches+=0.7
elifcategory=="related":
                        keyword_matches+=0.5
elifcategory=="context":
                        keyword_matches+=0.3

keyword_similarity=keyword_matches/max(total_keywords,1)

combined_similarity=(original_similarity*0.4+keyword_similarity*0.6)

returnmin(combined_similarity,1.0)

defget_search_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas do sistema de busca"""

return{
"cache_size":len(self.search_cache),
"synonyms_loaded":len(self.synonyms_dict),
"context_relations":len(self.context_relations),
"spacy_model":self.nlp.meta.get("name","unknown"),
"stop_words_count":len(self.stop_words)
}

defclear_cache(self):
        """Limpa o cache de buscas"""
self.search_cache.clear()

defadd_custom_synonyms(self,word:str,synonyms:List[str]):
        """Adiciona sinnimos customizados"""
ifwordnotinself.synonyms_dict:
            self.synonyms_dict[word]=[]
self.synonyms_dict[word].extend(synonyms)
self.synonyms_dict[word]=list(set(self.synonyms_dict[word]))

defadd_context_relation(self,term:str,related_terms:List[str]):
        """Adiciona relao contextual customizada"""
iftermnotinself.context_relations:
            self.context_relations[term]=[]
self.context_relations[term].extend(related_terms)
self.context_relations[term]=list(set(self.context_relations[term]))
