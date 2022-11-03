import pytest
from fastapi.testclient import TestClient

from app_spam_filter_fr.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_detect_spam(client):
    json = {"text": "Vous avez gagné un cadeau, cliquez ici pour le recevoir !"}
    response = client.post("/verify", json=json).json()
    assert response["is_spam"] == True


def test_detect_ham(client):
    json = {"text": "On se retrouve à 14h devant chez moi"}
    response = client.post("/verify", json=json).json()
    assert response["is_spam"] == False
