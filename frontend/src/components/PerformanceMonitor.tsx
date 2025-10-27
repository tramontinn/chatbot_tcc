import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Activity, Cpu, HardDrive, Zap, TrendingUp, TrendingDown,
  AlertTriangle, CheckCircle, RefreshCw, Settings, BarChart3,
  Clock, MemoryStick, Gauge, Target, Lightbulb
} from 'lucide-react';

interface PerformanceMetrics {
  response_time: number;
  memory_usage: number;
  cpu_usage: number;
  cache_hit_rate: number;
  concurrent_requests: number;
  timestamp: number;
}

interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  issues: string[];
  recommendations: string[];
}

interface PerformanceReport {
  timestamp: number;
  system_health: {
    health: SystemHealth;
    current_metrics: PerformanceMetrics;
    average_metrics: {
      avg_memory_usage: number;
      avg_cpu_usage: number;
      avg_response_time: number;
      avg_cache_hit_rate: number;
      max_memory_usage: number;
      max_cpu_usage: number;
      max_response_time: number;
    };
    task_manager_stats: {
      max_workers: number;
      queue_size: number;
      running_tasks: number;
      completed_tasks: number;
      failed_tasks: number;
    };
    loaded_objects: string[];
  };
  performance_metrics: any;
  optimization_recommendations: string[];
  resource_usage: {
    memory_usage_mb: number;
    cpu_usage_percent: number;
    loaded_models: number;
    cached_functions: number;
  };
}

