
importtime
importjson
importpickle
importhashlib
importthreading
fromtypingimportAny,Dict,List,Optional,Tuple,Union
frompathlibimportPath
fromdatetimeimportdatetime,timedelta
fromcollectionsimportOrderedDict
importlogging
importasyncio
fromdataclassesimportdataclass,asdict
importsqlite3
importnumpyasnp

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

@dataclass
classCacheEntry:
    """Entrada do cache com metadados"""
key:str
value:Any
created_at:float
last_accessed:float
access_count:int
ttl:Optional[float]=None
size_bytes:int=0
tags:List[str]=None

def__post_init__(self):
        ifself.tagsisNone:
            self.tags=[]
ifself.size_bytes==0:
            self.size_bytes=self._calculate_size()

def_calculate_size(self)->int:
        """Calcula tamanho aproximado da entrada"""
try:
            ifisinstance(self.value,(str,bytes)):
                returnlen(self.value)
elifisinstance(self.value,np.ndarray):
                returnself.value.nbytes
else:
                returnlen(pickle.dumps(self.value))
except:
            return1024

defis_expired(self)->bool:
        """Verifica se a entrada expirou"""
ifself.ttlisNone:
            returnFalse
returntime.time()-self.created_at>self.ttl

deftouch(self):
        """Atualiza ltimo acesso"""
self.last_accessed=time.time()
self.access_count+=1

classIntelligentCacheManager:
    """Gerenciador de cache inteligente com mltiplas estratgias"""

def__init__(self,
max_memory_size:int=100*1024*1024,
max_disk_size:int=500*1024*1024,
default_ttl:float=3600,
cache_dir:str="./cache",
enable_disk_cache:bool=True,
enable_compression:bool=True):

        self.max_memory_size=max_memory_size
self.max_disk_size=max_disk_size
self.default_ttl=default_ttl
self.cache_dir=Path(cache_dir)
self.cache_dir.mkdir(exist_ok=True)
self.enable_disk_cache=enable_disk_cache
self.enable_compression=enable_compression

self.memory_cache:OrderedDict[str,CacheEntry]=OrderedDict()
self.current_memory_size=0

self.db_path=self.cache_dir/"cache.db"
self._init_database()

self.stats={
'hits':0,
'misses':0,
'evictions':0,
'disk_hits':0,
'disk_misses':0,
'total_requests':0
}

self.cleanup_thread=threading.Thread(target=self._cleanup_worker,daemon=True)
self.cleanup_thread.start()

self.lock=threading.RLock()

logger.info(f"Cache inteligente inicializado - Memria: {max_memory_size//1024//1024}MB, Disco: {max_disk_size//1024//1024}MB")

def_init_database(self):
        """Inicializa banco de dados SQLite para cache em disco"""
ifnotself.enable_disk_cache:
            return

try:
            withsqlite3.connect(self.db_path)asconn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS cache_entries (
                        key TEXT PRIMARY KEY,
                        value BLOB,
                        created_at REAL,
                        last_accessed REAL,
                        access_count INTEGER,
                        ttl REAL,
                        size_bytes INTEGER,
                        tags TEXT,
                        compressed INTEGER DEFAULT 0
                    )
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_created_at ON cache_entries(created_at)
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_last_accessed ON cache_entries(last_accessed)
                '''
)

conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_tags ON cache_entries(tags)
                '''
)

conn.commit()
exceptExceptionase:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
self.enable_disk_cache=False

def_cleanup_worker(self):
        """Worker thread para limpeza automtica do cache"""
whileTrue:
            try:
                time.sleep(300)
self._cleanup_expired()
self._cleanup_disk()
exceptExceptionase:
                logger.error(f"Erro no worker de limpeza: {e}")

def_cleanup_expired(self):
        """Remove entradas expiradas do cache em memria"""
withself.lock:
            expired_keys=[]
forkey,entryinself.memory_cache.items():
                ifentry.is_expired():
                    expired_keys.append(key)

forkeyinexpired_keys:
                delself.memory_cache[key]
self.current_memory_size-=self.memory_cache[key].size_bytesifkeyinself.memory_cacheelse0

ifexpired_keys:
                logger.info(f"Removidas {len(expired_keys)} entradas expiradas do cache")

def_cleanup_disk(self):
        """Remove entradas expiradas do cache em disco"""
ifnotself.enable_disk_cache:
            return

try:
            current_time=time.time()
withsqlite3.connect(self.db_path)asconn:
                cursor=conn.execute('''
                    DELETE FROM cache_entries 
                    WHERE ttl IS NOT NULL AND (created_at + ttl) < ?
                '''
,(current_time,))

deleted_count=cursor.rowcount
conn.commit()

ifdeleted_count>0:
                    logger.info(f"Removidas {deleted_count} entradas expiradas do cache em disco")
exceptExceptionase:
            logger.error(f"Erro na limpeza do cache em disco: {e}")

