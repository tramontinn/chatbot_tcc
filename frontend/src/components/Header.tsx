import React from 'react';
import { Bot, FileText } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-primary-500 rounded-lg">
              <Bot className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Chatbot IA
              </h1>
              <p className="text-sm text-gray-600">
                Documentos Internos
              </p>
            </div>
          </div>
          
          <div className="ml-auto flex items-center space-x-2 text-sm text-gray-500">
            <FileText className="h-4 w-4" />
            <span>Sistema de IA para Documentos</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
