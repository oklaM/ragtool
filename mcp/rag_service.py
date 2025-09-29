from core.utils import load_config
from core.retriever import retrieve_top_k
from core.embedder import get_embedder
from core import constants

class RagMCPService:
    def __init__(self, config):
        self.config = config
        self.embedder = get_embedder(config)
        self.index_path = config.get(constants.INDEX, {}).get(constants.PATH, 'rag_index.faiss')

    def search(self, query, top_k=5):
        q_emb = self.embedder.embed_query(query)
        hits = retrieve_top_k(q_emb, top_k=top_k, index_path=self.index_path)
        return [
            {
                'score': h['score'],
                'source': h['meta'].get('source'),
                'text': h['meta'].get('text')[:1000],
            }
            for h in hits
        ]
