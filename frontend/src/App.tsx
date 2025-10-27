import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import DocumentManager from './components/DocumentManager';
import Header from './components/Header';

type TabType = 'chat' | 'documents';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('chat');

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex space-x-1 bg-white rounded-lg p-1 mb-8 shadow-sm">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 py-3 px-4 rounded-md font-medium transition-colors ${
              activeTab === 'chat'
                ? 'bg-primary-500 text-white shadow-sm'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setActiveTab('documents')}
            className={`flex-1 py-3 px-4 rounded-md font-medium transition-colors ${
              activeTab === 'documents'
                ? 'bg-primary-500 text-white shadow-sm'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }`}
          >
            📄 Documentos
          </button>
        </div>

        {/* Content */}
        <div className="animate-fade-in">               
          {activeTab === 'chat' ? (
            <ChatInterface />
          ) : (
            <DocumentManager />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