def_generate_key(self,*args,**kwargs)->str:
        """Gera chave nica baseada nos argumentos"""
key_data={
'args':args,
'kwargs':sorted(kwargs.items())ifkwargselse{}
}
key_str=json.dumps(key_data,sort_keys=True,default=str)
returnhashlib.md5(key_str.encode()).hexdigest()

def_evict_lru(self):
        """Remove entradas menos recentemente usadas"""
withself.lock:
            whileself.current_memory_size>self.max_memory_sizeandself.memory_cache:

                key,entry=self.memory_cache.popitem(last=False)
self.current_memory_size-=entry.size_bytes
self.stats['evictions']+=1

ifself.enable_disk_cache:
                    self._save_to_disk(key,entry)

def_save_to_disk(self,key:str,entry:CacheEntry):
        """Salva entrada no cache em disco"""
try:

            ifself.enable_compression:
                importgzip
value_data=gzip.compress(pickle.dumps(entry.value))
compressed=1
else:
                value_data=pickle.dumps(entry.value)
compressed=0

withsqlite3.connect(self.db_path)asconn:
                conn.execute('''
                    INSERT OR REPLACE INTO cache_entries 
                    (key, value, created_at, last_accessed, access_count, ttl, size_bytes, tags, compressed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
,(
key,value_data,entry.created_at,entry.last_accessed,
entry.access_count,entry.ttl,entry.size_bytes,
json.dumps(entry.tags),compressed
))
conn.commit()
exceptExceptionase:
            logger.error(f"Erro ao salvar no cache em disco: {e}")

def_load_from_disk(self,key:str)->Optional[CacheEntry]:
        """Carrega entrada do cache em disco"""
ifnotself.enable_disk_cache:
            returnNone

try:
            withsqlite3.connect(self.db_path)asconn:
                cursor=conn.execute('''
                    SELECT value, created_at, last_accessed, access_count, ttl, size_bytes, tags, compressed
                    FROM cache_entries WHERE key = ?
                '''
,(key,))

row=cursor.fetchone()
ifnotrow:
                    returnNone

value_data,created_at,last_accessed,access_count,ttl,size_bytes,tags_json,compressed=row

ifcompressed:
                    importgzip
value=pickle.loads(gzip.decompress(value_data))
else:
                    value=pickle.loads(value_data)

tags=json.loads(tags_json)iftags_jsonelse[]

entry=CacheEntry(
key=key,
value=value,
created_at=created_at,
last_accessed=last_accessed,
access_count=access_count,
ttl=ttl,
size_bytes=size_bytes,
tags=tags
)

ifentry.is_expired():
                    self._remove_from_disk(key)
returnNone

returnentry
exceptExceptionase:
            logger.error(f"Erro ao carregar do cache em disco: {e}")
returnNone

def_remove_from_disk(self,key:str):
        """Remove entrada do cache em disco"""
try:
            withsqlite3.connect(self.db_path)asconn:
                conn.execute('DELETE FROM cache_entries WHERE key = ?',(key,))
conn.commit()
exceptExceptionase:
            logger.error(f"Erro ao remover do cache em disco: {e}")

defget(self,key:str,default:Any=None)->Any:
        """Obtm valor do cache"""
self.stats['total_requests']+=1

withself.lock:

            ifkeyinself.memory_cache:
                entry=self.memory_cache[key]

ifentry.is_expired():
                    delself.memory_cache[key]
self.current_memory_size-=entry.size_bytes
self.stats['misses']+=1
returndefault

self.memory_cache.move_to_end(key)
entry.touch()
self.stats['hits']+=1
returnentry.value

entry=self._load_from_disk(key)
ifentryisnotNone:

                self.memory_cache[key]=entry
self.current_memory_size+=entry.size_bytes
self.memory_cache.move_to_end(key)
entry.touch()
self.stats['disk_hits']+=1
self.stats['hits']+=1
returnentry.value

self.stats['misses']+=1
returndefault

defset(self,key:str,value:Any,ttl:Optional[float]=None,tags:List[str]=None)->bool:
        """Define valor no cache"""
ifttlisNone:
            ttl=self.default_ttl

iftagsisNone:
            tags=[]

entry=CacheEntry(
key=key,
value=value,
created_at=time.time(),
last_accessed=time.time(),
access_count=1,
ttl=ttl,
tags=tags
)

withself.lock:

            ifkeyinself.memory_cache:
                old_entry=self.memory_cache[key]
self.current_memory_size-=old_entry.size_bytes

self.memory_cache[key]=entry
self.current_memory_size+=entry.size_bytes
self.memory_cache.move_to_end(key)

ifself.current_memory_size>self.max_memory_size:
                self._evict_lru()

returnTrue

defdelete(self,key:str)->bool:
        """Remove entrada do cache"""
withself.lock:
            removed=False

ifkeyinself.memory_cache:
                entry=self.memory_cache[key]
delself.memory_cache[key]
self.current_memory_size-=entry.size_bytes
removed=True

ifself.enable_disk_cache:
                self._remove_from_disk(key)
removed=True

returnremoved

defclear(self,tags:List[str]=None):
        """Limpa cache (opcionalmente por tags)"""
withself.lock:
            iftags:

                keys_to_remove=[]
forkey,entryinself.memory_cache.items():
                    ifany(taginentry.tagsfortagintags):
                        keys_to_remove.append(key)

forkeyinkeys_to_remove:
                    entry=self.memory_cache[key]
delself.memory_cache[key]
self.current_memory_size-=entry.size_bytes

ifself.enable_disk_cache:
                    try:
                        withsqlite3.connect(self.db_path)asconn:
                            fortagintags:
                                conn.execute('''
                                    DELETE FROM cache_entries 
                                    WHERE tags LIKE ?
                                '''
,(f'%{tag}%',))
conn.commit()
exceptExceptionase:
                        logger.error(f"Erro ao limpar cache em disco por tags: {e}")
else:

                self.memory_cache.clear()
self.current_memory_size=0

ifself.enable_disk_cache:
                    try:
                        withsqlite3.connect(self.db_path)asconn:
                            conn.execute('DELETE FROM cache_entries')
conn.commit()
exceptExceptionase:
                        logger.error(f"Erro ao limpar cache em disco: {e}")

definvalidate_by_tags(self,tags:List[str]):
        """Invalida entradas por tags"""
self.clear(tags)

defget_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache"""
hit_rate=self.stats['hits']/max(self.stats['total_requests'],1)*100
disk_hit_rate=self.stats['disk_hits']/max(self.stats['hits'],1)*100

return{
'memory_entries':len(self.memory_cache),
'memory_size_mb':self.current_memory_size/1024/1024,
'max_memory_size_mb':self.max_memory_size/1024/1024,
'hit_rate':hit_rate,
'disk_hit_rate':disk_hit_rate,
'total_requests':self.stats['total_requests'],
'hits':self.stats['hits'],
'misses':self.stats['misses'],
'evictions':self.stats['evictions'],
'disk_hits':self.stats['disk_hits']
}

defget_disk_stats(self)->Dict[str,Any]:
        """Retorna estatsticas do cache em disco"""
ifnotself.enable_disk_cache:
            return{'enabled':False}

try:
            withsqlite3.connect(self.db_path)asconn:
                cursor=conn.execute('SELECT COUNT(*), SUM(size_bytes) FROM cache_entries')
count,total_size=cursor.fetchone()

return{
'enabled':True,
'entries':countor0,
'size_mb':(total_sizeor0)/1024/1024,
'max_size_mb':self.max_disk_size/1024/1024,
'db_path':str(self.db_path)
}
exceptExceptionase:
            logger.error(f"Erro ao obter estatsticas do disco: {e}")
return{'enabled':True,'error':str(e)}

defoptimize(self):
        """Otimiza o cache removendo entradas antigas e pouco usadas"""
withself.lock:

            current_time=time.time()
keys_to_remove=[]

forkey,entryinself.memory_cache.items():
                age=current_time-entry.created_at
access_rate=entry.access_count/max(age/3600,1)

ifage>86400andaccess_rate<0.1:
                    keys_to_remove.append(key)

forkeyinkeys_to_remove:
                entry=self.memory_cache[key]
delself.memory_cache[key]
self.current_memory_size-=entry.size_bytes

ifkeys_to_remove:
                logger.info(f"Otimizao: removidas {len(keys_to_remove)} entradas antigas")

defcache_function(self,ttl:Optional[float]=None,tags:List[str]=None):
        """Decorator para cache de funes"""
defdecorator(func):
            defwrapper(*args,**kwargs):

                key=self._generate_key(func.__name__,*args,**kwargs)

result=self.get(key)
ifresultisnotNone:
                    returnresult

result=func(*args,**kwargs)
self.set(key,result,ttl,tags)
returnresult

returnwrapper
returndecorator

defasync_cache_function(self,ttl:Optional[float]=None,tags:List[str]=None):
        """Decorator para cache de funes assncronas"""
defdecorator(func):
            asyncdefwrapper(*args,**kwargs):

                key=self._generate_key(func.__name__,*args,**kwargs)

result=self.get(key)
ifresultisnotNone:
                    returnresult

result=awaitfunc(*args,**kwargs)
self.set(key,result,ttl,tags)
returnresult

returnwrapper
returndecorator

cache_manager=IntelligentCacheManager()

defcached(ttl:Optional[float]=None,tags:List[str]=None):
    """Decorator para cache de funes sncronas"""
returncache_manager.cache_function(ttl,tags)

defasync_cached(ttl:Optional[float]=None,tags:List[str]=None):
    """Decorator para cache de funes assncronas"""
returncache_manager.async_cache_function(ttl,tags)