const PerformanceMonitor: React.FC = () => {
  const [report, setReport] = useState<PerformanceReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(5); // segundos
  const [activeTab, setActiveTab] = useState<'overview' | 'metrics' | 'health' | 'optimization'>('overview');
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchPerformanceReport();
  }, []);

  useEffect(() => {
    if (autoRefresh) {
      intervalRef.current = setInterval(() => {
        fetchPerformanceReport();
      }, refreshInterval * 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [autoRefresh, refreshInterval]);

  const fetchPerformanceReport = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/performance/report');
      setReport(response.data);
    } catch (error) {
      console.error('Erro ao buscar relatório de performance:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'critical':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5" />;
      case 'critical':
        return <AlertTriangle className="h-5 w-5" />;
      default:
        return <Activity className="h-5 w-5" />;
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  const formatTime = (seconds: number) => {
    if (seconds < 1) {
      return `${(seconds * 1000).toFixed(0)}ms`;
    }
    return `${seconds.toFixed(2)}s`;
  };

  if (loading && !report) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2 text-gray-600">Carregando relatório de performance...</span>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="text-center p-8">
        <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
        <p className="text-gray-600">Não foi possível carregar o relatório de performance.</p>
        <button
          onClick={fetchPerformanceReport}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  const { system_health, performance_metrics, optimization_recommendations, resource_usage } = report;

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="border-b border-gray-200 p-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold text-gray-900">Monitor de Performance</h1>
            <div className="flex items-center space-x-4">
              {/* Auto Refresh Toggle */}
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-600">Auto Refresh:</label>
                <button
                  onClick={() => setAutoRefresh(!autoRefresh)}
                  className={`px-3 py-1 rounded-md text-sm ${
                    autoRefresh 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {autoRefresh ? 'ON' : 'OFF'}
                </button>
              </div>
              
              {/* Refresh Interval */}
              <div className="flex items-center space-x-2">
                <label className="text-sm text-gray-600">Intervalo:</label>
                <select
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(Number(e.target.value))}
                  className="px-2 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value={5}>5s</option>
                  <option value={10}>10s</option>
                  <option value={30}>30s</option>
                  <option value={60}>1m</option>
                </select>
              </div>
              
              <button
                onClick={fetchPerformanceReport}
                disabled={loading}
                className="bg-blue-100 text-blue-700 px-4 py-2 rounded-md hover:bg-blue-200 disabled:opacity-50 flex items-center"
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Atualizar
              </button>
            </div>
          </div>

          {/* Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className={`p-4 rounded-lg ${getStatusColor(system_health.health.status)}`}>
              <div className="flex items-center">
                {getStatusIcon(system_health.health.status)}
                <div className="ml-3">
                  <p className="text-sm font-medium">Status do Sistema</p>
                  <p className="text-lg font-bold capitalize">
                    {system_health.health.status}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center">
                <MemoryStick className="h-8 w-8 text-blue-500 mr-3" />
                <div>
                  <p className="text-sm text-blue-600">Uso de Memória</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {formatBytes(system_health.current_metrics.memory_usage * 1024 * 1024)}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Cpu className="h-8 w-8 text-green-500 mr-3" />
                <div>
                  <p className="text-sm text-green-600">Uso de CPU</p>
                  <p className="text-2xl font-bold text-green-900">
                    {formatPercentage(system_health.current_metrics.cpu_usage)}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Clock className="h-8 w-8 text-purple-500 mr-3" />
                <div>
                  <p className="text-sm text-purple-600">Tempo de Resposta</p>
                  <p className="text-2xl font-bold text-purple-900">
                    {formatTime(system_health.current_metrics.response_time)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6 py-4">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'overview'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Visão Geral
            </button>
            <button
              onClick={() => setActiveTab('metrics')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'metrics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Métricas
            </button>
            <button
              onClick={() => setActiveTab('health')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'health'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Saúde do Sistema
            </button>
            <button
              onClick={() => setActiveTab('optimization')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'optimization'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Otimização
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Resumo de Performance</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Recursos do Sistema</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Modelos Carregados</span>
                      <span className="text-sm font-medium text-gray-900">
                        {resource_usage.loaded_models}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Funções em Cache</span>
                      <span className="text-sm font-medium text-gray-900">
                        {resource_usage.cached_functions}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Tarefas Concorrentes</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.current_metrics.concurrent_requests}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Taxa de Cache Hit</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatPercentage(system_health.current_metrics.cache_hit_rate * 100)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Gerenciador de Tarefas</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Workers Máximos</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.task_manager_stats.max_workers}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Fila de Tarefas</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.task_manager_stats.queue_size}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Tarefas Executando</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.task_manager_stats.running_tasks}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Tarefas Concluídas</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.task_manager_stats.completed_tasks}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'metrics' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Métricas Detalhadas</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Métricas Atuais</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Tempo de Resposta</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatTime(system_health.current_metrics.response_time)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Uso de Memória</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatBytes(system_health.current_metrics.memory_usage * 1024 * 1024)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Uso de CPU</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatPercentage(system_health.current_metrics.cpu_usage)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Taxa de Cache Hit</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatPercentage(system_health.current_metrics.cache_hit_rate * 100)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Métricas Médias (1h)</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Tempo de Resposta Médio</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatTime(system_health.average_metrics.avg_response_time)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Uso de Memória Médio</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatBytes(system_health.average_metrics.avg_memory_usage * 1024 * 1024)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Uso de CPU Médio</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatPercentage(system_health.average_metrics.avg_cpu_usage)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Taxa de Cache Hit Média</span>
                      <span className="text-sm font-medium text-gray-900">
                        {formatPercentage(system_health.average_metrics.avg_cache_hit_rate * 100)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="text-md font-medium text-gray-900 mb-4">Picos de Uso</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Pico de Memória</p>
                    <p className="text-lg font-bold text-red-600">
                      {formatBytes(system_health.average_metrics.max_memory_usage * 1024 * 1024)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Pico de CPU</p>
                    <p className="text-lg font-bold text-red-600">
                      {formatPercentage(system_health.average_metrics.max_cpu_usage)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Pico de Tempo de Resposta</p>
                    <p className="text-lg font-bold text-red-600">
                      {formatTime(system_health.average_metrics.max_response_time)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'health' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Saúde do Sistema</h3>
              
              <div className={`p-6 rounded-lg ${getStatusColor(system_health.health.status)}`}>
                <div className="flex items-center mb-4">
                  {getStatusIcon(system_health.health.status)}
                  <h4 className="text-lg font-medium ml-2 capitalize">
                    Status: {system_health.health.status}
                  </h4>
                </div>
                
                {system_health.health.issues.length > 0 && (
                  <div className="mb-4">
                    <h5 className="text-md font-medium mb-2">Problemas Identificados:</h5>
                    <ul className="list-disc list-inside space-y-1">
                      {system_health.health.issues.map((issue, index) => (
                        <li key={index} className="text-sm">{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {system_health.health.recommendations.length > 0 && (
                  <div>
                    <h5 className="text-md font-medium mb-2">Recomendações:</h5>
                    <ul className="list-disc list-inside space-y-1">
                      {system_health.health.recommendations.map((recommendation, index) => (
                        <li key={index} className="text-sm">{recommendation}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="text-md font-medium text-gray-900 mb-4">Objetos Carregados</h4>
                {system_health.loaded_objects.length > 0 ? (
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                    {system_health.loaded_objects.map((obj, index) => (
                      <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                        {obj}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Nenhum objeto carregado</p>
                )}
              </div>
            </div>
          )}

          {activeTab === 'optimization' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Recomendações de Otimização</h3>
              
              <div className="bg-gray-50 p-6 rounded-lg">
                <h4 className="text-md font-medium text-gray-900 mb-4">Sugestões de Melhoria</h4>
                {optimization_recommendations.length > 0 ? (
                  <div className="space-y-3">
                    {optimization_recommendations.map((recommendation, index) => (
                      <div key={index} className="flex items-start space-x-3">
                        <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5 flex-shrink-0" />
                        <p className="text-sm text-gray-700">{recommendation}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Sistema está otimizado</p>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-blue-900 mb-4">Ações de Otimização</h4>
                  <div className="space-y-3">
                    <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm">
                      Otimizar Memória
                    </button>
                    <button className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 text-sm">
                      Limpar Cache
                    </button>
                    <button className="w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 text-sm">
                      Reorganizar Tarefas
                    </button>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Configurações de Performance</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Workers Máximos</span>
                      <span className="text-sm font-medium text-gray-900">
                        {system_health.task_manager_stats.max_workers}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Timeout de Tarefas</span>
                      <span className="text-sm font-medium text-gray-900">30s</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Limite de Memória</span>
                      <span className="text-sm font-medium text-gray-900">1GB</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Limite de CPU</span>
                      <span className="text-sm font-medium text-gray-900">80%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PerformanceMonitor;


