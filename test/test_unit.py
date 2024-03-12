import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_show_summary_valid_login(client):
    # Using "test@userid.co.uk" as testing email
    response = client.post('/showSummary', data={'email': 'test@userid.co.uk'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Points available:" in response.data


