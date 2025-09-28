from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import os, numpy as np, json

def build_milvus_index(chunks, collection_name='rag_collection', host=None, port=None):
    host = host or os.getenv('MILVUS_HOST','127.0.0.1')
    port = port or os.getenv('MILVUS_PORT','19530')
    connections.connect(host=host, port=str(port))
    dim = len(chunks[0]['embedding'])
    fields = [
        FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='emb', dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=65535)
    ]
    schema = CollectionSchema(fields, description='RAG collection')
    if utility.has_collection(collection_name):
        coll = Collection(collection_name)
    else:
        coll = Collection(name=collection_name, schema=schema)
    texts = [c['text'] for c in chunks]
    embs = [list(map(float, c['embedding'])) for c in chunks]
    coll.insert([embs, texts])
    index_params = {'metric_type':'L2','index_type':'IVF_FLAT','params':{'nlist':128}}
    coll.create_index('emb', index_params)
    coll.load()
    return {'backend':'milvus','collection':collection_name}
