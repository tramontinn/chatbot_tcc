
importasyncio
importtime
importthreading
fromtypingimportDict,List,Any,Optional,Callable,Union
fromconcurrent.futuresimportThreadPoolExecutor
fromdataclassesimportdataclass
importlogging
frompathlibimportPath
importweakref
importgc
fromfunctoolsimportwraps,lru_cache
importqueue
importjson
importos

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

@dataclass
classPerformanceMetrics:
    """Mtricas de performance"""
response_time:float
memory_usage:float
cpu_usage:float
cache_hit_rate:float
concurrent_requests:int
timestamp:float

@dataclass
classAsyncTask:
    """Tarefa assncrona"""
task_id:str
function:Callable
args:tuple
kwargs:dict
priority:int=0
created_at:float=0.0
timeout:Optional[float]=None

classLazyLoader:
    """Carregador preguioso para modelos e recursos"""

def__init__(self):
        self._loaded_objects={}
self._loading_locks={}
self._loading_threads={}

defload_lazy(self,key:str,loader_func:Callable,*args,**kwargs):
        """Carrega objeto de forma preguiosa"""
ifkeyinself._loaded_objects:
            returnself._loaded_objects[key]

ifkeyinself._loading_locks:

            withself._loading_locks[key]:
                ifkeyinself._loaded_objects:
                    returnself._loaded_objects[key]

self._loading_locks[key]=threading.Lock()

withself._loading_locks[key]:

            ifkeyinself._loaded_objects:
                returnself._loaded_objects[key]

logger.info(f"Carregando objeto: {key}")
start_time=time.time()

try:
                obj=loader_func(*args,**kwargs)
self._loaded_objects[key]=obj

load_time=time.time()-start_time
logger.info(f"Objeto {key} carregado em {load_time:.2f}s")

returnobj
exceptExceptionase:
                logger.error(f"Erro ao carregar {key}: {e}")
raise
finally:

                ifkeyinself._loading_locks:
                    delself._loading_locks[key]

defunload(self,key:str):
        """Descarrega objeto da memria"""
ifkeyinself._loaded_objects:
            delself._loaded_objects[key]
logger.info(f"Objeto {key} descarregado")

defget_loaded_objects(self)->Dict[str,Any]:
        """Retorna objetos carregados"""
returnself._loaded_objects.copy()

defclear_all(self):
        """Limpa todos os objetos carregados"""
self._loaded_objects.clear()
logger.info("Todos os objetos foram descarregados")

classAsyncTaskManager:
    """Gerenciador de tarefas assncronas"""

def__init__(self,max_workers:int=None):
        self.max_workers=max_workersormin(32,os.cpu_count()+4)
self.executor=ThreadPoolExecutor(max_workers=self.max_workers)
self.task_queue=queue.PriorityQueue()
self.running_tasks={}
self.completed_tasks={}
self.failed_tasks={}

self.queue_thread=threading.Thread(target=self._process_queue,daemon=True)
self.queue_thread.start()

logger.info(f"Gerenciador de tarefas assncronas inicializado com {self.max_workers} workers")

defsubmit_task(self,task_id:str,function:Callable,*args,
priority:int=0,timeout:Optional[float]=None,**kwargs)->str:
        """Submete tarefa assncrona"""
task=AsyncTask(
task_id=task_id,
function=function,
args=args,
kwargs=kwargs,
priority=priority,
created_at=time.time(),
timeout=timeout
)

self.task_queue.put((-priority,task))

logger.info(f"Tarefa {task_id} submetida com prioridade {priority}")
returntask_id

def_process_queue(self):
        """Processa fila de tarefas"""
whileTrue:
            try:

                priority,task=self.task_queue.get(timeout=1)

iftask.timeoutand(time.time()-task.created_at)>task.timeout:
                    self.failed_tasks[task.task_id]={
"error":"Timeout",
"timestamp":time.time()
}
continue

self.running_tasks[task.task_id]={
"started_at":time.time(),
"status":"running"
}

try:
                    result=task.function(*task.args,**task.kwargs)
self.completed_tasks[task.task_id]={
"result":result,
"completed_at":time.time()
}
logger.info(f"Tarefa {task.task_id} concluda")

