import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { 
  Upload, File, Trash2, Eye, Download, X, CheckCircle, AlertCircle, 
  FileText, Image, FileSpreadsheet, FileImage, FileVideo, FileAudio,
  Plus, Minus, Search, Filter, SortAsc, SortDesc
} from 'lucide-react';
import { useDropzone } from 'react-dropzone';

interface Document {
  filename: string;
  content_type: string;
  size: number;
  processed: boolean;
  timestamp?: string;
  id?: string;
  category?: string;
}

interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
  error?: string;
}

interface DocumentStats {
  total: number;
  processed: number;
  pending: number;
  totalSize: number;
  categories: { [key: string]: number };
}

const EnhancedDocumentManager: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [internalDocuments, setInternalDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<UploadProgress[]>([]);
  const [activeTab, setActiveTab] = useState<'upload' | 'documents' | 'internal' | 'stats'>('upload');
  const [previewFile, setPreviewFile] = useState<File | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'size' | 'date'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [filterBy, setFilterBy] = useState<'all' | 'processed' | 'pending'>('all');
  const [stats, setStats] = useState<DocumentStats>({
    total: 0,
    processed: 0,
    pending: 0,
    totalSize: 0,
    categories: {}
  });

  useEffect(() => {
    fetchDocuments();
    fetchInternalDocuments();
    fetchStats();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/documents');
      setDocuments(response.data);
    } catch (error) {
      console.error('Erro ao buscar documentos:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchInternalDocuments = async () => {
    try {
      const response = await axios.get('/internal-documents');
      setInternalDocuments(response.data.documents || []);
    } catch (error) {
      console.error('Erro ao buscar documentos internos:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('/internal-documents/statistics');
      const data = response.data;
      setStats({
        total: data.internal_documents?.total_documents || 0,
        processed: data.internal_documents?.processed_documents || 0,
        pending: (data.internal_documents?.total_documents || 0) - (data.internal_documents?.processed_documents || 0),
        totalSize: data.internal_documents?.total_size || 0,
        categories: data.internal_documents?.categories || {}
      });
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const validFiles = acceptedFiles.filter(file => {
      const validTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'text/markdown',
        'application/rtf',
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      ];
      const maxSize = 10 * 1024 * 1024; // 10MB
      
      if (!validTypes.includes(file.type)) {
        alert(`Tipo de arquivo não suportado: ${file.name}`);
        return false;
      }
      
      if (file.size > maxSize) {
        alert(`Arquivo muito grande: ${file.name} (máx. 10MB)`);
        return false;
      }
      
      return true;
    });

    setSelectedFiles(prev => [...prev, ...validFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md'],
      'application/rtf': ['.rtf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/gif': ['.gif'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    multiple: true,
    noClick: selectedFiles.length > 0
  });

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async (isInternal: boolean = false) => {
    if (selectedFiles.length === 0) return;

    setUploading(true);
    const progressList: UploadProgress[] = selectedFiles.map(file => ({
      file,
      progress: 0,
      status: 'uploading'
    }));
    setUploadProgress(progressList);

    try {
      const uploadPromises = selectedFiles.map(async (file, index) => {
        try {
          const formData = new FormData();
          formData.append('file', file);

          const endpoint = isInternal ? '/internal-documents/add' : '/upload-document';
          
          const response = await axios.post(endpoint, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
              const progress = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
              setUploadProgress(prev => prev.map((item, i) => 
                i === index ? { ...item, progress, status: 'processing' } : item
              ));
            },
          });

          setUploadProgress(prev => prev.map((item, i) => 
            i === index ? { ...item, progress: 100, status: 'completed' } : item
          ));

          return response.data;
        } catch (error) {
          setUploadProgress(prev => prev.map((item, i) => 
            i === index ? { 
              ...item, 
              status: 'error', 
              error: error instanceof Error ? error.message : 'Erro desconhecido' 
            } : item
          ));
          throw error;
        }
      });

      await Promise.all(uploadPromises);
      
      setSelectedFiles([]);
      fetchDocuments();
      fetchInternalDocuments();
      fetchStats();
      
      // Limpar progresso após 3 segundos
      setTimeout(() => {
        setUploadProgress([]);
      }, 3000);
      
    } catch (error) {
      console.error('Erro no upload:', error);
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (filename: string) => {
    if (!confirm('Tem certeza que deseja remover este documento?')) return;

    try {
      await axios.delete(`/documents/${filename}`);
      fetchDocuments();
    } catch (error) {
      console.error('Erro ao remover documento:', error);
      alert('Erro ao remover documento');
    }
  };

  const handleDeleteInternalDocument = async (filename: string) => {
    if (!confirm('Tem certeza que deseja remover este documento interno?')) return;

    try {
      await axios.delete(`/internal-documents/${filename}`);
      fetchInternalDocuments();
      fetchStats();
    } catch (error) {
      console.error('Erro ao remover documento interno:', error);
      alert('Erro ao remover documento interno');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (contentType: string, filename: string) => {
    if (contentType.includes('pdf')) return <FileText className="h-8 w-8 text-red-500" />;
    if (contentType.includes('word')) return <FileText className="h-8 w-8 text-blue-500" />;
    if (contentType.includes('text')) return <FileText className="h-8 w-8 text-gray-500" />;
    if (contentType.includes('image')) return <Image className="h-8 w-8 text-green-500" />;
    if (contentType.includes('spreadsheet') || contentType.includes('excel')) return <FileSpreadsheet className="h-8 w-8 text-green-600" />;
    if (contentType.includes('video')) return <FileVideo className="h-8 w-8 text-purple-500" />;
    if (contentType.includes('audio')) return <FileAudio className="h-8 w-8 text-orange-500" />;
    return <File className="h-8 w-8 text-gray-400" />;
  };

  const getFilePreview = (file: File) => {
    if (file.type.startsWith('image/')) {
      return (
        <div className="mt-4">
          <img 
            src={URL.createObjectURL(file)} 
            alt={file.name}
            className="max-w-full h-48 object-contain rounded-lg border"
          />
        </div>
      );
    }
    
    if (file.type === 'text/plain' || file.type === 'text/markdown') {
      return (
        <div className="mt-4">
          <div className="bg-gray-100 p-4 rounded-lg max-h-48 overflow-y-auto">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap">
              {file.name} - Arquivo de texto
            </pre>
          </div>
        </div>
      );
    }
    
    return (
      <div className="mt-4 p-4 bg-gray-100 rounded-lg text-center">
        <p className="text-sm text-gray-600">Preview não disponível para este tipo de arquivo</p>
      </div>
    );
  };

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterBy === 'all' || 
      (filterBy === 'processed' && doc.processed) ||
      (filterBy === 'pending' && !doc.processed);
    return matchesSearch && matchesFilter;
  });

  const sortedDocuments = [...filteredDocuments].sort((a, b) => {
    let comparison = 0;
    
    switch (sortBy) {
      case 'name':
        comparison = a.filename.localeCompare(b.filename);
        break;
      case 'size':
        comparison = a.size - b.size;
        break;
      case 'date':
        comparison = new Date(a.timestamp || 0).getTime() - new Date(b.timestamp || 0).getTime();
        break;
    }
    
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header com Estatísticas */}
        <div className="border-b border-gray-200 p-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold text-gray-900">Gerenciador de Documentos</h1>
            <button
              onClick={() => fetchStats()}
              className="bg-blue-100 text-blue-700 px-4 py-2 rounded-md hover:bg-blue-200 transition-colors"
            >
              Atualizar Estatísticas
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="flex items-center">
                <File className="h-8 w-8 text-blue-500 mr-3" />
                <div>
                  <p className="text-sm text-blue-600">Total</p>
                  <p className="text-2xl font-bold text-blue-900">{stats.total}</p>
                </div>
              </div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
                <div>
                  <p className="text-sm text-green-600">Processados</p>
                  <p className="text-2xl font-bold text-green-900">{stats.processed}</p>
                </div>
              </div>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="h-8 w-8 text-yellow-500 mr-3" />
                <div>
                  <p className="text-sm text-yellow-600">Pendentes</p>
                  <p className="text-2xl font-bold text-yellow-900">{stats.pending}</p>
                </div>
              </div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="flex items-center">
                <FileSpreadsheet className="h-8 w-8 text-purple-500 mr-3" />
                <div>
                  <p className="text-sm text-purple-600">Tamanho Total</p>
                  <p className="text-2xl font-bold text-purple-900">{formatFileSize(stats.totalSize)}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Navegação por Abas */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6 py-4">
            <button
              onClick={() => setActiveTab('upload')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'upload'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Upload de Documentos
            </button>
            <button
              onClick={() => setActiveTab('documents')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'documents'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Documentos ({documents.length})
            </button>
            <button
              onClick={() => setActiveTab('internal')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'internal'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Documentos Internos ({internalDocuments.length})
            </button>
            <button
              onClick={() => setActiveTab('stats')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'stats'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Estatísticas
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'upload' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Upload de Documentos
                </h3>
                
                {/* Área de Drop Melhorada */}
                <div 
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                    isDragActive 
                      ? 'border-blue-400 bg-blue-50' 
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input {...getInputProps()} />
                  <Upload className="h-12 w-12 text-gray-400 mb-4 mx-auto" />
                  <span className="text-lg font-medium text-gray-900">
                    {isDragActive ? 'Solte os arquivos aqui' : 'Clique para selecionar arquivos'}
                  </span>
                  <span className="text-sm text-gray-500 mt-2 block">
                    ou arraste e solte aqui
                  </span>
                  <span className="text-xs text-gray-400 mt-1 block">
                    PDF, DOC, DOCX, TXT, MD, RTF, JPG, PNG, XLS, XLSX (máx. 10MB cada)
                  </span>
                </div>

                {/* Lista de Arquivos Selecionados */}
                {selectedFiles.length > 0 && (
                  <div className="mt-6">
                    <div className="flex justify-between items-center mb-3">
                      <h4 className="text-md font-medium text-gray-900">
                        Arquivos Selecionados ({selectedFiles.length})
                      </h4>
                      <button
                        onClick={() => setSelectedFiles([])}
                        className="text-red-500 hover:text-red-700 text-sm"
                      >
                        Limpar Todos
                      </button>
                    </div>
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {selectedFiles.map((file, index) => (
                        <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-3">
                            {getFileIcon(file.type, file.name)}
                            <div>
                              <p className="font-medium text-gray-900">{file.name}</p>
                              <p className="text-sm text-gray-500">
                                {formatFileSize(file.size)}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => setPreviewFile(file)}
                              className="text-blue-500 hover:text-blue-700 p-1"
                              title="Visualizar"
                            >
                              <Eye className="h-5 w-5" />
                            </button>
                            <button
                              onClick={() => removeFile(index)}
                              className="text-red-500 hover:text-red-700 p-1"
                              title="Remover"
                            >
                              <X className="h-5 w-5" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Progresso de Upload */}
                {uploadProgress.length > 0 && (
                  <div className="mt-6">
                    <h4 className="text-md font-medium text-gray-900 mb-3">
                      Progresso do Upload
                    </h4>
                    <div className="space-y-3">
                      {uploadProgress.map((progress, index) => (
                        <div key={index} className="p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium text-gray-900">
                              {progress.file.name}
                            </span>
                            <div className="flex items-center space-x-2">
                              {progress.status === 'completed' && (
                                <CheckCircle className="h-5 w-5 text-green-500" />
                              )}
                              {progress.status === 'error' && (
                                <AlertCircle className="h-5 w-5 text-red-500" />
                              )}
                              <span className="text-sm text-gray-500">
                                {progress.progress}%
                              </span>
                            </div>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-300 ${
                                progress.status === 'completed' ? 'bg-green-500' :
                                progress.status === 'error' ? 'bg-red-500' : 'bg-blue-500'
                              }`}
                              style={{ width: `${progress.progress}%` }}
                            />
                          </div>
                          {progress.error && (
                            <p className="text-sm text-red-600 mt-2">{progress.error}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Botões de Upload */}
                {selectedFiles.length > 0 && (
                  <div className="mt-6 flex space-x-4">
                    <button
                      onClick={() => handleUpload(false)}
                      disabled={uploading}
                      className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {uploading ? 'Enviando...' : 'Enviar Documentos'}
                    </button>
                    <button
                      onClick={() => handleUpload(true)}
                      disabled={uploading}
                      className="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {uploading ? 'Enviando...' : 'Adicionar como Internos'}
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'documents' && (
            <div>
              {/* Filtros e Busca */}
              <div className="flex flex-col md:flex-row gap-4 mb-6">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <input
                      type="text"
                      placeholder="Buscar documentos..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent w-full"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <select
                    value={filterBy}
                    onChange={(e) => setFilterBy(e.target.value as any)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">Todos</option>
                    <option value="processed">Processados</option>
                    <option value="pending">Pendentes</option>
                  </select>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as any)}
                    className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="name">Nome</option>
                    <option value="size">Tamanho</option>
                    <option value="date">Data</option>
                  </select>
                  <button
                    onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                    className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                  >
                    {sortOrder === 'asc' ? <SortAsc className="h-5 w-5" /> : <SortDesc className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-medium text-gray-900">
                  Documentos Processados ({sortedDocuments.length})
                </h3>
                <button
                  onClick={fetchDocuments}
                  disabled={loading}
                  className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 disabled:opacity-50"
                >
                  {loading ? 'Carregando...' : 'Atualizar'}
                </button>
              </div>

              {sortedDocuments.length === 0 ? (
                <div className="text-center py-12">
                  <File className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">
                    {searchTerm ? 'Nenhum documento encontrado para a busca' : 'Nenhum documento encontrado'}
                  </p>
                </div>
              ) : (
                <div className="grid gap-4">
                  {sortedDocuments.map((doc) => (
                    <div
                      key={doc.filename}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        {getFileIcon(doc.content_type, doc.filename)}
                        <div>
                          <p className="font-medium text-gray-900">{doc.filename}</p>
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
                          {doc.processed ? 'Processado' : 'Pendente'}
                        </span>
                        <button
                          onClick={() => handleDeleteDocument(doc.filename)}
                          className="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 rounded-md transition-colors"
                          title="Remover documento"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'internal' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-medium text-gray-900">
                  Documentos Internos ({internalDocuments.length})
                </h3>
                <button
                  onClick={fetchInternalDocuments}
                  disabled={loading}
                  className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 disabled:opacity-50"
                >
                  {loading ? 'Carregando...' : 'Atualizar'}
                </button>
              </div>

              {internalDocuments.length === 0 ? (
                <div className="text-center py-12">
                  <File className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">Nenhum documento interno encontrado</p>
                </div>
              ) : (
                <div className="grid gap-4">
                  {internalDocuments.map((doc) => (
                    <div
                      key={doc.filename}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-3">
                        {getFileIcon(doc.content_type, doc.filename)}
                        <div>
                          <p className="font-medium text-gray-900">{doc.filename}</p>
                          <p className="text-sm text-gray-500">
                            {formatFileSize(doc.size)} • {doc.processed ? 'Processado' : 'Pendente'}
                          </p>
                          {doc.category && (
                            <span className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full mt-1">
                              {doc.category}
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleDeleteInternalDocument(doc.filename)}
                          className="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 rounded-md transition-colors"
                          title="Remover documento interno"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'stats' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Estatísticas Detalhadas</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Distribuição por Categoria</h4>
                  {Object.keys(stats.categories).length > 0 ? (
                    <div className="space-y-2">
                      {Object.entries(stats.categories).map(([category, count]) => (
                        <div key={category} className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 capitalize">{category}</span>
                          <span className="text-sm font-medium text-gray-900">{count}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Nenhuma categoria disponível</p>
                  )}
                </div>
                
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Resumo do Sistema</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Taxa de Processamento</span>
                      <span className="text-sm font-medium text-gray-900">
                        {stats.total > 0 ? Math.round((stats.processed / stats.total) * 100) : 0}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Tamanho Médio</span>
                      <span className="text-sm font-medium text-gray-900">
                        {stats.total > 0 ? formatFileSize(stats.totalSize / stats.total) : '0 Bytes'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Última Atualização</span>
                      <span className="text-sm font-medium text-gray-900">
                        {new Date().toLocaleString('pt-BR')}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modal de Preview */}
      {previewFile && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Preview: {previewFile.name}
              </h3>
              <button
                onClick={() => setPreviewFile(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
            {getFilePreview(previewFile)}
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedDocumentManager;


