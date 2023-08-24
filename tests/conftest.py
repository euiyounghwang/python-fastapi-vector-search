import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from injector import es_client

@pytest.fixture
def mock_client():
    # app = FastAPI()
    client = TestClient(app)
    
    return client

@pytest.fixture
def mock_es_client():
    return es_client