exceptExceptionase:
                    self.failed_tasks[task.task_id]={
"error":str(e),
"timestamp":time.time()
}
logger.error(f"Tarefa {task.task_id} falhou: {e}")

finally:
                    iftask.task_idinself.running_tasks:
                        delself.running_tasks[task.task_id]

exceptqueue.Empty:
                continue
exceptExceptionase:
                logger.error(f"Erro no processamento da fila: {e}")

defget_task_status(self,task_id:str)->Dict[str,Any]:
        """Obtm status da tarefa"""
iftask_idinself.completed_tasks:
            return{"status":"completed","data":self.completed_tasks[task_id]}
eliftask_idinself.running_tasks:
            return{"status":"running","data":self.running_tasks[task_id]}
eliftask_idinself.failed_tasks:
            return{"status":"failed","data":self.failed_tasks[task_id]}
else:
            return{"status":"not_found"}

defwait_for_task(self,task_id:str,timeout:Optional[float]=None)->Any:
        """Aguarda concluso da tarefa"""
start_time=time.time()

whileTrue:
            status=self.get_task_status(task_id)

ifstatus["status"]=="completed":
                returnstatus["data"]["result"]
elifstatus["status"]=="failed":
                raiseException(f"Tarefa falhou: {status['data']['error']}")

iftimeoutand(time.time()-start_time)>timeout:
                raiseTimeoutError(f"Timeout aguardando tarefa {task_id}")

time.sleep(0.1)

defget_statistics(self)->Dict[str,Any]:
        """Retorna estatsticas do gerenciador"""
return{
"max_workers":self.max_workers,
"queue_size":self.task_queue.qsize(),
"running_tasks":len(self.running_tasks),
"completed_tasks":len(self.completed_tasks),
"failed_tasks":len(self.failed_tasks)
}

defshutdown(self):
        """Encerra o gerenciador"""
self.executor.shutdown(wait=True)
logger.info("Gerenciador de tarefas encerrado")

classPerformanceMonitor:
    """Monitor de performance do sistema (verso lite)"""

def__init__(self):
        self.metrics_history=[]
self.max_history=1000
self.monitoring=False
self.monitor_thread=None

defstart_monitoring(self,interval:float=1.0):
        """Inicia monitoramento de performance"""
ifself.monitoring:
            return

self.monitoring=True
self.monitor_thread=threading.Thread(
target=self._monitor_loop,
args=(interval,),
daemon=True
)
self.monitor_thread.start()

logger.info(f"Monitoramento de performance iniciado (intervalo: {interval}s)")

defstop_monitoring(self):
        """Para monitoramento de performance"""
self.monitoring=False
ifself.monitor_thread:
            self.monitor_thread.join()
logger.info("Monitoramento de performance parado")

def_monitor_loop(self,interval:float):
        """Loop de monitoramento"""
whileself.monitoring:
            try:
                metrics=self._collect_metrics()
self.metrics_history.append(metrics)

iflen(self.metrics_history)>self.max_history:
                    self.metrics_history=self.metrics_history[-self.max_history:]

exceptExceptionase:
                logger.error(f"Erro no monitoramento: {e}")

time.sleep(interval)

def_collect_metrics(self)->PerformanceMetrics:
        """Coleta mtricas de performance (verso lite)"""

try:

            importresource
memory_usage=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
except:
            memory_usage=0.0

returnPerformanceMetrics(
response_time=0.0,
memory_usage=memory_usage,
cpu_usage=0.0,
cache_hit_rate=0.0,
concurrent_requests=0,
timestamp=time.time()
)

defget_current_metrics(self)->PerformanceMetrics:
        """Obtm mtricas atuais"""
returnself._collect_metrics()

defget_metrics_history(self,duration:Optional[float]=None)->List[PerformanceMetrics]:
        """Obtm histrico de mtricas"""
ifduration:
            cutoff_time=time.time()-duration
return[mforminself.metrics_historyifm.timestamp>=cutoff_time]
returnself.metrics_history.copy()

defget_average_metrics(self,duration:Optional[float]=None)->Dict[str,float]:
        """Obtm mtricas mdias"""
history=self.get_metrics_history(duration)

ifnothistory:
            return{}

