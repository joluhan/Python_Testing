import pytest
from server import create_app
from server import loadClubs, loadCompetitions
# import json

@pytest.fixture # fixture to create a test client
def client():
    """Create a test client for the app."""
    flask_app = create_app() # create an instance of the app
    flask_app.config['TESTING'] = True # set the app to testing mode
    with flask_app.test_client() as client: # use the app's test client
        yield client # this is where the testing happens

# loadClubs tests
def test_load_clubs():
    """Test that the loadClubs function returns a list of clubs."""
    clubs = loadClubs()
    assert isinstance(clubs, list), "loadClubs should return a list" # Check that the return value is a list
    assert len(clubs) > 0, "Should load at least one club" # Check that at least one club is loaded
    assert all("name" in club for club in clubs), "Each club should have a name" # Check that each club has a name
    
# loadCompetitions tests
def test_load_competitions():
    """Test that the loadCompetitions function returns a list of competitions."""
    competitions = loadCompetitions()
    assert isinstance(competitions, list), "loadCompetitions should return a list" # Check that the return value is a list
    assert len(competitions) > 0, "Should load at least one competition" # Check that at least one competition is loaded
    assert all("name" in competition for competition in competitions), "Each competition should have a name" # Check that each competition has a name

# Index tests
def test_index_route_loads(client): # test passed
    """Happy path for index route."""
    response = client.get('/') # send a GET request to the index route
    assert response.status_code == 200 # check that the response is OK
    assert b"Welcome" in response.data # check for unique content from index.html to ensure it's the correct template

# ShowSummary tests
def test_show_summary_valid_login(client): # test passed
    """Happy path for valid login."""
    response = client.post('/showSummary', data={'email': 'test@userid.co.uk'}, follow_redirects=True) # send a POST request to the showSummary route
    assert b"Points available:" in response.data # check for unique content from showSummary.html to ensure it's the correct template

def test_show_summary_invalid_login(client): # test passed
    """Sad path for invalid login."""
    response = client.post('/showSummary', data={'email': 'invalid_email@example.com'}, follow_redirects=True) # send a POST request to the showSummary route
    assert b"Sorry, that email was not found." in response.data # check for the flash message

def test_show_summary_empty_email(client): # test passed
    """Sad path for empty email."""
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True) # send a POST request to the showSummary route
    assert b"Sorry, that email was not found." in response.data # check for the flash message

# Book tests
def test_book_route_valid(client): # test passed
    """Happy path for booking with valid competition and club."""
    response = client.get('/book/Future Competition Test/Test Club') # send a GET request to the booking route
    assert response.status_code == 200
    assert b'Booking for' in response.data # check for unique content from booking.html to ensure it's the correct template

def test_book_past_competition(client): # test passed
    """Sad path for attempting to book a past competition."""
    response = client.get('/book/Past Competition Test/Test Club', follow_redirects=True) # send a GET request to the booking route
    assert b'Cannot book a past competition.' in response.data # check for the flash message

def test_book_invalid_competition(client): # test passeds
    """Sad path for invalid competition."""
    response = client.get('/book/InvalidCompetition/Test Club', follow_redirects=True)
    assert b'Something went wrong - please try again.' in response.data

# PurchasePlaces tests
def test_purchase_places_success(client): # test passed
    """Happy path for a successful purchase."""
    response = client.post('/purchasePlaces', data={'competition': 'Future Competition Test', 'club': 'Test Club', 'places': '1'}, follow_redirects=True)
    assert b'Great-booking complete!' in response.data

def test_purchase_places_past_competition(client): # test passed
    """Sad path for attempting to purchase places for a past competition."""
    response = client.post('/purchasePlaces', data={'competition': 'Past Competition Test', 'club': 'Test Club', 'places': '1'}, follow_redirects=True)
    assert b'Cannot complete booking for a past competition.' in response.data

# Logout tests
def test_logout_redirects_to_index(client): # test passed
    """Happy path for logout."""
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    assert '/' in response.headers['Location']

def test_logout_follow_redirect(client): # test passed
    """Extra test for logout to ensure redirection to index works as expected."""
    response = client.get('/logout', follow_redirects=True) 
    assert response.status_code == 200
    assert b"Welcome" in response.data
