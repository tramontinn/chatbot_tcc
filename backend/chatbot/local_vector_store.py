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

classLocalVectorStore:
    """Sistema de busca vetorial local usando TF-IDF"""

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

self.metadata_file=self.persist_directory/"metadata.json"
self.vectors_file=self.persist_directory/"vectors.pkl"
self.vectorizer_file=self.persist_directory/"vectorizer.pkl"

self._load_data()

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

defsearch(self,query:str,n_results:int=5,min_similarity:float=0.1)->List[Dict[str,Any]]:
        """Busca documentos similares  query"""
try:
            ifnotself.documentsorself.document_vectorsisNone:
                return[]

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
            print(f"Erro na busca: {e}")
return[]

defsearch_by_category(self,category:str,n_results:int=10)->List[Dict[str,Any]]:
        """Busca documentos por categoria"""
try:
            results=[]
fordoc_id,doc_datainself.documents.items():
                ifdoc_data["metadata"].get("category")==category:
                    results.append({
"content":doc_data["content"],
"metadata":doc_data["metadata"],
"id":doc_id
})

returnresults[:n_results]

exceptExceptionase:
            print(f"Erro na busca por categoria: {e}")
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
"vector_dimensions":0
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
"vector_dimensions":vector_dimensions
}

defclear_all(self)->bool:
        """Remove todos os documentos do sistema"""
try:
            self.documents={}
self.document_ids=[]
self.document_vectors=None

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
self._save_data()
returnTrue
exceptExceptionase:
            print(f"Erro ao reconstruir ndice: {e}")
returnFalse