return{
"avg_memory_usage":sum(m.memory_usageforminhistory)/len(history),
"avg_cpu_usage":0.0,
"avg_response_time":sum(m.response_timeforminhistory)/len(history),
"avg_cache_hit_rate":sum(m.cache_hit_rateforminhistory)/len(history),
"max_memory_usage":max(m.memory_usageforminhistory),
"max_cpu_usage":0.0,
"max_response_time":max(m.response_timeforminhistory)
}

classPerformanceOptimizer:
    """Otimizador principal de performance (verso lite)"""

def__init__(self):
        self.lazy_loader=LazyLoader()
self.task_manager=AsyncTaskManager()
self.performance_monitor=PerformanceMonitor()

self.function_cache={}

self.max_concurrent_requests=100
self.request_timeout=30.0
self.memory_threshold=80.0
self.cpu_threshold=80.0

self.performance_monitor.start_monitoring()

logger.info("Otimizador de performance (lite) inicializado")

defoptimize_function(self,cache_size:int=128,timeout:Optional[float]=None):
        """Decorator para otimizar funes"""
defdecorator(func):
            @wraps(func)
asyncdefasync_wrapper(*args,**kwargs):
                start_time=time.time()

try:

                    cache_key=f"{func.__name__}_{hash(str(args)+str(kwargs))}"
ifcache_keyinself.function_cache:
                        logger.debug(f"Cache hit para {func.__name__}")
returnself.function_cache[cache_key]

ifasyncio.iscoroutinefunction(func):
                        result=awaitfunc(*args,**kwargs)
else:
                        result=func(*args,**kwargs)

self.function_cache[cache_key]=result

iflen(self.function_cache)>cache_size:

                        oldest_key=next(iter(self.function_cache))
delself.function_cache[oldest_key]

response_time=time.time()-start_time
self._update_metrics(response_time)

returnresult

exceptExceptionase:
                    logger.error(f"Erro na funo {func.__name__}: {e}")
raise

@wraps(func)
defsync_wrapper(*args,**kwargs):
                start_time=time.time()

try:

                    cache_key=f"{func.__name__}_{hash(str(args)+str(kwargs))}"
ifcache_keyinself.function_cache:
                        logger.debug(f"Cache hit para {func.__name__}")
returnself.function_cache[cache_key]

result=func(*args,**kwargs)

self.function_cache[cache_key]=result

iflen(self.function_cache)>cache_size:

                        oldest_key=next(iter(self.function_cache))
delself.function_cache[oldest_key]

response_time=time.time()-start_time
self._update_metrics(response_time)

returnresult

exceptExceptionase:
                    logger.error(f"Erro na funo {func.__name__}: {e}")
raise

returnasync_wrapperifasyncio.iscoroutinefunction(func)elsesync_wrapper

returndecorator

def_update_metrics(self,response_time:float):
        """Atualiza mtricas de performance"""

ifself.performance_monitor.metrics_history:
            latest_metrics=self.performance_monitor.metrics_history[-1]
latest_metrics.response_time=response_time

defsubmit_async_task(self,task_id:str,function:Callable,*args,
priority:int=0,timeout:Optional[float]=None,**kwargs)->str:
        """Submete tarefa assncrona"""
returnself.task_manager.submit_task(
task_id,function,*args,
priority=priority,timeout=timeout,**kwargs
)

defwait_for_async_task(self,task_id:str,timeout:Optional[float]=None)->Any:
        """Aguarda concluso de tarefa assncrona"""
returnself.task_manager.wait_for_task(task_id,timeout)

defload_model_lazy(self,model_name:str,loader_func:Callable,*args,**kwargs):
        """Carrega modelo de forma preguiosa"""
returnself.lazy_loader.load_lazy(model_name,loader_func,*args,**kwargs)

defunload_model(self,model_name:str):
        """Descarrega modelo da memria"""
self.lazy_loader.unload(model_name)

defcheck_system_health(self)->Dict[str,Any]:
        """Verifica sade do sistema (verso lite)"""
current_metrics=self.performance_monitor.get_current_metrics()
avg_metrics=self.performance_monitor.get_average_metrics(duration=300)

