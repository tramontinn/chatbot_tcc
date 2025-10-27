importos
importjson
importnumpyasnp
fromtypingimportList,Dict,Any,Optional,Tuple
fromdatetimeimportdatetime
importuuid
fromsklearn.feature_extraction.textimportTfidfVectorizer
fromsklearn.metrics.pairwiseimportcosine_similarity
importpickle
frompathlibimportPath
importtime
fromfunctoolsimportlru_cache

classOptimizedVectorStore:
    """Sistema de busca vetorial otimizado com cache inteligente"""

def__init__(self,persist_directory:str="./local_vector_db"):
        self.persist_directory=Path(persist_directory)
self.persist_directory.mkdir(exist_ok=True)

self.vectorizer=TfidfVectorizer(
max_features=1000,
stop_words=None,
ngram_range=(1,2),
min_df=1,
max_df=0.8
)

self.documents={}
self.document_vectors=None
self.document_ids=[]

self._search_cache={}
self._search_cache_ttl=1800
self._last_search_time={}

self._category_vectors={}
self._category_documents={}

self.metadata_file=self.persist_directory/"metadata.json"
self.vectors_file=self.persist_directory/"vectors.pkl"
self.vectorizer_file=self.persist_directory/"vectorizer.pkl"

self._load_data()

ifself.documents:
            self._preprocess_categories()

def_load_data(self):
        """Carrega dados persistidos"""
try:

            ifself.metadata_file.exists():
                withopen(self.metadata_file,'r',encoding='utf-8')asf:
                    self.documents=json.load(f)

ifself.vectors_file.exists():
                withopen(self.vectors_file,'rb')asf:
                    self.document_vectors=pickle.load(f)

ifself.vectorizer_file.exists():
                withopen(self.vectorizer_file,'rb')asf:
                    self.vectorizer=pickle.load(f)

self.document_ids=list(self.documents.keys())

exceptExceptionase:
            print(f"Erro ao carregar dados: {e}")
self.documents={}
self.document_vectors=None
self.document_ids=[]

def_save_data(self):
        """Salva dados no disco"""
try:

            withopen(self.metadata_file,'w',encoding='utf-8')asf:
                json.dump(self.documents,f,ensure_ascii=False,indent=2)

ifself.document_vectorsisnotNone:
                withopen(self.vectors_file,'wb')asf:
                    pickle.dump(self.document_vectors,f)

withopen(self.vectorizer_file,'wb')asf:
                pickle.dump(self.vectorizer,f)

exceptExceptionase:
            print(f"Erro ao salvar dados: {e}")

def_preprocess_categories(self):
        """Pr-processa documentos por categoria para busca mais rpida"""
try:
            self._category_documents={}
self._category_vectors={}

fordoc_id,doc_datainself.documents.items():
                category=doc_data["metadata"].get("category","geral")

ifcategorynotinself._category_documents:
                    self._category_documents[category]=[]
self._category_vectors[category]=None

self._category_documents[category].append(doc_id)

forcategory,doc_idsinself._category_documents.items():
                iflen(doc_ids)>0:
                    texts=[self.documents[doc_id]["content"]fordoc_idindoc_ids]
self._category_vectors[category]=self.vectorizer.transform(texts)

print(f" Categorias pr-processadas: {list(self._category_documents.keys())}")

exceptExceptionase:
            print(f"Erro ao pr-processar categorias: {e}")

defadd_documents(self,texts:List[str],filenames:List[str],metadata_list:Optional[List[Dict]]=None)->bool:
        """Adiciona documentos ao banco vetorial"""
try:
            iflen(texts)!=len(filenames):
                raiseValueError("Nmero de textos deve ser igual ao nmero de nomes de arquivo")

ifmetadata_listisNone:
                metadata_list=[{}for_intexts]

new_doc_ids=[]
fori,(text,filename,metadata)inenumerate(zip(texts,filenames,metadata_list)):
                doc_id=str(uuid.uuid4())

full_metadata={
"filename":filename,
"timestamp":datetime.now().isoformat(),
"size":len(text),
"processed":True,
**metadata
}

self.documents[doc_id]={
"content":text,
"metadata":full_metadata
}
new_doc_ids.append(doc_id)

self.document_ids.extend(new_doc_ids)

self._rebuild_vectors()

self._preprocess_categories()

self._search_cache.clear()

self._save_data()

returnTrue

