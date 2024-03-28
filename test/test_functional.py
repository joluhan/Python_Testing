import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_book_past_competition(client): # test passed
    """Sad path for attempting to book a past competition."""
    # Use the 'Past Competition Test' competition and 'Test Club'
    response = client.get('/book/Past Competition Test/Test Club', follow_redirects=False) # Send a GET request to the booking route
    assert response.status_code == 302  # Expect a redirect to the index page
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', []) # Get the flash messages from the session
        # Check if the specific message is in the list of flash messages
        assert any('Cannot book a past competition.' in message for category, message in flashes) # Check for the flash message

def test_book_valid_competition(client):
    """Happy path for booking with valid competition and club."""
    # Using "Future Competition Test" from competition.json and "Test Club" as valid club name in clubs.json
    response = client.get('/book/Future Competition Test/Test Club', follow_redirects=False)
    assert response.status_code == 200
    assert 'Book</button>' in response.data.decode('utf-8') # Check for the booking button

def test_purchase_places_success(client):
    """Happy path for a successful purchase."""
    # Simulate a scenario where booking is successful.
    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition Test',
        'club': 'Test Club',
        'places': '1'
    }) # Send a POST request to the purchasePlaces route
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data # Check for the flash message

def test_purchase_places_insufficient_points(client):
    """Sad path for insufficient points to book the required number of places."""
    response = client.post('/purchasePlaces', data={
        'competition': 'Future Competition Test',
        'club': 'Test Club',
        'places': '10'
    }, follow_redirects=True)    
    assert response.status_code == 200
    assert b"Not enough points to book the required number of places." in response.data

def test_purchase_more_than_12_places(client):
    """Sad path for attempting to book more than 12 places."""
    competition_name = "Future Competition Test"
    club_name = "Test Club"
    places_to_purchase = "13"  # More than the limit of 12 places    
    # Execute the request
    response = client.post('/purchasePlaces', data={
        'competition': competition_name,
        'club': club_name,
        'places': places_to_purchase
    }, follow_redirects=True)
    assert b'Cannot book more than 12 places.' in response.data
