# Workflow

Workflow is a Django-based web application designed for efficient task and team management. It provides a robust backend to handle users, organize teams, and track tasks through various states of completion.

## Features

- **User Management**: Custom user model allowing registration and authentication using a unique `userid`.
- **Team Organization**: Create teams with a designated team leader and multiple team members.
- **Task Tracking**: Create and assign tasks to teams and specific users.
  - Track progress states: `TODO`, `IN_PROGRESS`, and `DONE`.
  - Set priority levels: `LOW`, `MEDIUM`, and `HIGH`.
  - Assign deadlines to keep projects on schedule.

## Project Structure

The project is structured into distinct Django apps for modularity:
- `users`: Handles the custom User model and authentication logic.
- `teams`: Manages Team creation, leadership, and memberships.
- `tasks`: Core logic for task creation, assignment, and status tracking.
- `workflow`: Main configuration and settings.

## Technology Stack

- **Backend Framework**: Django 6.0
- **Database**: PostgreSQL (via `psycopg2-binary`) / SQLite for local development
- **Server**: Gunicorn
- **Static File Management**: WhiteNoise

## Installation and Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
