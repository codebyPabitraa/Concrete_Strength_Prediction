import pytest
import json
from app_flask import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_predict_missing_feature(client):
    # Only sending one feature when 8 are expected
    payload = {
        "Cement": 500
    }
    response = client.post('/predict', json=payload)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing feature' in data['error']
