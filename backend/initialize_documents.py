
importsys
importos
frompathlibimportPath

sys.path.append(str(Path(__file__).parent))

fromchatbot.internal_document_managerimportInternalDocumentManager
fromchatbot.optimized_vector_storeimportOptimizedVectorStore
fromchatbot.document_processorimportDocumentProcessor

definitialize_system():
    """Inicializa o sistema processando documentos existentes"""

print("🚀 Inicializando sistema de documentos internos...")

doc_manager=InternalDocumentManager()
vector_store=OptimizedVectorStore()
doc_processor=DocumentProcessor()

unprocessed=doc_manager.get_unprocessed_documents()

ifnotunprocessed:
        print("✅ Todos os documentos já foram processados!")
return

print(f"📄 Encontrados {len(unprocessed)} documentos não processados")

forfilenameinunprocessed:
        print(f"🔄 Processando: {filename}")

try:

            content=doc_manager.get_document_content(filename)

ifcontent:

                chunks=doc_processor.split_text(content,chunk_size=1000,overlap=200)

success=vector_store.add_documents(
chunks,
[filename]*len(chunks),
[{"category":doc_manager.documents_metadata[filename]["category"]}for_inchunks]
)

ifsuccess:

                    doc_manager.mark_as_processed(filename,True)
print(f"✅ {filename} processado com sucesso ({len(chunks)} chunks)")
else:
                    print(f"❌ Erro ao processar {filename}")
else:
                print(f"⚠️ Não foi possível ler o conteúdo de {filename}")

exceptExceptionase:
            print(f"❌ Erro ao processar {filename}: {e}")

print("\nEstatisticas do sistema otimizado:")
doc_stats=doc_manager.get_statistics()
vector_stats=vector_store.get_statistics()

print(f"   Documentos internos: {doc_stats['total_documents']}")
print(f"   Tamanho total: {doc_stats['total_size_mb']} MB")
print(f"   Categorias: {list(doc_stats['categories'].keys())}")
print(f"   Chunks no banco vetorial: {vector_stats['total_documents']}")
print(f"   Categorias pre-processadas: {len(vector_stats.get('preprocessed_categories',[]))}")
print(f"   Cache de busca: {vector_stats.get('cache_size',0)} consultas")

print("\nSistema otimizado inicializado com sucesso!")
print("O sistema agora inclui:")
print("   • Cache inteligente para respostas rápidas")
print("   • Busca otimizada por categoria")
print("   • Carregamento preguiçoso de componentes")
print("   • Processamento NLP otimizado")

if__name__=="__main__":
    initialize_system()
