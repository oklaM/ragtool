from core.utils import load_config
import openai, os, numpy as np
from core.retriever import retrieve_top_k
CONF = load_config()
class RagMCPService:
    def __init__(self,index_path=None):
        self.index_path=index_path or CONF.get('FAISS_INDEX_PATH')
    def embed_query(self,query):
        if CONF.get('OPENAI_API_KEY') and (CONF.get('EMBED_MODEL','').startswith('text-embedding') or os.getenv('OPENAI_API_KEY')):
            resp = openai.Embedding.create(model=CONF.get('EMBED_MODEL','text-embedding-3-small'), input=[query])
            return np.array(resp.data[0].embedding).astype('float32')
        else:
            from sentence_transformers import SentenceTransformer
            m=SentenceTransformer('all-MiniLM-L6-v2')
            emb=m.encode([query])[0]
            return np.array(emb).astype('float32')
    def search(self,query,top_k=5):
        q_emb=self.embed_query(query)
        hits=retrieve_top_k(q_emb,top_k=top_k,index_path=self.index_path)
        return [{'score':h['score'],'source':h['meta'].get('source'),'text':h['meta'].get('text')[:1000]} for h in hits]
