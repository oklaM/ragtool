import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from core.loader_base import LoaderBase
HEADERS = {"User-Agent":"rag-tool-bot/1.0"}

class URLLoader(LoaderBase):
    def __init__(self, start_url, max_pages=300, delay=0.2):
        self.start_url = start_url
        self.max_pages = max_pages
        self.delay = delay
    def extract_page(self, url):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print('fetch error', url, e)
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        title_tag = soup.find(['h1']) or soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else url
        content_parts = []
        main = soup.find('article') or soup.find(id='content') or soup
        for el in main.find_all(['h1','h2','h3','h4','p','li','pre','code']):
            text = el.get_text("\n", strip=True)
            if text:
                content_parts.append(text)
        text = "\n\n".join(content_parts)
        return {'id':url,'text':text,'meta':{'source':url,'title':title}}
    def load(self):
        seen=set(); to_visit=[self.start_url]; docs=[]
        while to_visit and len(seen)<self.max_pages:
            url=to_visit.pop(0)
            if url in seen: continue
            page=self.extract_page(url)
            seen.add(url)
            if page and page.get('text'): docs.append(page)
            try:
                r = requests.get(url, headers=HEADERS, timeout=10)
                r.raise_for_status()
                soup=BeautifulSoup(r.text,'html.parser')
                for a in soup.find_all('a', href=True):
                    href=urljoin(url,a['href'])
                    if href.startswith('http') and href not in seen and href not in to_visit:
                        to_visit.append(href)
            except Exception:
                pass
            time.sleep(self.delay)
        return docs
