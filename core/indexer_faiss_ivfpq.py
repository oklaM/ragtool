import faiss, numpy as np, json, os

def build_faiss_ivfpq(chunks, index_path='rag_ivfpq.index', nlist=128, m=8, nbits=8):
    vectors = np.array([c['embedding'] for c in chunks]).astype('float32')
    dim = vectors.shape[1]
    quantizer = faiss.IndexFlatL2(dim)
    index = faiss.IndexIVFPQ(quantizer, dim, nlist, m, nbits)
    np.random.seed(1234)
    perm = np.random.permutation(len(vectors))
    train_size = min(10000, len(vectors))
    index.train(vectors[perm[:train_size]])
    index.add(vectors)
    faiss.write_index(index, index_path)
    with open(index_path + '.meta.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False)
    return index_path
