import pytest
import requests_mock
from core.loaders.url_loader import UrlLoader
from core.utils import Document

def test_url_loader_instantiation():
    loader = UrlLoader()
    assert loader is not None

def test_url_loader_load_html(requests_mock):
    url = "http://test.com"
    requests_mock.get(url, text="<html><body><h1>Test</h1><p>This is a test.</p></body></html>")
    
    loader = UrlLoader()
    docs = loader.load([url])
    
    assert len(docs) == 1
    assert "Test" in docs[0].content
    assert "This is a test" in docs[0].content
    assert docs[0].source == url
