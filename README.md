# Gudlift Registration

## Table of Contents
1. [Why](#1-why)
2. [Getting Started](#2-getting-started)
3. [Installation](#3-installation)
4. [Current Setup](#4-current-setup)
5. [Testing](#5-testing)
6. [Coverage Reporting](#6-coverage-reporting)
7. [Performance Testing with Locust](#7-performance-testing-with-locust)
8. [Running the Local Flask Server](#8-running-the-local-flask-server)

## 1. Why

This project serves as a Proof of Concept (POC) to demonstrate a lightweight version of our competition booking platform. The goal is to keep the implementation minimalistic, focusing on core functionalities while iterating based on user feedback.

## 2. Getting Started

### Technologies Used

- **Python (v3.x+):** The primary programming language for the project.
- **Flask:** A micro web framework for Python. Unlike Django, which provides many out-of-the-box features, Flask allows for more granular control and minimalism. [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- **Virtual Environment:** Ensures package installations do not interfere with the system's Python environment. [Virtual Environment Installation](https://virtualenv.pypa.io/en/stable/installation.html). Before proceeding, please ensure it is installed globally.

## 3. Installation

Follow these steps to set up the project locally:

1. **Set Up Virtual Environment:** In the project directory, execute `virtualenv .` to create a Python virtual environment.
2. **Activate Virtual Environment:** Use `source bin/activate` or `source env/Scripts/activate` to activate the virtual environment. Your command prompt should now reflect the environment's name. Use `deactivate` to exit.
3. **Install Dependencies:** Run `pip install -r requirements.txt` to install necessary packages in one go. If you add a new package, update `requirements.txt` with `pip freeze > requirements.txt`.
4. **Set Environment Variable:** Flask requires setting an environment variable to the main application file, typically `server.py`. Refer to [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for details.
5. **Run the Application:** Execute `flask run` or `python -m flask run` to start the app. Your browser should be able to access it through the provided address.

## 4. Current Setup

The application utilizes JSON files as a temporary data store to avoid database dependencies until necessary. Important files include:
- `competitions.json` - A list of competitions.
- `clubs.json` - Information on clubs, including accepted email addresses for login.

## 5. Testing

Testing is conducted with `pytest`:

- Ensure the virtual environment is active.
- Install `pytest` with `pip install pytest`.
- Run tests using `python -m pytest`.
- For HTML reports, `pytest --html=test/test_report.html`.

## 6. Coverage Reporting

We use the `coverage` tool for test coverage analysis:

- Activate the virtual environment.
- Install `coverage` with `pip install coverage`.
- Execute tests with `coverage run -m pytest`.
- View the report with `coverage report`. For detailed insights, including missing lines, add `-m`.
- For an HTML report, `coverage html`.

## 7. Performance Testing with Locust

`Locust` is used for load testing:

- Install `locust` (`pip install locust`).
- Start the application and then `locust`.
- Visit `http://localhost:8089` for the Locust interface.
- Configure test parameters: 6 users, 1 ramp-up and target `http://localhost:5000`.
- Begin the test and monitor performance.

## 8. Running the Local Flask Server

Steps to run the Flask application locally:

- **Activate Virtual Environment**
- **Set the FLASK_APP Environment Variable:** Use `export FLASK_APP=server:create_app` (Linux/MacOS) or `set FLASK_APP=server:create_app` (Windows).
- **Run the Flask Application:** Start the server with `Flask run`.
