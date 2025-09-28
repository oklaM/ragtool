import os, json, importlib.util, glob
from dotenv import load_dotenv
load_dotenv()

def load_config():
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'EMBED_MODEL': os.getenv('EMBED_MODEL','text-embedding-3-small'),
        'CHUNK_MAX_CHARS': int(os.getenv('CHUNK_MAX_CHARS',2000)),
        'CHUNK_OVERLAP': int(os.getenv('CHUNK_OVERLAP',200)),
        'BASE_URL': os.getenv('BASE_URL','https://www.backtrader.com/docu/'),
        'FAISS_INDEX_PATH': os.getenv('FAISS_INDEX_PATH','rag_index.faiss'),
        'DOCS_JSON': os.getenv('DOCS_JSON','docs.json'),
    }

def save_json(path, obj):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def discover_loaders(paths=('core/loaders','plugins')):
    loaders = {}
    for base in paths:
        pattern = os.path.join(base, '*.py')
        for p in glob.glob(pattern):
            name = os.path.splitext(os.path.basename(p))[0]
            spec = importlib.util.spec_from_file_location(name, p)
            try:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    try:
                        bases = [b.__name__ for b in getattr(obj, '__mro__', [])]
                        if 'LoaderBase' in bases and attr != 'LoaderBase':
                            loaders[attr] = obj
                    except Exception:
                        continue
            except Exception as e:
                print('failed to import', p, e)
    return loaders
