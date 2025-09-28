"""Enhanced NotionLoader with backoff and attachments
"""
import os, time, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.loader_base import LoaderBase
try:
    from notion_client import Client
except Exception:
    Client = None
ATTACH_DIR = os.getenv('NOTION_ATTACH_DIR','attachments')
os.makedirs(ATTACH_DIR, exist_ok=True)

def _safe_filename(url):
    name = url.split('/')[-1].split('?')[0]
    name = re.sub(r'[^A-Za-z0-9_.-]','_',name)
    return name

class NotionLoader(LoaderBase):
    def __init__(self, token=None, database_id=None, page_id=None, max_pages=1000, max_workers=8, max_retries=5):
        self.token = token or os.getenv('NOTION_TOKEN')
        self.database_id = database_id or os.getenv('NOTION_DATABASE_ID')
        self.page_id = page_id
        self.max_pages = max_pages
        self.max_workers = max_workers
        self.max_retries = max_retries
        if Client is None:
            raise RuntimeError('notion-client required')
        self.client = Client(auth=self.token)
    def _backoff(self, attempt):
        base=0.5
        sleep = base * (2**attempt) + (0.1*(attempt%3))
        return min(sleep,30)
    def _fetch_blocks_page(self,page_id,start_cursor=None):
        attempt=0
        while attempt<self.max_retries:
            try:
                resp=self.client.blocks.children.list(block_id=page_id,start_cursor=start_cursor)
                return resp
            except Exception as e:
                time.sleep(self._backoff(attempt))
                attempt+=1
        raise RuntimeError('failed fetch blocks')
    def _get_all_blocks(self,page_id):
        results=[]
        cursor=None
        while True:
            resp=self._fetch_blocks_page(page_id,cursor)
            results.extend(resp.get('results',[]))
            if not resp.get('has_more'): break
            cursor=resp.get('next_cursor')
        return results
    def _blocks_to_text_and_attachments(self,blocks):
        parts=[]
        attachments=[]
        for b in blocks:
            t=b.get('type')
            rich=b.get(t,{})
            arr=rich.get('rich_text') or rich.get('title') or rich.get('text') or []
            if isinstance(arr,list):
                parts.append(''.join([x.get('plain_text','') for x in arr]))
            else:
                if isinstance(rich,dict):
                    maybe=rich.get('plain_text')
                    if maybe: parts.append(maybe)
            if t in ('image','file'):
                file_field = rich.get('file') or rich.get('external') or {}
                url = file_field.get('url')
                if url:
                    fname=_safe_filename(url)
                    attachments.append((url,fname))
        return '\n\n'.join([p for p in parts if p]), attachments
    def _download_attachment(self,url_fname):
        url,fname=url_fname
        path=os.path.join(ATTACH_DIR,fname)
        if os.path.exists(path): return path
        try:
            r=requests.get(url,timeout=30,stream=True)
            r.raise_for_status()
            with open(path,'wb') as f:
                for chunk in r.iter_content(1024*32):
                    if chunk: f.write(chunk)
            return path
        except Exception as e:
            print('attachment download failed',url,e); return None
    def _extract_page(self,page_id):
        blocks=self._get_all_blocks(page_id)
        text, attachments = self._blocks_to_text_and_attachments(blocks)
        downloaded=[]
        if attachments:
            with ThreadPoolExecutor(max_workers=min(len(attachments), self.max_workers)) as ex:
                futures={ex.submit(self._download_attachment,a):a for a in attachments}
                for fut in as_completed(futures):
                    res=fut.result()
                    if res: downloaded.append(res)
        return text, downloaded
    def load(self):
        docs=[]
        if self.database_id:
            cursor=None; count=0
            while True:
                attempt=0
                while attempt<self.max_retries:
                    try:
                        res=self.client.databases.query(database_id=self.database_id, start_cursor=cursor)
                        break
                    except Exception as e:
                        time.sleep(self._backoff(attempt)); attempt+=1
                else:
                    raise RuntimeError('failed query')
                for r in res.get('results',[]):
                    if count>=self.max_pages: break
                    page_id=r.get('id')
                    title=None
                    props=r.get('properties',{})
                    for v in props.values():
                        if v.get('type')=='title':
                            title_list=v.get('title',[])
                            title=''.join([t.get('plain_text','') for t in title_list]); break
                    text, attachments = self._extract_page(page_id)
                    meta={'source':'notion','page_id':page_id,'title':title,'attachments':attachments}
                    docs.append({'id':page_id,'text':text,'meta':meta}); count+=1
                if count>=self.max_pages: break
                if not res.get('has_more'): break
                cursor=res.get('next_cursor')
            return docs
        if self.page_id:
            text, attachments = self._extract_page(self.page_id)
            docs.append({'id':self.page_id,'text':text,'meta':{'source':'notion','page_id':self.page_id,'attachments':attachments}})
        return docs
