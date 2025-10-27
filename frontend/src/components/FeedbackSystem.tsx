import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  ThumbsUp, ThumbsDown, Star, MessageSquare, TrendingUp, 
  BarChart3, Target, Lightbulb, CheckCircle, AlertTriangle,
  RefreshCw, Download, Filter, Search
} from 'lucide-react';

interface FeedbackData {
  id: string;
  session_id: string;
  question: string;
  original_response: string;
  satisfaction: number;
  feedback_text?: string;
  timestamp: number;
  category?: string;
  improved_response?: string;
  improvement_applied: boolean;
}

interface LearningInsights {
  feedback_stats: {
    total_feedback: number;
    average_satisfaction: number;
    positive_feedback: number;
    negative_feedback: number;
    positive_rate: number;
  };
  successful_patterns: Array<{
    pattern: string;
    success_rate: number;
    usage_count: number;
    category: string;
  }>;
  improvement_areas: { [key: string]: number };
  low_satisfaction_categories: Array<{
    category: string;
    count: number;
    avg_satisfaction: number;
  }>;
  total_patterns: number;
  total_suggestions: number;
  learning_rate: number;
}

interface FeedbackFormProps {
  sessionId: string;
  question: string;
  response: string;
  onFeedbackSubmitted: () => void;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ 
  sessionId, question, response, onFeedbackSubmitted 
}) => {
  const [satisfaction, setSatisfaction] = useState<number>(0);
  const [feedbackText, setFeedbackText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (satisfaction === 0) return;

    setIsSubmitting(true);
    try {
      await axios.post('/feedback', {
        session_id: sessionId,
        question: question,
        response: response,
        satisfaction: satisfaction,
        feedback_text: feedbackText || null
      });

      setSubmitted(true);
      onFeedbackSubmitted();
      
      // Reset form after 3 seconds
      setTimeout(() => {
        setSatisfaction(0);
        setFeedbackText('');
        setSubmitted(false);
      }, 3000);

    } catch (error) {
      console.error('Erro ao enviar feedback:', error);
      alert('Erro ao enviar feedback');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
          <span className="text-green-700 font-medium">Feedback enviado com sucesso!</span>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <h4 className="text-sm font-medium text-gray-900 mb-3">
        Como você avalia esta resposta?
      </h4>
      
      {/* Rating Stars */}
      <div className="flex items-center space-x-1 mb-4">
        {[1, 2, 3, 4, 5].map((rating) => (
          <button
            key={rating}
            type="button"
            onClick={() => setSatisfaction(rating)}
            className={`p-1 ${
              rating <= satisfaction
                ? 'text-yellow-400 hover:text-yellow-500'
                : 'text-gray-300 hover:text-gray-400'
            }`}
          >
            <Star className="h-6 w-6 fill-current" />
          </button>
        ))}
        <span className="ml-2 text-sm text-gray-600">
          {satisfaction > 0 && (
            satisfaction === 1 ? 'Muito insatisfeito' :
            satisfaction === 2 ? 'Insatisfeito' :
            satisfaction === 3 ? 'Neutro' :
            satisfaction === 4 ? 'Satisfeito' :
            'Muito satisfeito'
          )}
        </span>
      </div>

      {/* Feedback Text */}
      <div className="mb-4">
        <label htmlFor="feedback-text" className="block text-sm font-medium text-gray-700 mb-2">
          Comentários (opcional)
        </label>
        <textarea
          id="feedback-text"
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
          placeholder="Conte-nos como podemos melhorar..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          rows={3}
        />
      </div>

      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={satisfaction === 0 || isSubmitting}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {isSubmitting ? (
            <>
              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              Enviando...
            </>
          ) : (
            'Enviar Feedback'
          )}
        </button>
      </div>
    </form>
  );
};

const FeedbackSystem: React.FC = () => {
  const [insights, setInsights] = useState<LearningInsights | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'patterns' | 'improvements' | 'analytics'>('overview');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/learning/insights');
      setInsights(response.data);
    } catch (error) {
      console.error('Erro ao buscar insights:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportData = async () => {
    try {
      const response = await axios.get('/learning/export', {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `learning_data_${new Date().toISOString().split('T')[0]}.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Erro ao exportar dados:', error);
      alert('Erro ao exportar dados');
    }
  };

  const getSatisfactionColor = (rating: number) => {
    if (rating >= 4) return 'text-green-600 bg-green-100';
    if (rating >= 3) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getSatisfactionIcon = (rating: number) => {
    if (rating >= 4) return <ThumbsUp className="h-4 w-4" />;
    if (rating >= 3) return <MessageSquare className="h-4 w-4" />;
    return <ThumbsDown className="h-4 w-4" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2 text-gray-600">Carregando insights...</span>
      </div>
    );
  }

  if (!insights) {
    return (
      <div className="text-center p-8">
        <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
        <p className="text-gray-600">Não foi possível carregar os insights de aprendizado.</p>
        <button
          onClick={fetchInsights}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="border-b border-gray-200 p-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold text-gray-900">Sistema de Feedback Adaptativo</h1>
            <div className="flex space-x-2">
              <button
                onClick={fetchInsights}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 flex items-center"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Atualizar
              </button>
              <button
                onClick={exportData}
                className="bg-green-100 text-green-700 px-4 py-2 rounded-md hover:bg-green-200 flex items-center"
              >
                <Download className="h-4 w-4 mr-2" />
                Exportar
              </button>
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-blue-500 mr-3" />
                <div>
                  <p className="text-sm text-blue-600">Total de Feedback</p>
                  <p className="text-2xl font-bold text-blue-900">
                    {insights.feedback_stats.total_feedback}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-green-500 mr-3" />
                <div>
                  <p className="text-sm text-green-600">Satisfação Média</p>
                  <p className="text-2xl font-bold text-green-900">
                    {insights.feedback_stats.average_satisfaction.toFixed(1)}/5
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Target className="h-8 w-8 text-purple-500 mr-3" />
                <div>
                  <p className="text-sm text-purple-600">Padrões Aprendidos</p>
                  <p className="text-2xl font-bold text-purple-900">
                    {insights.total_patterns}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="flex items-center">
                <Lightbulb className="h-8 w-8 text-orange-500 mr-3" />
                <div>
                  <p className="text-sm text-orange-600">Sugestões de Melhoria</p>
                  <p className="text-2xl font-bold text-orange-900">
                    {insights.total_suggestions}
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
              onClick={() => setActiveTab('patterns')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'patterns'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Padrões de Sucesso
            </button>
            <button
              onClick={() => setActiveTab('improvements')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'improvements'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Melhorias
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'analytics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Análises
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Resumo do Sistema de Aprendizado</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Distribuição de Feedback</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Feedback Positivo (4-5 estrelas)</span>
                      <span className="text-sm font-medium text-green-600">
                        {insights.feedback_stats.positive_feedback} ({insights.feedback_stats.positive_rate}%)
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Feedback Negativo (1-2 estrelas)</span>
                      <span className="text-sm font-medium text-red-600">
                        {insights.feedback_stats.negative_feedback}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${insights.feedback_stats.positive_rate}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Taxa de Aprendizado</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Taxa de Aprendizado Atual</span>
                      <span className="text-sm font-medium text-blue-600">
                        {(insights.learning_rate * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Padrões Identificados</span>
                      <span className="text-sm font-medium text-purple-600">
                        {insights.total_patterns}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Sugestões Geradas</span>
                      <span className="text-sm font-medium text-orange-600">
                        {insights.total_suggestions}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'patterns' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Padrões de Resposta Bem-Sucedidos</h3>
                <div className="flex space-x-2">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <input
                      type="text"
                      placeholder="Buscar padrões..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    />
                  </div>
                  <select
                    value={filterCategory}
                    onChange={(e) => setFilterCategory(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 text-sm"
                  >
                    <option value="all">Todas as Categorias</option>
                    <option value="horario">Horário</option>
                    <option value="beneficios">Benefícios</option>
                    <option value="ferias">Férias</option>
                    <option value="licenca">Licença</option>
                    <option value="vestimenta">Vestimenta</option>
                    <option value="comunicacao">Comunicação</option>
                    <option value="seguranca">Segurança</option>
                    <option value="limpeza">Limpeza</option>
                    <option value="treinamento">Treinamento</option>
                    <option value="rh">RH</option>
                  </select>
                </div>
              </div>

              {insights.successful_patterns.length === 0 ? (
                <div className="text-center py-12">
                  <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Nenhum padrão de sucesso identificado ainda.</p>
                  <p className="text-sm text-gray-400 mt-2">
                    Continue coletando feedback para identificar padrões.
                  </p>
                </div>
              ) : (
                <div className="grid gap-4">
                  {insights.successful_patterns
                    .filter(pattern => 
                      (filterCategory === 'all' || pattern.category === filterCategory) &&
                      (searchTerm === '' || pattern.pattern.toLowerCase().includes(searchTerm.toLowerCase()))
                    )
                    .map((pattern, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-medium text-gray-900 capitalize">
                            {pattern.pattern.replace(/_/g, ' ')}
                          </h4>
                          <p className="text-sm text-gray-500 capitalize">
                            Categoria: {pattern.category}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            pattern.success_rate >= 0.8 ? 'bg-green-100 text-green-800' :
                            pattern.success_rate >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {(pattern.success_rate * 100).toFixed(0)}% sucesso
                          </span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center text-sm text-gray-600">
                        <span>Usado {pattern.usage_count} vezes</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${pattern.success_rate * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'improvements' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Áreas de Melhoria Identificadas</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Tipos de Melhoria</h4>
                  {Object.keys(insights.improvement_areas).length > 0 ? (
                    <div className="space-y-3">
                      {Object.entries(insights.improvement_areas).map(([type, count]) => (
                        <div key={type} className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 capitalize">
                            {type === 'clarity' ? 'Clareza' :
                             type === 'completeness' ? 'Completude' :
                             type === 'tone' ? 'Tom' :
                             type === 'accuracy' ? 'Precisão' : type}
                          </span>
                          <span className="text-sm font-medium text-gray-900">{count}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Nenhuma área de melhoria identificada ainda.</p>
                  )}
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Categorias com Baixa Satisfação</h4>
                  {insights.low_satisfaction_categories.length > 0 ? (
                    <div className="space-y-3">
                      {insights.low_satisfaction_categories.map((category, index) => (
                        <div key={index} className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 capitalize">{category.category}</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-medium text-gray-900">
                              {category.avg_satisfaction.toFixed(1)}/5
                            </span>
                            <span className="text-xs text-gray-500">({category.count} feedbacks)</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Todas as categorias têm boa satisfação.</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Análises Detalhadas</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-blue-900 mb-4">Eficiência do Sistema</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-blue-700">Taxa de Aprendizado</span>
                      <span className="text-sm font-medium text-blue-900">
                        {(insights.learning_rate * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-blue-700">Padrões Ativos</span>
                      <span className="text-sm font-medium text-blue-900">
                        {insights.total_patterns}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-blue-700">Sugestões Geradas</span>
                      <span className="text-sm font-medium text-blue-900">
                        {insights.total_suggestions}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-green-900 mb-4">Qualidade das Respostas</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-green-700">Satisfação Média</span>
                      <span className="text-sm font-medium text-green-900">
                        {insights.feedback_stats.average_satisfaction.toFixed(1)}/5
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-green-700">Taxa de Aprovação</span>
                      <span className="text-sm font-medium text-green-900">
                        {insights.feedback_stats.positive_rate.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-green-700">Total de Avaliações</span>
                      <span className="text-sm font-medium text-green-900">
                        {insights.feedback_stats.total_feedback}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-purple-900 mb-4">Recomendações</h4>
                  <div className="space-y-2 text-sm text-purple-700">
                    {insights.feedback_stats.positive_rate >= 80 ? (
                      <p>✅ Sistema funcionando bem!</p>
                    ) : insights.feedback_stats.positive_rate >= 60 ? (
                      <p>⚠️ Há espaço para melhorias</p>
                    ) : (
                      <p>🔴 Necessário revisar respostas</p>
                    )}
                    
                    {insights.total_patterns < 5 && (
                      <p>📈 Coletar mais feedback para identificar padrões</p>
                    )}
                    
                    {insights.low_satisfaction_categories.length > 0 && (
                      <p>🎯 Focar nas categorias com baixa satisfação</p>
                    )}
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

export { FeedbackForm, FeedbackSystem };


