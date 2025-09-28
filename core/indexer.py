import os, json
from core.utils import load_config
CONF = load_config()

def build_index(chunks, backend='faiss', index_path=None, **kwargs):
    if backend == 'faiss':
        import faiss, numpy as np
        index_path = index_path or CONF.get('FAISS_INDEX_PATH','rag_index.faiss')
        vectors = np.array([c['embedding'] for c in chunks]).astype('float32')
        dim = vectors.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)
        faiss.write_index(index, index_path)
        with open(index_path + '.meta.json', 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False)
        return index_path
    elif backend == 'chroma':
        from core.indexer_chroma import build_chroma_index
        return build_chroma_index(chunks, persist_directory=kwargs.get('persist_directory'))
    elif backend == 'milvus':
        from core.indexer_milvus import build_milvus_index
        return build_milvus_index(chunks, collection_name=kwargs.get('collection_name'))
    else:
        raise NotImplementedError('Unknown backend')
