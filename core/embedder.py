import os, time, numpy as np
from core.utils import load_config
import abc
from core import constants

class Embedder(abc.ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abc.abstractmethod
    def embed(self, texts):
        pass

    def embed_query(self, query):
        return self.embed([query])[0]

class OpenAIEmbedder(Embedder):
    def __init__(self, model_name, api_key):
        super().__init__(model_name)
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def embed(self, texts, batch_size=16):
        embs = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            resp = self.client.embeddings.create(input=batch_texts, model=self.model_name)
            for d in resp.data:
                embs.append(d.embedding)
            time.sleep(0.2)
        return embs

class SentenceTransformerEmbedder(Embedder):
    def __init__(self, model_name):
        super().__init__(model_name)
        from sentence_transformers import SentenceTransformer
        self._st_model = SentenceTransformer(model_name)

    def embed(self, texts):
        embs = self._st_model.encode(texts, show_progress_bar=False)
        return [e.tolist() if hasattr(e, 'tolist') else e for e in embs]

def get_embedder(config):
    provider = config.get(constants.EMBEDDING, {}).get(constants.PROVIDER, constants.PROVIDER_AUTO)
    model_name = config.get(constants.EMBEDDING, {}).get(constants.MODEL)
    api_key = config.get(constants.EMBEDDING, {}).get(constants.API_KEY)

    if provider == constants.PROVIDER_OPENAI or (provider == constants.PROVIDER_AUTO and model_name and model_name.startswith('text-embedding')):
        return OpenAIEmbedder(model_name or 'text-embedding-3-small', api_key)
    else:
        return SentenceTransformerEmbedder(model_name or 'all-MiniLM-L6-v2')

def embed_chunks(chunks, config):
    embedder = get_embedder(config)
    texts = [c['text'] for c in chunks]
    vecs = embedder.embed(texts)
    for c, v in zip(chunks, vecs):
        c['embedding'] = v
    return chunks
