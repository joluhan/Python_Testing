# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    For testing, this project uses `pytest`:

    - Make sure your virtual environment is active (`source bin/activate`).
    - Install `pytest` by running `pip install pytest`.
    - To run your tests, use the command `python -m pytest` from the root of the project directory.

6. Coverage Reporting

To measure the coverage of the tests, we use the `coverage` tool. This helps us understand which parts of our code are not being tested and might require additional tests.

- First, ensure your virtual environment is activated (`source bin/activate`).
- Install `coverage` by running `pip install coverage`.
- To start measuring coverage, run your tests with coverage by using the command `coverage run -m pytest`.
- After the tests have finished, you can view the report by running `coverage report`.
- For a more detailed report that includes missing lines, run `coverage report -m`.
- If you prefer to view this in a browser as an HTML page, run `coverage html`. This will generate a `htmlcov` directory with HTML files you can open in your browser.

7. Performance Testing with Locust

To ensure the application can handle the expected load, we use `locust` for performance testing.

**How use locust:**

- First, install `locust` by running `pip install locust`.
- With the Flask application running, start Locust using `locust`.
- Open a browser and navigate to `http://localhost:8089` to access the Locust web interface.

When the Locust web interface is open, set the following parameters:
- Number of users: 6 (to simulate 6 concurrent users)
- Ramp Up: 1 (users will be started per second)
- Host: Enter the local address of your Flask application, usually `http://localhost:5000`.

- Click `Start Swarming` to begin the test.
- Observe the results to ensure your application performs well under the expected load of 6 concurrent users.

8. Running the Local Flask Server

To run the Gudlift Registration Flask application locally, follow these steps:

- Activate Virtual Environment
- Set the FLASK_APP Environment Variable:

   Flask uses the `FLASK_APP` environment variable to locate the application. Set this variable to your main application file (usually `server.py`):

   - On Linux/MacOS:`export FLASK_APP=server.py`
   - On Windows:`set FLASK_APP=server.py`

- Run the Flask Application**

   With the environment variable set, you can start the Flask development server with the following command:`Flask run`
