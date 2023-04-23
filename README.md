Documentation for a Flask and MySQL Social Network Website

Overview:
This project is a web application built using Flask and MySQL. The website is a social network where users can create an account, create news, and view news created by other users. The website also features a simple frontend for easy navigation.

Features:

User account creation and authentication
News creation and viewing
Simple frontend for easy navigation
ORM migrations and SQLAlchemy to work with the database
Unit tests for each endpoint using Postman
Continuous integration with Travis CI
Project stored on GitHub
Technologies:

Python 3.9.7
Flask
MySQL
SQLAlchemy
ORM migrations
Postman
Travis CI
Git
Methodology:
The project was developed using Python 3.x and Flask, a micro web development framework that allows for quick and easy website development. MySQL was used for database management, with SQLAlchemy and ORM migrations being utilized to manage database changes. The project was thoroughly tested using Postman, a popular testing suite for API endpoints. Unit tests were created for each endpoint to ensure proper functionality and prevent potential bugs.

To extend the functionality of the website, additional features could be implemented such as messaging, user profile customization, and improved search capabilities. Additional security measures could also be implemented to protect user data and prevent unauthorized access.
Installation:

Install Python 3.9.7 on your local machine.
Install Flask by running the following command: pip install flask
Install MySQL and create a database for the project.
Install SQLAlchemy by running the following command: pip install sqlalchemy
Install the ORM migrations library by running the following command: pip install flask-migrate
Clone the project from GitHub.
Set up the database by running the following commands:
flask db init
flask db migrate
flask db upgrade
Run the project by running the following command: flask run
Usage:

Navigate to the website using your preferred web browser.
Create an account by clicking on the "Register" button and filling out the registration form.
Log in using your credentials.
Create a news by clicking on the "Create News" button and filling out the news form.
View news created by other users by clicking on the "View News" button.
Testing:

Install Postman on your local machine.
Import the provided Postman collection and environment files.
Run the collection to test each endpoint.
Verify that each test passes.
Continuous Integration:

The project is set up with Travis CI for continuous integration.
Each time a new commit is pushed to GitHub, Travis CI runs the unit tests to verify that everything is working correctly.
If the unit tests pass, the code is deployed to the live server.

