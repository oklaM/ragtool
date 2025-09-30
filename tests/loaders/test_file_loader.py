import pytest
from core.loaders.file_loader import FileLoader
from core.utils import Document
import os

def test_file_loader_instantiation():
    loader = FileLoader()
    assert loader is not None

def test_file_loader_load_txt():
    # Create a dummy txt file
    with open("test.txt", "w") as f:
        f.write("This is a test.")
    
    loader = FileLoader()
    docs = loader.load(["test.txt"])
    
    assert len(docs) == 1
    assert docs[0].content == "This is a test."
    assert docs[0].source == "test.txt"

    os.remove("test.txt")
