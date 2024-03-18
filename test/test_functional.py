import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_book_past_competition(client):
    # Use the 'Past Competition Test' competition and 'Test Club'
    response = client.get('/book/Past Competition Test/Test Club', follow_redirects=False)
    assert response.status_code == 302  # Expect a redirect to the index page

    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        # Check if the specific message is in the list of flash messages
        assert any('Cannot book a past competition.' in message for category, message in flashes)

def test_book_valid_competition(client):
    # Using "Future Competition Test" from competition.json and "Test Club" as valid club name in clubs.json
    response = client.get('/book/Future Competition Test/Test Club', follow_redirects=False)
    assert response.status_code == 200
    assert 'Book</button>' in response.data.decode('utf-8')

def test_purchase_places_success(client):
    # Simulate a scenario where booking is successful.
    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition Test',
        'club': 'Test Club',
        'places': '1'
    })
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

def test_purchase_places_insufficient_points(client):
    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition Test',
        'club': 'Test Club',
        'places': '10'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Not enough points to book the required number of places." in response.data
