# Import the json module to work with JSON files and Flask framework components for web application.
import json
from flask import Flask, render_template, request, redirect, flash, url_for

# Function to load clubs from a JSON file.
def loadClubs():
    # Open the clubs.json file for reading.
    with open('clubs.json') as c:
        # Load JSON content and access the 'clubs' data.
        listOfClubs = json.load(c)['clubs']
        # Return the list of clubs.
        return listOfClubs

# Function to load competitions from a JSON file.
def loadCompetitions():
    # Open the competitions.json file for reading.
    with open('competitions.json') as comps:
        # Load JSON content and access the 'competitions' data.
        listOfCompetitions = json.load(comps)['competitions']
        # Return the list of competitions.
        return listOfCompetitions

def create_app(test_config=None):
    # Initialize a Flask application instance.
    app = Flask(__name__)
    # Set a secret key for session management and flash messages.
    app.secret_key = 'something_special'

    # Load competitions and clubs data into variables.
    competitions = loadCompetitions()
    clubs = loadClubs()

    # Define the route for the index page.
    @app.route('/')
    def index():
        # Return the index.html template.
        return render_template('index.html')

    # Define the route for showing summary after a POST request.
    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        try:
            # Try to find the club by the email provided in the form.
            club = [club for club in clubs if club['email'] == request.form['email']][0]
        except IndexError:
            # If no club is found, flash an error message and redirect to the index.
            flash('Sorry, that email wasn\'t found.')
            return redirect(url_for('index'))

        # If a club is found, render the welcome page with the club's and competitions' details.
        return render_template('welcome.html', club=club, competitions=competitions)

    # Define the route for booking.
    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            # Find club and competition by name, raise IndexError if not found.
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
        except IndexError:
            # If not found, flash an error message and redirect.
            flash('Something went wrong - please try again.')
            return redirect(url_for('index'))
        # If both are found, render the booking page with their details.
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    # Define the route for purchasing places.
    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        try:
            # Find competition and club by name from form data.
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
        except IndexError:
            # If not found, flash an error message and redirect.
            flash('Something went wrong - booking could not be completed.')
            return redirect(url_for('index'))

        placesRequired = int(request.form['places'])  # Number of places requested.
        placesAvailable = int(competition['numberOfPlaces'])  # Available places in the competition.
        clubPoints = int(club['points'])  # Current points of the club.

        # Check if the club has enough points (assuming 1 place = 3 points).
        if placesRequired * 3 > clubPoints:
            flash('Not enough points')
            return redirect(url_for('book', competition=competition['name'], club=club['name']))

        # Check if there are enough places available in the competition.
        if placesRequired > placesAvailable:
            flash('Not enough places available')
            return redirect(url_for('book', competition=competition['name'], club=club['name']))

        # Update competition places and club points.
        competition['numberOfPlaces'] = str(placesAvailable - placesRequired)
        club['points'] = str(clubPoints - (placesRequired * 3))

        # Get the number of places required from form data.
        placesRequired = int(request.form['places'])
        # Subtract the required places from competition's available places.
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        # Show success message and redirect back to the welcome page with updated data.

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Define the route for logout.
    @app.route('/logout')
    def logout():
        # Redirect to the index page.
        return redirect(url_for('index'))

