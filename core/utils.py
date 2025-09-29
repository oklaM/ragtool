import os, json, importlib.util, glob, yaml
from dotenv import load_dotenv
load_dotenv()

def load_config(config_path='configs/config.yaml'):
    with open(config_path, 'r') as f:
        config_str = f.read()
    config_str = os.path.expandvars(config_str)
    config = yaml.safe_load(config_str)
    
    # Override with environment variables for some keys
    config['embedding']['api_key'] = os.getenv('OPENAI_API_KEY', config.get('embedding', {}).get('api_key'))
    config['sources'] = [
        {**s, 'value': os.getenv('NOTION_DATABASE_ID') if s['type'] == 'notion' else s['value']}
        for s in config.get('sources', [])
    ]
    return config

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
