import React, { useState, useEffect } from 'react';
import { Upload, FileText, Trash2, Download, AlertCircle } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface Document {
  filename: string;
  content_type: string;
  size: number;
  processed: boolean;
  timestamp?: string;
  id?: string;
}

const DocumentManager: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await axios.get('/documents');
      setDocuments(response.data);
    } catch (error) {
      console.error('Erro ao carregar documentos:', error);
      setError('Erro ao carregar documentos');
    }
  };

  const onDrop = async (acceptedFiles: File[]) => {
    setIsLoading(true);
    setError(null);

    for (const file of acceptedFiles) {
      try {
        setUploadProgress(prev => ({ ...prev, [file.name]: 0 }));

        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post('/upload-document', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total
              ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
              : 0;
            setUploadProgress(prev => ({ ...prev, [file.name]: progress }));
          },
        });

        // Atualizar lista de documentos
        await loadDocuments();
        
        // Remover progresso
        setUploadProgress(prev => {
          const newProgress = { ...prev };
          delete newProgress[file.name];
          return newProgress;
        });

      } catch (error) {
        console.error(`Erro ao fazer upload de ${file.name}:`, error);
        setError(`Erro ao fazer upload de ${file.name}`);
        
        // Remover progresso
        setUploadProgress(prev => {
          const newProgress = { ...prev };
          delete newProgress[file.name];
          return newProgress;
        });
      }
    }

    setIsLoading(false);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    multiple: true,
  });

  const deleteDocument = async (filename: string) => {
    try {
      await axios.delete(`/documents/${encodeURIComponent(filename)}`);
      await loadDocuments();
    } catch (error) {
      console.error('Erro ao deletar documento:', error);
      setError('Erro ao deletar documento');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (contentType: string) => {
    switch (contentType) {
      case 'application/pdf':
        return '📄';
      case 'text/plain':
        return '📝';
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return '📘';
      default:
        return '📄';
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Upload de Documentos
        </h2>
        
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            {isDragActive ? 'Solte os arquivos aqui' : 'Arraste arquivos aqui ou clique para selecionar'}
          </p>
          <p className="text-sm text-gray-500">
            Suporta PDF, TXT e DOCX (máximo 10MB por arquivo)
          </p>
        </div>

        {/* Upload Progress */}
        {Object.keys(uploadProgress).length > 0 && (
          <div className="mt-4 space-y-2">
            {Object.entries(uploadProgress).map(([filename, progress]) => (
              <div key={filename} className="flex items-center space-x-2">
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <span className="text-sm text-gray-600 min-w-0 truncate">
                  {filename}
                </span>
                <span className="text-sm text-gray-500">
                  {progress}%
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-4 flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Documentos Processados ({documents.length})
          </h2>
        </div>

        <div className="divide-y divide-gray-200">
          {documents.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p className="text-lg font-medium mb-2">
                Nenhum documento processado
              </p>
              <p className="text-sm">
                Faça upload de documentos para começar a usar o chatbot.
              </p>
            </div>
          ) : (
            documents.map((doc) => (
              <div key={doc.filename} className="p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{getFileIcon(doc.content_type)}</span>
                    <div>
                      <h3 className="font-medium text-gray-900 truncate max-w-xs">
                        {doc.filename}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {formatFileSize(doc.size)} • {doc.content_type}
                      </p>
                      {doc.timestamp && (
                        <p className="text-xs text-gray-400">
                          Processado em {new Date(doc.timestamp).toLocaleString('pt-BR')}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      doc.processed
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {doc.processed ? 'Processado' : 'Processando...'}
                    </span>
                    
                    <button
                      onClick={() => deleteDocument(doc.filename)}
                      className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                      title="Deletar documento"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentManager;
