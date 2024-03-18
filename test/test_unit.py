import pytest
from server import create_app
from server import loadClubs
from server import loadCompetitions
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True # Set the app to testing mode
    with app.test_client() as client: # Use the app's test client
        yield client # This is where the testing happens

def test_index_route(client):
    response = client.get('/') # Send a GET request to the index route
    assert response.status_code == 200 # Check that the response is OK
    assert b"Welcome" in response.data # Check for unique content from index.html to ensure it's the correct template

def test_show_summary_valid_login(client):
    # Using "test@userid.co.uk" as testing email
    response = client.post('/showSummary', data={'email': 'test@userid.co.uk'}, follow_redirects=True) # Send a POST request to the showSummary route
    assert response.status_code == 200 # Check that the response is OK
    assert b"Points available:" in response.data # Check for unique content from showSummary.html to ensure it's the correct template

def test_show_summary_invalid_login(client):
    response = client.post('/showSummary', data={'email': 'notarealemail@example.com'}, follow_redirects=True) # Send a POST request to the showSummary route
    assert response.status_code == 200 # Check that the response is OK
    assert b"Sorry, that email was not found." in response.data # Check for the flash message

def test_show_summary_invalid_email_flash_message(client):
    response = client.post('/showSummary', data={'email': 'fakeemail@test.com'}, follow_redirects=True) # Send a POST request to the showSummary route
    assert b"Sorry, that email was not found." in response.data, "Flash message for invalid email not found." # Check for the flash message

def test_show_summary_invalid_email_redirection(client):
    response = client.post('/showSummary', data={'email': 'nonexistentemail@test.com'}) # Send a POST request to the showSummary route
    assert response.status_code == 302, "Response should be a redirect." # Check that the response is a redirect
    assert '/showSummary' not in response.headers['Location'], "Should not redirect back to showSummary." # Check that the response does not redirect back to showSummary

def test_booking_route_success(client):
    valid_competition = 'Future Competition Test'
    valid_club = 'Test Club'
    response = client.get(f'/book/{valid_competition}/{valid_club}') # Send a GET request to the booking route
    assert response.status_code == 200 # Check that the response is OK
    assert b'Places available:' in response.data # Check for unique content from booking.html to ensure it's the correct template
    assert b'action="/purchasePlaces"' in response.data # Ensure the booking form is rendered

def test_welcome_route_after_login(client):
    valid_email = 'test@userid.co.uk'
    response = client.post('/showSummary', data={'email': valid_email}, follow_redirects=True) # Send a POST request to the showSummary route
    assert response.status_code == 200 # Check that the response is OK
    assert b'Points available:' in response.data # Check for unique content from showSummary.html to ensure it's the correct template
    assert b'Competitions:' in response.data # Check for unique content from showSummary.html to ensure it's the correct template

def test_load_clubs():
    clubs = loadClubs()
    assert isinstance(clubs, list), "loadClubs should return a list" # Check that the return value is a list
    assert len(clubs) > 0, "Should load at least one club" # Check that at least one club is loaded
    assert all("name" in club for club in clubs), "Each club should have a name" # Check that each club has a name

def update_club_points(club, points_to_deduct):
    club['points'] = str(int(club['points']) - points_to_deduct) # Deduct points from the club
    return club

def test_update_club_points():
    club = {'name': 'Test Club', 'points': '100'}
    update_club_points(club, 30) # Deduct 30 points
    assert club['points'] == '70', "Club points should be correctly updated after deduction" # Check that the points have been correctly updated

def test_load_competitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list), "loadCompetitions should return a list" # Check that the return value is a list
    assert len(competitions) > 0, "Should load at least one competition" # Check that at least one competition is loaded
    assert all("name" in competition for competition in competitions), "Each competition should have a name" # Check that each competition has a name

def is_competition_in_future(competition_date):
    comp_date = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S') # Convert the string to a datetime object
    return datetime.now() < comp_date # Check if the competition date is in the future

def test_competition_in_future():
    future_date = "2099-01-01 00:00:00"
    assert is_competition_in_future(future_date), "Competition should be in the future" # Check that the function returns True for a future date

def test_competition_in_past():
    past_date = "2000-01-01 00:00:00"
    assert not is_competition_in_future(past_date), "Competition should be in the past" # Check that the function returns False for a past date

def test_logout_route(client):
    response = client.get('/logout') # Send a GET request to the logout route
    assert response.status_code == 302 # Check that the response is a redirect

def test_logout_route_redirection(client):
    response = client.get('/logout', follow_redirects=False) # Send a GET request to the logout route
    assert response.status_code == 302, "Logout should redirect." # Check that the response is a redirect
    assert '/' in response.headers['Location'], "Logout should redirect to the index page." # Check that the response redirects to the index page
