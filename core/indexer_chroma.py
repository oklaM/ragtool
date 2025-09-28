import chromadb
from chromadb.config import Settings
import os, json

def build_chroma_index(chunks, persist_directory=None, collection_name='rag_collection'):
    persist_directory = persist_directory or os.getenv('CHROMA_DIR','./chroma_db')
    client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=persist_directory))
    coll = client.get_or_create_collection(collection_name)
    ids = [c['id'] for c in chunks]
    metadatas = [{'source': c.get('source'), 'title': c.get('title'), 'meta': c.get('meta',{})} for c in chunks]
    documents = [c['text'] for c in chunks]
    embeddings = [c['embedding'] for c in chunks]
    coll.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
    client.persist()
    return {'backend':'chroma','persist_directory':persist_directory,'collection':collection_name}
