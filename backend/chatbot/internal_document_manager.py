importos
importjson
importhashlib
fromtypingimportList,Dict,Any,Optional
fromdatetimeimportdatetime
importshutil
frompathlibimportPath

classInternalDocumentManager:
    """Gerencia documentos internos do sistema de forma segura"""

def__init__(self,internal_docs_path:str="internal_documents"):
        self.internal_docs_path=Path(internal_docs_path)
self.metadata_file=self.internal_docs_path/"documents_metadata.json"

self.internal_docs_path.mkdir(exist_ok=True)

self.documents_metadata=self._load_metadata()

self.allowed_extensions={'.txt','.pdf','.docx','.md','.rtf'}

self._scan_existing_documents()

def_load_metadata(self)->Dict[str,Any]:
        """Carrega metadata dos documentos"""
ifself.metadata_file.exists():
            try:
                withopen(self.metadata_file,'r',encoding='utf-8')asf:
                    returnjson.load(f)
exceptExceptionase:
                print(f"Erro ao carregar metadata: {e}")
return{}

def_save_metadata(self):
        """Salva metadata dos documentos"""
try:
            withopen(self.metadata_file,'w',encoding='utf-8')asf:
                json.dump(self.documents_metadata,f,ensure_ascii=False,indent=2)
exceptExceptionase:
            print(f"Erro ao salvar metadata: {e}")

def_scan_existing_documents(self):
        """Escaneia documentos existentes na pasta interna"""
forfile_pathinself.internal_docs_path.iterdir():
            iffile_path.is_file()andfile_path.suffix.lower()inself.allowed_extensions:
                iffile_path.namenotinself.documents_metadata:
                    self._add_document_metadata(file_path)

def_add_document_metadata(self,file_path:Path):
        """Adiciona metadata de um documento"""
try:
            file_hash=self._calculate_file_hash(file_path)
file_size=file_path.stat().st_size
modified_time=datetime.fromtimestamp(file_path.stat().st_mtime)

self.documents_metadata[file_path.name]={
"filename":file_path.name,
"file_path":str(file_path),
"file_hash":file_hash,
"size":file_size,
"created":modified_time.isoformat(),
"last_modified":modified_time.isoformat(),
"processed":False,
"content_type":self._get_content_type(file_path.suffix),
"category":self._categorize_document(file_path.name)
}

self._save_metadata()

exceptExceptionase:
            print(f"Erro ao adicionar metadata do arquivo {file_path.name}: {e}")

def_calculate_file_hash(self,file_path:Path)->str:
        """Calcula hash do arquivo para verificar integridade"""
hash_md5=hashlib.md5()
try:
            withopen(file_path,"rb")asf:
                forchunkiniter(lambda:f.read(4096),b""):
                    hash_md5.update(chunk)
returnhash_md5.hexdigest()
exceptExceptionase:
            print(f"Erro ao calcular hash do arquivo {file_path.name}: {e}")
return""

def_get_content_type(self,extension:str)->str:
        """Retorna o tipo de contedo baseado na extenso"""
content_types={
'.txt':'text/plain',
'.md':'text/markdown',
'.pdf':'application/pdf',
'.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'.rtf':'application/rtf'
}
returncontent_types.get(extension.lower(),'application/octet-stream')

def_categorize_document(self,filename:str)->str:
        """Categoriza o documento baseado no nome"""
filename_lower=filename.lower()

ifany(wordinfilename_lowerforwordin['academia','gym','fitness','musculao','musculacao']):
            return'academia'
elifany(wordinfilename_lowerforwordin['supermercado','mercado','loja','compras']):
            return'supermercado'
elifany(wordinfilename_lowerforwordin['restaurante','comida','jantar','almoo','almoco']):
            return'restaurante'
elifany(wordinfilename_lowerforwordin['funcionario','funcionrio','empresa','trabalho','rh']):
            return'empresa'
elifany(wordinfilename_lowerforwordin['manual','guia','instruo']):
            return'manual'
elifany(wordinfilename_lowerforwordin['poltica','regulamento','norma']):
            return'politica'
elifany(wordinfilename_lowerforwordin['procedimento','processo','fluxo']):
            return'procedimento'
elifany(wordinfilename_lowerforwordin['treinamento','curso','capacitao']):
            return'treinamento'
elifany(wordinfilename_lowerforwordin['relatrio','anlise','estudo']):
            return'relatorio'
