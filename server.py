import json
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    """Load clubs from a JSON file."""
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    """Load competitions from a JSON file."""
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

def initialize_app(config={}):
    """
    Initialize the Flask application.
    
    This function uses the app factory pattern to create a Flask application instance.
    It allows for dynamic configuration, making the app easily testable and configurable.
    
    Parameters:
    - config: A dictionary of configuration keys and values to initialize the app with.
    """
    app = Flask(__name__)
    app.config.update(config)  # Update the app's configuration
    app.secret_key = "something_special"  # Set a secret key for sessions and cookies
    
    # Load competitions and clubs data into the app
    competitions = loadCompetitions()
    clubs = loadClubs()

    @app.route("/")
    def index():
        """Render the index page."""
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        """
        Show summary for the club based on the email provided.
        
        This route handles POST requests from the index page where a user submits their email.
        It attempts to find the club associated with the email and displays a summary if found.
        Otherwise, it redirects to the index page with an error message.
        """
        try:
            # Find the club by email; if not found, None is returned.
            club = next((club for club in clubs if club["email"] == request.form["email"]), None)
            if club is None:
                raise ValueError  # Trigger error handling for club not found.
            # Display the club's summary page with competitions.
            return render_template("welcome.html", club=club, competitions=competitions)
        except ValueError:
            # Inform the user if the email doesn't match any club.
            flash("Sorry, that email wasn't found.")
            return redirect(url_for("index"))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        """
        Route to book a club for a competition.
        Retrieves the club and competition details from the list based on URL parameters.
        """
        # Find the club and competition by name from the URL parameters.
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        
        # Check if both club and competition are found.
        if foundClub and foundCompetition:
            # Render the booking template with the found club and competition.
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            # Flash error message and redirect to welcome page if not found.
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        """
        Route to handle the purchase of places for a competition.
        Extracts competition and club information from the form data.
        """
        # Retrieve the selected competition and club from the form data.
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        
        # Convert the requested number of places from form data to an integer.
        placesRequired = int(request.form['places'])
        
        # Subtract the requested number of places from the competition's available places.
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        
        # Flash a success message.
        flash('Great-booking complete!')
        
        # Render the welcome template with the updated details.
        return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display. This comment indicates a future feature for displaying club points.

    @app.route('/logout')
    def logout():
        """
        Route to log out the user.
        Redirects the user to the index page.
        """
        # Redirect to the index page, effectively logging the user out.
        return redirect(url_for('index'))


    # Placeholder for additional functionality or routes

    return app
