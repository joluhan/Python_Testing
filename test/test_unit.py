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

def test_show_summary_invalid_login(client):
    response = client.post('/showSummary', data={'email': 'notarealemail@example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sorry, that email was not found." in response.data

def test_book_past_competition(client):
    # Use the 'Winter Classic' competition and 'Test Club'
    response = client.get('/book/Winter Classic/Test Club', follow_redirects=False)
    assert response.status_code == 302  # Expect a redirect to the index page

    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        # Check if the specific message is in the list of flash messages
        assert any('Cannot book a past competition.' in message for category, message in flashes)

def test_book_valid_competition(client):
    # Using "Summer Showdown" from competition.json and "Test Club" as valid club name in clubs.json
    response = client.get('/book/Summer Showdown/Test Club', follow_redirects=False)
    assert response.status_code == 200
    assert 'Book</button>' in response.data.decode('utf-8')
