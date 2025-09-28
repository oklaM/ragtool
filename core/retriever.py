import faiss, numpy as np, json
from core.utils import load_config
CONF = load_config()

def load_index(index_path=None):
    index_path = index_path or CONF.get('FAISS_INDEX_PATH')
    index = faiss.read_index(index_path)
    with open(index_path + '.meta.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)
    return index, meta

def retrieve_top_k(query_emb, top_k=5, index_path=None):
    index, meta = load_index(index_path)
    D, I = index.search(np.array([query_emb]).astype('float32'), top_k)
    hits = []
    for dist, idx in zip(D[0], I[0]):
        if idx < 0: continue
        item = meta[idx]
        hits.append({'score': float(dist), 'meta': item})
    return hits