exceptExceptionase:
            print(f"Erro ao adicionar documentos: {e}")
returnFalse

def_rebuild_vectors(self):
        """Recalcula todos os vetores TF-IDF"""
try:
            ifnotself.documents:
                self.document_vectors=None
return

texts=[self.documents[doc_id]["content"]fordoc_idinself.document_ids]

self.document_vectors=self.vectorizer.fit_transform(texts)

exceptExceptionase:
            print(f"Erro ao recalcular vetores: {e}")
self.document_vectors=None

defsearch(self,query:str,n_results:int=5,min_similarity:float=0.1,category:Optional[str]=None)->List[Dict[str,Any]]:
        """Busca documentos similares  query com cache otimizado"""
try:

            cache_key=f"{query}_{n_results}_{min_similarity}_{categoryor'all'}"
current_time=time.time()

if(cache_keyinself._search_cacheand
cache_keyinself._last_search_timeand
current_time-self._last_search_time[cache_key]<self._search_cache_ttl):
                returnself._search_cache[cache_key]

ifnotself.documentsorself.document_vectorsisNone:
                return[]

ifcategoryandcategoryinself._category_documents:
                results=self._search_by_category(query,category,n_results,min_similarity)
else:
                results=self._search_global(query,n_results,min_similarity)

self._search_cache[cache_key]=results
self._last_search_time[cache_key]=current_time

returnresults

exceptExceptionase:
            print(f"Erro na busca: {e}")
return[]

def_search_by_category(self,query:str,category:str,n_results:int,min_similarity:float)->List[Dict[str,Any]]:
        """Busca otimizada por categoria"""
try:
            doc_ids=self._category_documents[category]
category_vectors=self._category_vectors[category]

ifnotdoc_idsorcategory_vectorsisNone:
                return[]

query_vector=self.vectorizer.transform([query])

similarities=cosine_similarity(query_vector,category_vectors).flatten()

sorted_indices=np.argsort(similarities)[::-1]

results=[]
foridxinsorted_indices:
                ifsimilarities[idx]>=min_similarityandlen(results)<n_results:
                    doc_id=doc_ids[idx]
doc_data=self.documents[doc_id]

results.append({
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"similarity":float(similarities[idx]),
"id":doc_id
})

returnresults

exceptExceptionase:
            print(f"Erro na busca por categoria: {e}")
return[]

def_search_global(self,query:str,n_results:int,min_similarity:float)->List[Dict[str,Any]]:
        """Busca global otimizada"""
try:

            query_vector=self.vectorizer.transform([query])

similarities=cosine_similarity(query_vector,self.document_vectors).flatten()

sorted_indices=np.argsort(similarities)[::-1]

results=[]
foridxinsorted_indices:
                ifsimilarities[idx]>=min_similarityandlen(results)<n_results:
                    doc_id=self.document_ids[idx]
doc_data=self.documents[doc_id]

results.append({
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"similarity":float(similarities[idx]),
"id":doc_id
})

returnresults

exceptExceptionase:
            print(f"Erro na busca global: {e}")
return[]

defsearch_by_category(self,category:str,n_results:int=10)->List[Dict[str,Any]]:
        """Busca documentos por categoria"""
try:
            ifcategorynotinself._category_documents:
                return[]

results=[]
fordoc_idinself._category_documents[category]:
                doc_data=self.documents[doc_id]
results.append({
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"id":doc_id
})

returnresults[:n_results]

exceptExceptionase:
            print(f"Erro na busca por categoria: {e}")
return[]

defsearch_similar_documents(self,doc_id:str,n_results:int=5)->List[Dict[str,Any]]:
        """Busca documentos similares a um documento especfico"""
try:
            ifdoc_idnotinself.documents:
                return[]

doc_index=self.document_ids.index(doc_id)

doc_vector=self.document_vectors[doc_index:doc_index+1]
similarities=cosine_similarity(doc_vector,self.document_vectors).flatten()

sorted_indices=np.argsort(similarities)[::-1]

results=[]
foridxinsorted_indices:
                ifidx!=doc_indexandlen(results)<n_results:
                    similar_doc_id=self.document_ids[idx]
doc_data=self.documents[similar_doc_id]

results.append({
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"similarity":float(similarities[idx]),
"id":similar_doc_id
})

returnresults

exceptExceptionase:
            print(f"Erro na busca de documentos similares: {e}")
return[]

