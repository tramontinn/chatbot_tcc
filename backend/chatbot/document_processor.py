importPyPDF2
importdocx
fromfastapiimportUploadFile
importio
importre
fromtypingimportList,Optional
frompathlibimportPath

classDocumentProcessor:
    """Processa diferentes tipos de documentos e extrai texto"""

def__init__(self):
        self.supported_types={
"application/pdf":self._process_pdf,
"text/plain":self._process_txt,
"text/markdown":self._process_txt,
"application/vnd.openxmlformats-officedocument.wordprocessingml.document":self._process_docx,
"application/rtf":self._process_rtf
}

asyncdefprocess_file(self,file:UploadFile)->str:
        """Processa um arquivo e retorna o texto extrado"""
iffile.content_typenotinself.supported_types:
            raiseValueError(f"Tipo de arquivo no suportado: {file.content_type}")

content=awaitfile.read()

processor=self.supported_types[file.content_type]
text=processor(content)

cleaned_text=self._clean_text(text)

returncleaned_text

def_process_pdf(self,content:bytes)->str:
        """Processa arquivo PDF"""
try:
            pdf_file=io.BytesIO(content)
pdf_reader=PyPDF2.PdfReader(pdf_file)

text=""
forpageinpdf_reader.pages:
                text+=page.extract_text()+"\n"

returntext
exceptExceptionase:
            raiseValueError(f"Erro ao processar PDF: {str(e)}")

def_process_txt(self,content:bytes)->str:
        """Processa arquivo de texto"""
try:

            encodings=['utf-8','latin-1','cp1252']

forencodinginencodings:
                try:
                    returncontent.decode(encoding)
exceptUnicodeDecodeError:
                    continue

raiseValueError("No foi possvel decodificar o arquivo de texto")
exceptExceptionase:
            raiseValueError(f"Erro ao processar arquivo de texto: {str(e)}")

def_process_docx(self,content:bytes)->str:
        """Processa arquivo DOCX"""
try:
            doc_file=io.BytesIO(content)
doc=docx.Document(doc_file)

text=""
forparagraphindoc.paragraphs:
                text+=paragraph.text+"\n"

returntext
exceptExceptionase:
            raiseValueError(f"Erro ao processar DOCX: {str(e)}")

def_process_rtf(self,content:bytes)->str:
        """Processa arquivo RTF (bsico)"""
try:

            text=content.decode('utf-8',errors='ignore')

text=re.sub(r'\\[a-z]+\d*\s?','',text)
text=re.sub(r'[{}]','',text)
text=re.sub(r'\\[\\{}]','',text)

returntext
exceptExceptionase:
            raiseValueError(f"Erro ao processar RTF: {str(e)}")

def_read_file_content(self,file_path:str)->str:
        """L contedo de um arquivo do sistema de arquivos"""
try:
            file_path=Path(file_path)

ifnotfile_path.exists():
                raiseFileNotFoundError(f"Arquivo no encontrado: {file_path}")

extension=file_path.suffix.lower()

ifextensionin['.txt','.md']:
                withopen(file_path,'r',encoding='utf-8')asf:
                    returnf.read()
elifextension=='.pdf':
                withopen(file_path,'rb')asf:
                    returnself._process_pdf(f.read())
elifextension=='.docx':
                withopen(file_path,'rb')asf:
                    returnself._process_docx(f.read())
elifextension=='.rtf':
                withopen(file_path,'rb')asf:
                    returnself._process_rtf(f.read())
else:
                raiseValueError(f"Tipo de arquivo no suportado: {extension}")

exceptExceptionase:
            raiseValueError(f"Erro ao ler arquivo {file_path}: {str(e)}")

def_clean_text(self,text:str)->str:
        """Limpa e normaliza o texto extrado"""

text=re.sub(r'\s+',' ',text)
text=re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]','',text)

text=re.sub(r'\n\s*\n','\n\n',text)

text=text.strip()

returntext

defsplit_text(self,text:str,chunk_size:int=1000,overlap:int=200)->List[str]:
        """Divide o texto em chunks para processamento"""
chunks=[]
start=0

whilestart<len(text):
            end=start+chunk_size

ifend<len(text):

                last_space=text.rfind(' ',start,end)
iflast_space>start:
                    end=last_space

chunk=text[start:end].strip()
ifchunk:
                chunks.append(chunk)

start=end-overlap
ifstart>=len(text):
                break

returnchunks