health_status={
"status":"healthy",
"issues":[],
"recommendations":[]
}

ifcurrent_metrics.memory_usage>1000:
            health_status["issues"].append("Alto uso de memria")
health_status["recommendations"].append("Considere descarregar modelos no utilizados")

ifavg_metrics.get("avg_response_time",0)>5.0:
            health_status["issues"].append("Tempo de resposta alto")
health_status["recommendations"].append("Otimize consultas e use mais cache")

ifavg_metrics.get("avg_cache_hit_rate",0)<0.5:
            health_status["recommendations"].append("Melhore a estratgia de cache")

ifhealth_status["issues"]:
            health_status["status"]="warning"

iflen(health_status["issues"])>2:
            health_status["status"]="critical"

return{
"health":health_status,
"current_metrics":current_metrics,
"average_metrics":avg_metrics,
"task_manager_stats":self.task_manager.get_statistics(),
"loaded_objects":list(self.lazy_loader.get_loaded_objects().keys())
}

defoptimize_memory(self):
        """Otimiza uso de memria"""
logger.info("Iniciando otimizao de memria...")

collected=gc.collect()
logger.info(f"Garbage collection: {collected} objetos coletados")

loaded_objects=self.lazy_loader.get_loaded_objects()
forobj_nameinlist(loaded_objects.keys()):

            obj_ref=weakref.ref(loaded_objects[obj_name])
ifobj_ref()isNone:
                self.lazy_loader.unload(obj_name)
logger.info(f"Objeto {obj_name} descarregado (no utilizado)")

iflen(self.function_cache)>50:

            cache_items=list(self.function_cache.items())
self.function_cache=dict(cache_items[-25:])
logger.info("Cache de funes otimizado")

logger.info("Otimizao de memria concluda")

defget_performance_report(self)->Dict[str,Any]:
        """Gera relatrio de performance"""
health_check=self.check_system_health()
avg_metrics=self.performance_monitor.get_average_metrics(duration=3600)

return{
"timestamp":time.time(),
"system_health":health_check,
"performance_metrics":avg_metrics,
"optimization_recommendations":self._get_optimization_recommendations(avg_metrics),
"resource_usage":{
"memory_usage_mb":health_check["current_metrics"].memory_usage,
"cpu_usage_percent":0.0,
"loaded_models":len(self.lazy_loader.get_loaded_objects()),
"cached_functions":len(self.function_cache)
}
}

def_get_optimization_recommendations(self,metrics:Dict[str,float])->List[str]:
        """Gera recomendaes de otimizao"""
recommendations=[]

ifmetrics.get("avg_memory_usage",0)>500:
            recommendations.append("Considere usar lazy loading para modelos grandes")

ifmetrics.get("avg_response_time",0)>3.0:
            recommendations.append("Implemente cache mais agressivo para consultas frequentes")

ifmetrics.get("avg_cache_hit_rate",0)<0.6:
            recommendations.append("Ajuste a estratgia de cache para melhor hit rate")

ifnotrecommendations:
            recommendations.append("Sistema est otimizado")

returnrecommendations

defshutdown(self):
        """Encerra otimizador"""
self.performance_monitor.stop_monitoring()
self.task_manager.shutdown()
logger.info("Otimizador de performance encerrado")

performance_optimizer=PerformanceOptimizer()

defoptimize_performance(cache_size:int=128,timeout:Optional[float]=None):
    """Decorator para otimizar performance de funes"""
returnperformance_optimizer.optimize_function(cache_size,timeout)

defasync_task(priority:int=0,timeout:Optional[float]=None):
    """Decorator para executar funo como tarefa assncrona"""
defdecorator(func):
        @wraps(func)
defwrapper(*args,**kwargs):
            task_id=f"{func.__name__}_{int(time.time()*1000)}"
returnperformance_optimizer.submit_async_task(
task_id,func,*args,priority=priority,timeout=timeout,**kwargs
)
returnwrapper
returndecorator

deflazy_load(key:str):
    """Decorator para carregamento preguioso"""
defdecorator(func):
        @wraps(func)
defwrapper(*args,**kwargs):
            returnperformance_optimizer.load_model_lazy(key,func,*args,**kwargs)
returnwrapper
returndecorator
