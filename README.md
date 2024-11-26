# CSC450_TaskManagementSystem

1. Backend Service (backend/)
This folder contains everything for the backend, a Flask-based REST API that serves the data for the task manager app.

- backend/app.py
This is the main script for the backend application.
Key Components:
    Flask Setup: We initialize the Flask app and configure it to use SQLite as the database, stored locally.
    Database Models: We define a Task model that represents each task in the database, with attributes like id, title, and completed.
    API Endpoints:
        Supports GET (to list all tasks) and POST (to create a new task).
        Supports PATCH (to update a task's completed status) and DELETE (to delete a task).
    Database Initialization: something like db.create_all() is called to create the database tables when the app first runs.
- backend/requirements.txt
    Contains all the dependencies for the backend application. We specify:
    Flask: The web framework.
    Flask-SQLAlchemy: For handling the SQLite database through SQLAlchemy.
- backend/Dockerfile
    Defines how to build the backend container.
