# Import the json module to work with JSON files and Flask framework components for web application.
import json
from flask import Flask, render_template, request, redirect, flash, url_for

# Function to load clubs from a JSON file.
def loadClubs():
    with open('clubs.json') as c:  # Open the clubs.json file for reading.
        listOfClubs = json.load(c)['clubs']  # Load JSON content and access the 'clubs' data.
        return listOfClubs  # Return the list of clubs.

# Function to load competitions from a JSON file.
def loadCompetitions():
    with open('competitions.json') as comps:  # Open the competitions.json file for reading.
        listOfCompetitions = json.load(comps)['competitions']  # Load JSON content and access the 'competitions' data.
        return listOfCompetitions  # Return the list of competitions.

# Initialize a Flask application instance.
app = Flask(__name__)
app.secret_key = 'something_special'  # Set a secret key for session management and flash messages.

# Load competitions and clubs data into variables.
competitions = loadCompetitions()
clubs = loadClubs()

# Define the route for the index page.
@app.route('/')
def index():
    return render_template('index.html')  # Return the index.html template.

# Define the route for showing summary after a POST request.
@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]  # Find club by email from form data.
    return render_template('welcome.html', club=club, competitions=competitions)  # Render welcome template with club and competitions data.

# Define the route for booking.
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]  # Find club by name.
    foundCompetition = [c for c in competitions if c['name'] == competition][0]  # Find competition by name.
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)  # Render booking template with found club and competition.
    else:
        flash("Something went wrong-please try again")  # Show error message if something goes wrong.
        return render_template('welcome.html', club=club, competitions=competitions)  # Redirect back to welcome page.

# Define the route for purchasing places.
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]  # Find competition by name from form data.
    club = [c for c in clubs if c['name'] == request.form['club']][0]  # Find club by name from form data.
    placesRequired = int(request.form['places'])  # Get the number of places required from form data.
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired  # Subtract the required places from competition's available places.
    flash('Great-booking complete!')  # Show success message.
    return render_template('welcome.html', club=club, competitions=competitions)  # Redirect back to welcome page with updated data.

# TODO: Add route for points display

# Define the route for logout.
@app.route('/logout')
def logout():
    return redirect(url_for('index'))  # Redirect to the index page.
