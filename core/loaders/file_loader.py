import glob, os
from core.loader_base import LoaderBase

class FileLoader(LoaderBase):
    def __init__(self, pattern):
        self.pattern = pattern
    def load(self):
        out=[]
        for path in glob.glob(self.pattern, recursive=True):
            if os.path.isdir(path): continue
            try:
                with open(path,'r',encoding='utf-8') as f:
                    text=f.read()
            except Exception:
                continue
            out.append({'id':path,'text':text,'meta':{'source':'file','path':path}})
        return out
