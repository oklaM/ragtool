#!/usr/bin/env python3
"""
数据管道脚本 - 创建测试索引文件
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.utils import discover_loaders, load_config, save_json
from core.chunker import docs_to_chunks
from core.embedder import embed_chunks
from core.indexer import build_index

def main():
    print("启动数据管道...")
    
    # 加载测试配置
    cfg = load_config('configs/test_config.yaml')
    print("配置加载成功")
    
    # 发现加载器
    loads = discover_loaders()
    print('发现的加载器:', list(loads.keys()))
    
    # 加载文档
    sources = cfg.get('sources', [])
    docs = []
    
    for s in sources:
        t = s.get('type')
        v = s.get('value')
        
        if t == 'file':
            Loader = loads.get('FileLoader')
            if Loader is None:
                from core.loaders.file_loader import FileLoader as Loader
            loader = Loader(v)
            docs.extend(loader.load())
            print(f'从文件加载文档: {v}')
        else:
            print(f'跳过不支持的源类型: {t}')
    
    print(f'加载了 {len(docs)} 个文档')
    
    if len(docs) == 0:
        print("警告: 没有加载到任何文档，将创建空索引")
        # 创建一个简单的测试文档
        test_doc = {
            'text': '这是一个测试文档，用于创建索引。',
            'meta': {'source': 'test', 'type': 'test'}
        }
        docs = [test_doc]
    
    # 分块
    chunk_max_chars = cfg.get('pipeline', {}).get('chunk_max_chars', 2000)
    chunk_overlap = cfg.get('pipeline', {}).get('chunk_overlap', 200)
    chunks = docs_to_chunks(docs, max_chars=chunk_max_chars, overlap=chunk_overlap)
    
    print(f'创建了 {len(chunks)} 个块')
    
    # 嵌入
    enriched = embed_chunks(chunks, cfg)
    
    # 构建索引
    idx_cfg = cfg.get('index', {})
    idx_backend = idx_cfg.get('type', 'faiss')
    idx_path = build_index(enriched, backend=idx_backend, index_path=idx_cfg.get('path'))
    
    print(f'索引已写入: {idx_path}')
    print("数据管道完成!")

if __name__ == '__main__':
    main()