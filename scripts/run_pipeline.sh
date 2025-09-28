#!/usr/bin/env bash
set -e
python - <<'PY'
from core.utils import discover_loaders, load_config, save_json
import yaml, os
cfg = yaml.safe_load(open('configs/config.yaml'))
loads = discover_loaders()
print('Discovered loaders:', list(loads.keys()))
sources = cfg.get('sources', [])
docs = []
for s in sources:
    t = s.get('type')
    v = s.get('value')
    if t == 'url':
        Loader = loads.get('URLLoader')
        if Loader is None:
            from core.loaders.url_loader import URLLoader as Loader
        loader = Loader(v)
        docs.extend(loader.load())
    elif t == 'file':
        Loader = loads.get('FileLoader')
        if Loader is None:
            from core.loaders.file_loader import FileLoader as Loader
        loader = Loader(v)
        docs.extend(loader.load())
    elif t == 'pdf':
        Loader = loads.get('PDFLoader')
        if Loader is None:
            from core.loaders.pdf_loader import PDFLoader as Loader
        loader = Loader(v)
        docs.extend(loader.load())
    elif t == 'notion':
        Loader = loads.get('NotionLoader')
        if Loader is None:
            from core.loaders.notion_loader import NotionLoader as Loader
        loader = Loader(token=os.getenv('NOTION_TOKEN'), database_id=v)
        docs.extend(loader.load())
    elif t == 's3':
        Loader = loads.get('S3Loader')
        if Loader is None:
            from core.loaders.s3_loader import S3Loader as Loader
        bucket, prefix = v.split('|',1) if '|' in v else (v,'')
        loader = Loader(bucket, prefix=prefix)
        docs.extend(loader.load())
    else:
        print('Unknown source type', t)
print('Loaded', len(docs), 'documents')
from core.chunker import docs_to_chunks
from core.embedder import embed_chunks
from core.indexer import build_index
chunks = docs_to_chunks(docs, max_chars=cfg.get('pipeline',{}).get('chunk_max_chars',2000), overlap=cfg.get('pipeline',{}).get('chunk_overlap',200))
save_json('docs.json', docs)
save_json('chunks.json', chunks)
print('Created', len(chunks), 'chunks')
enriched = embed_chunks(chunks)
save_json('chunks_emb.json', enriched)
idx_cfg = cfg.get('index',{})
idx_backend = idx_cfg.get('type','faiss')
idx_path = build_index(enriched, backend=idx_backend, index_path=idx_cfg.get('path'))
print('Index written to', idx_path)
PY