else:
            return'geral'

defadd_document(self,source_path:str,filename:Optional[str]=None)->bool:
        """Adiciona um documento  pasta interna"""
try:
            source=Path(source_path)

ifnotsource.exists():
                print(f"Arquivo no encontrado: {source_path}")
returnFalse

ifsource.suffix.lower()notinself.allowed_extensions:
                print(f"Tipo de arquivo no permitido: {source.suffix}")
returnFalse

ifnotfilename:
                filename=source.name

iffilenameinself.documents_metadata:
                print(f"Documento j existe: {filename}")
returnFalse

dest_path=self.internal_docs_path/filename
shutil.copy2(source,dest_path)

self._add_document_metadata(dest_path)

print(f"Documento adicionado com sucesso: {filename}")
returnTrue

exceptExceptionase:
            print(f"Erro ao adicionar documento: {e}")
returnFalse

defremove_document(self,filename:str)->bool:
        """Remove um documento da pasta interna"""
try:
            iffilenamenotinself.documents_metadata:
                print(f"Documento no encontrado: {filename}")
returnFalse

file_path=Path(self.documents_metadata[filename]["file_path"])
iffile_path.exists():
                file_path.unlink()

delself.documents_metadata[filename]
self._save_metadata()

print(f"Documento removido com sucesso: {filename}")
returnTrue

exceptExceptionase:
            print(f"Erro ao remover documento: {e}")
returnFalse

deflist_documents(self)->List[Dict[str,Any]]:
        """Lista todos os documentos internos"""
documents=[]
forfilename,metadatainself.documents_metadata.items():
            documents.append({
"filename":metadata["filename"],
"content_type":metadata["content_type"],
"size":metadata["size"],
"category":metadata["category"],
"created":metadata["created"],
"last_modified":metadata["last_modified"],
"processed":metadata["processed"]
})

returnsorted(documents,key=lambdax:x["last_modified"],reverse=True)

defget_document_path(self,filename:str)->Optional[str]:
        """Retorna o caminho completo de um documento"""
iffilenameinself.documents_metadata:
            returnself.documents_metadata[filename]["file_path"]
returnNone

defget_document_content(self,filename:str)->Optional[str]:
        """L o contedo de um documento"""
try:
            file_path=self.get_document_path(filename)
ifnotfile_pathornotPath(file_path).exists():
                returnNone

iffilename.endswith('.txt')orfilename.endswith('.md'):
                withopen(file_path,'r',encoding='utf-8')asf:
                    returnf.read()
else:

                from.document_processorimportDocumentProcessor
processor=DocumentProcessor()
returnprocessor._read_file_content(file_path)

exceptExceptionase:
            print(f"Erro ao ler contedo do documento {filename}: {e}")
returnNone

defmark_as_processed(self,filename:str,processed:bool=True):
        """Marca um documento como processado ou no processado"""
iffilenameinself.documents_metadata:
            self.documents_metadata[filename]["processed"]=processed
self._save_metadata()

defget_unprocessed_documents(self)->List[str]:
        """Retorna lista de documentos no processados"""
return[filenameforfilename,metadatainself.documents_metadata.items()
ifnotmetadata.get("processed",False)]

defget_documents_by_category(self,category:str)->List[Dict[str,Any]]:
        """Retorna documentos de uma categoria especfica"""
return[docfordocinself.list_documents()ifdoc["category"]==category]

defsearch_documents(self,query:str)->List[Dict[str,Any]]:
        """Busca documentos por nome ou categoria"""
query_lower=query.lower()
results=[]

fordocinself.list_documents():
            if(query_lowerindoc["filename"].lower()or
query_lowerindoc["category"].lower()):
                results.append(doc)

returnresults

defget_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas dos documentos"""
total_docs=len(self.documents_metadata)
processed_docs=sum(1formetadatainself.documents_metadata.values()
ifmetadata.get("processed",False))
total_size=sum(metadata["size"]formetadatainself.documents_metadata.values())

categories={}
formetadatainself.documents_metadata.values():
            category=metadata.get("category","geral")
categories[category]=categories.get(category,0)+1

return{
"total_documents":total_docs,
"processed_documents":processed_docs,
"unprocessed_documents":total_docs-processed_docs,
"total_size_bytes":total_size,
"total_size_mb":round(total_size/(1024*1024),2),
"categories":categories
}