defget_document_by_id(self,doc_id:str)->Optional[Dict[str,Any]]:
        """Obtm um documento especfico por ID"""
ifdoc_idinself.documents:
            doc_data=self.documents[doc_id]
return{
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"id":doc_id
}
returnNone

defupdate_document(self,doc_id:str,new_content:str,new_metadata:Optional[Dict]=None)->bool:
        """Atualiza um documento existente"""
try:
            ifdoc_idnotinself.documents:
                returnFalse

self.documents[doc_id]["content"]=new_content

ifnew_metadata:
                self.documents[doc_id]["metadata"].update(new_metadata)

self._rebuild_vectors()

self._preprocess_categories()

self._search_cache.clear()

self._save_data()

returnTrue

exceptExceptionase:
            print(f"Erro ao atualizar documento: {e}")
returnFalse

defdelete_document(self,doc_id:str)->bool:
        """Remove um documento do sistema"""
try:
            ifdoc_idnotinself.documents:
                returnFalse

delself.documents[doc_id]

ifdoc_idinself.document_ids:
                self.document_ids.remove(doc_id)

self._rebuild_vectors()

self._preprocess_categories()

self._search_cache.clear()

self._save_data()

returnTrue

exceptExceptionase:
            print(f"Erro ao remover documento: {e}")
returnFalse

defdelete_document_by_filename(self,filename:str)->bool:
        """Remove um documento pelo nome do arquivo"""
try:
            doc_id_to_remove=None
fordoc_id,doc_datainself.documents.items():
                ifdoc_data["metadata"]["filename"]==filename:
                    doc_id_to_remove=doc_id
break

ifdoc_id_to_remove:
                returnself.delete_document(doc_id_to_remove)

returnFalse

exceptExceptionase:
            print(f"Erro ao remover documento por filename: {e}")
returnFalse

deflist_documents(self)->List[Dict[str,Any]]:
        """Lista todos os documentos no sistema"""
documents=[]
fordoc_id,doc_datainself.documents.items():
            metadata=doc_data["metadata"]
documents.append({
"filename":metadata["filename"],
"content_type":metadata.get("content_type","text/plain"),
"size":metadata["size"],
"processed":metadata["processed"],
"timestamp":metadata["timestamp"],
"category":metadata.get("category","geral"),
"id":doc_id
})

returnsorted(documents,key=lambdax:x["timestamp"],reverse=True)

defget_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas do banco vetorial"""
total_docs=len(self.documents)

iftotal_docs==0:
            return{
"total_documents":0,
"total_size_bytes":0,
"total_size_mb":0,
"categories":{},
"vector_dimensions":0,
"cache_size":len(self._search_cache)
}

total_size=sum(doc["metadata"]["size"]fordocinself.documents.values())

categories={}
fordoc_datainself.documents.values():
            category=doc_data["metadata"].get("category","geral")
categories[category]=categories.get(category,0)+1

vector_dimensions=self.document_vectors.shape[1]ifself.document_vectorsisnotNoneelse0

return{
"total_documents":total_docs,
"total_size_bytes":total_size,
"total_size_mb":round(total_size/(1024*1024),2),
"categories":categories,
"vector_dimensions":vector_dimensions,
"cache_size":len(self._search_cache),
"preprocessed_categories":list(self._category_documents.keys())
}

defclear_all(self)->bool:
        """Remove todos os documentos do sistema"""
try:
            self.documents={}
self.document_ids=[]
self.document_vectors=None
self._category_documents={}
self._category_vectors={}
self._search_cache.clear()
self._last_search_time.clear()

forfile_pathin[self.metadata_file,self.vectors_file,self.vectorizer_file]:
                iffile_path.exists():
                    file_path.unlink()

returnTrue

exceptExceptionase:
            print(f"Erro ao limpar banco: {e}")
returnFalse

defrebuild_index(self)->bool:
        """Reconstri o ndice vetorial"""
try:
            self._rebuild_vectors()
self._preprocess_categories()
self._search_cache.clear()
self._save_data()
returnTrue
exceptExceptionase:
            print(f"Erro ao reconstruir ndice: {e}")
returnFalse

defclear_cache(self):
        """Limpa o cache de busca"""
self._search_cache.clear()
self._last_search_time.clear()
print(" Cache de busca limpo")

defget_cache_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache"""
return{
"search_cache_size":len(self._search_cache),
"category_cache_size":len(self._category_documents),
"cache_ttl":self._search_cache_ttl
}
