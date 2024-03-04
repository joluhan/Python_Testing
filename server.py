# Import the json module to work with JSON files and Flask framework components for web application.
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

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
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
            # Convert competition date to a datetime object.
            compDate = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
            # Check if the competition date is in the past.
            if datetime.now() > compDate:
                flash('Cannot book a past competition.')
                return redirect(url_for('index'))
        except IndexError:
            flash('Something went wrong - please try again.')
            return redirect(url_for('index'))
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    # Define the route for purchasing places.
    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        try:
            # Retrieve the competition from the list using the name provided in the form.
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            # Retrieve the club from the list using the name provided in the form.
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            # Convert the competition's date from a string to a datetime object for comparison.
            compDate = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
            # Check if the current date and time is past the competition's date and time.
            if datetime.now() > compDate:
                # Inform the user that booking for a past competition is not possible.
                flash('Cannot complete booking for a past competition.')
                # Redirect the user back to the index page.
                return redirect(url_for('index'))
        except IndexError:
            # If the competition or club specified does not exist, inform the user.
            flash('Something went wrong - booking could not be completed.')
            # Redirect the user back to the index page.
            return redirect(url_for('index'))

        placesRequired = int(request.form['places'])  # Number of places requested.
        placesAvailable = int(competition['numberOfPlaces'])  # Available places in the competition.
        clubPoints = int(club['points'])  # Current points of the club.

        # Calculate the cost of the requested places.
        cost = placesRequired

        # Check if the number of places required exceeds the maximum allowed booking limit of 12 places.
        if placesRequired > 12:
            # If it does, flash an error message to inform the user of the limit.
            flash('Cannot book more than 12 places.')
            # Then redirect the user back to the booking page to correct their input.
            return redirect(url_for('book', competition=competition['name'], club=club['name']))

        # Check if the club has enough points.
        if cost > clubPoints:
            flash('Not enough points to book the required number of places.')
            return redirect(url_for('book', competition=competition['name'], club=club['name']))

        # Check if there are enough places available in the competition.
        if placesRequired > placesAvailable:
            flash('Not enough places available in the competition.')
            return redirect(url_for('book', competition=competition['name'], club=club['name']))

        # Deduct the points from the club's total and update competition places.
        club['points'] = str(clubPoints - cost)
        competition['numberOfPlaces'] = str(placesAvailable - placesRequired)

        # Save the updated club points back to the clubs.json file.
        with open('clubs.json', 'w') as c:
            json.dump({'clubs': clubs}, c, indent=2)

        # Save the updated competition places back to the competitions.json file.
        with open('competitions.json', 'w') as comps:
            json.dump({'competitions': competitions}, comps, indent=2)

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # Define the route for logout.
    @app.route('/logout')
    def logout():
        # Redirect to the index page.
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)