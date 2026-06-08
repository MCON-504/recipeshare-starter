# RecipeShare Flask Starter

RecipeShare is a Flask starter app that supports both browser pages and JSON API clients.

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF / WTForms
- python-dotenv
- PostgreSQL (default)
- pytest

## Route Map

### Browser entry points

- `GET /` - home page (`home.html`)
- `GET /auth/register` - registration form
- `GET /auth/login` - login form

### API blueprint (`main_bp`, mounted at `/api`)

- `GET /api/` - API health/message JSON
- `GET /api/recipes` - HTML by default, JSON when `request.is_json` is `True`
- `GET /api/recipes/<id>` - JSON recipe detail (HTML rendering is added in Exercise 1)
- `POST /api/recipes` - create recipe (login required)
- `PATCH /api/recipes/<id>` - update recipe (owner only)
- `DELETE /api/recipes/<id>` - delete recipe (owner only)

### Auth blueprint (`auth_bp`, mounted at `/auth`)

- `GET|POST /auth/register` - dual-mode register route
- `GET|POST /auth/login` - dual-mode login route
- `POST /auth/logout` - logout route (currently returns JSON; becomes dual-mode after completing Exercise 2)

## Project Structure

```text
recipeshare-starter/
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- extensions.py
|   |-- models.py
|   |-- routes.py
|   |-- auth/
|   |   |-- forms.py
|   |   `-- views.py
|   `-- templates/
|       |-- base.html
|       |-- home.html
|       `-- auth/
|           |-- login.html
|           `-- register.html
|-- migrations/
|-- tests/
|-- exercises/
|-- env.example
|-- requirements.txt
|-- run.py
|-- seed.py
|-- EXERCISES_README.md
`-- HOMEWORK_README.md
```

## Setup

### 1) Create and activate a virtual environment

#### Windows (cmd.exe)

```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```cmd
pip install -r requirements.txt
```

### 3) Configure environment variables

Copy `env.example` to `.env` and update values.

Example `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost/recipeshare
SECRET_KEY=change-me
FLASK_APP=run.py
FLASK_ENV=development
```

### 4) Run migrations

This project already includes migration files, so usually you only need:

```cmd
flask db upgrade
```

### 5) (Optional) Seed starter data

```cmd
python seed.py
```

### 6) Run the app

```cmd
python run.py
```

## JSON Usage Notes

Dual-mode routes check `request.is_json`.

- If `request.is_json` is `True`, routes return JSON.
- Otherwise, routes render HTML templates.

For these GET routes, you can force JSON behavior by sending `Content-Type: application/json`:

- `GET /api/recipes`
- `GET /api/recipes/<id>`

## Example Requests

### Register (JSON)

```http
POST /auth/register
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123"
}
```

### Login (JSON)

```http
POST /auth/login
Content-Type: application/json

{
  "username": "alice",
  "password": "password123"
}
```

### Create recipe (JSON, authenticated session required)

```http
POST /api/recipes
Content-Type: application/json

{
  "title": "Tomato Soup",
  "description": "Simple homemade soup.",
  "instructions": "Cook tomatoes, blend, and simmer.",
  "prep_time": 30
}
```

## Tests

Run the test suite:

```cmd
pytest -q
```

## Course Docs and Starters

- `EXERCISES_README.md` - in-class exercise instructions
- `HOMEWORK_README.md` - homework instructions
- `exercises/hw1_views_login_starter.py`
- `exercises/hw2_routes_new_recipe_starter.py`
- `exercises/hw2_recipe_form.html`
- `exercises/recipe_detail.html`
