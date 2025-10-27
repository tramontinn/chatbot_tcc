import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Trash2, ThumbsUp, ThumbsDown, MessageCircle } from 'lucide-react';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  sources?: string[];
  feedback?: {
    satisfaction: number;
    submitted: boolean;
  };
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/chat', {
        message: inputMessage,
        session_id: sessionId,
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        isUser: false,
        timestamp: response.data.timestamp,
        sources: response.data.sources,
      };

      setMessages(prev => [...prev, botMessage]);
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.',
        isUser: false,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  const submitFeedback = async (messageId: string, satisfaction: number) => {
    try {
      const message = messages.find(m => m.id === messageId);
      if (!message || !sessionId) return;

      // Encontrar a pergunta correspondente
      const messageIndex = messages.findIndex(m => m.id === messageId);
      const userMessage = messages[messageIndex - 1];

      await axios.post('/feedback', {
        session_id: sessionId,
        question: userMessage?.text || '',
        response: message.text,
        satisfaction: satisfaction,
      });

      // Atualizar o estado da mensagem
      setMessages(prev => prev.map(m => 
        m.id === messageId 
          ? { ...m, feedback: { satisfaction, submitted: true } }
          : m
      ));
    } catch (error) {
      console.error('Erro ao enviar feedback:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <Bot className="h-5 w-5 text-primary-500" />
            <h2 className="text-lg font-semibold text-gray-900">
              Chat com IA
            </h2>
          </div>
          <button
            onClick={clearChat}
            className="flex items-center space-x-1 text-gray-500 hover:text-red-500 transition-colors"
          >
            <Trash2 className="h-4 w-4" />
            <span className="text-sm">Limpar</span>
          </button>
        </div>

        {/* Messages */}
        <div className="h-96 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Bot className="h-12 w-12 mx-auto mb-4 text-primary-500" />
              <p className="text-lg font-medium mb-2 text-gray-900">
                👋 Olá! Sou seu assistente virtual
              </p>
              <p className="text-sm mb-4">
                Estou aqui para ajudá-lo com informações sobre a empresa, políticas, benefícios e muito mais!
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md mx-auto">
                <p className="text-xs text-blue-800 mb-2 font-medium">
                  💡 Dicas para melhores respostas:
                </p>
                <ul className="text-xs text-blue-700 text-left space-y-1">
                  <li>• Seja específico em suas perguntas</li>
                  <li>• Use palavras-chave relacionadas ao assunto</li>
                  <li>• Avalie minhas respostas para eu melhorar</li>
                </ul>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-2xl px-4 py-3 rounded-lg ${
                    message.isUser
                      ? 'bg-primary-500 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <div className="flex items-start space-x-2">
                    {!message.isUser && (
                      <Bot className="h-4 w-4 mt-1 text-primary-500 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <div className="prose prose-sm max-w-none">
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {message.text}
                        </div>
                      </div>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-2 border-t border-gray-200">
                          <p className="text-xs text-gray-500 mb-2 flex items-center">
                            <MessageCircle className="h-3 w-3 mr-1" />
                            Fontes:
                          </p>
                          <div className="flex flex-wrap gap-1">
                            {message.sources.map((source, index) => (
                              <span
                                key={index}
                                className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full"
                              >
                                {source}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                      {!message.isUser && !message.feedback?.submitted && (
                        <div className="mt-3 pt-2 border-t border-gray-200">
                          <p className="text-xs text-gray-500 mb-2">Esta resposta foi útil?</p>
                          <div className="flex space-x-2">
                            <button
                              onClick={() => submitFeedback(message.id, 5)}
                              className="flex items-center space-x-1 text-xs text-green-600 hover:text-green-700 transition-colors"
                            >
                              <ThumbsUp className="h-3 w-3" />
                              <span>Sim</span>
                            </button>
                            <button
                              onClick={() => submitFeedback(message.id, 1)}
                              className="flex items-center space-x-1 text-xs text-red-600 hover:text-red-700 transition-colors"
                            >
                              <ThumbsDown className="h-3 w-3" />
                              <span>Não</span>
                            </button>
                          </div>
                        </div>
                      )}
                      {!message.isUser && message.feedback?.submitted && (
                        <div className="mt-2 pt-2 border-t border-gray-200">
                          <p className="text-xs text-green-600 flex items-center">
                            {message.feedback.satisfaction >= 4 ? (
                              <>
                                <ThumbsUp className="h-3 w-3 mr-1" />
                                Obrigado pelo feedback!
                              </>
                            ) : (
                              <>
                                <ThumbsDown className="h-3 w-3 mr-1" />
                                Vou melhorar nas próximas respostas!
                              </>
                            )}
                          </p>
                        </div>
                      )}
                    </div>
                    {message.isUser && (
                      <User className="h-4 w-4 mt-1 text-white flex-shrink-0" />
                    )}
                  </div>
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Bot className="h-4 w-4 text-primary-500" />
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse-slow"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse-slow" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse-slow" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200">
          <div className="flex space-x-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Digite sua pergunta..."
              className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={1}
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
