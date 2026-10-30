# Productivity Notes API

A Flask REST API with session-based authentication. Users can sign up, log in and
manage their own notes. Every notes route is protected, and a user can never see or
change another user's notes.

Built with Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt and a SQLite database.
It is designed to work with the `client-with-sessions` frontend from the lab's client repo.

## Features

- Sign up, log in, log out and a check-session route, using a signed session cookie
- Passwords are hashed with bcrypt and are never returned by the API
- Unique usernames, enforced by both the model and the database
- Full CRUD for notes, owned by the logged-in user
- Paginated notes list
- Seed script with Faker data

## Project structure

```
.
├── app.py                    # app factory: create_app()
├── run.py                    # starts the server on port 5555
├── seed.py                   # resets and seeds example data
├── extension.py              # db, bcrypt and migrate objects
├── config/
│   └── config.py             # development and testing settings
├── models/
│   ├── user.py               # User model and password hashing
│   └── note.py               # Note model, owned by a user
├── services/
│   ├── service.py            # save, fetch, paginate, update and remove helpers
│   └── auth.py               # current_user and the login_required decorator
├── controllers/
│   ├── auth_routes.py        # signup, login, logout, check_session
│   ├── note_routes.py        # notes CRUD
│   └── utils.py              # request helpers
├── migrations/               # Alembic migrations
├── Pipfile
└── Pipfile.lock
```

## Installation

Requires Python 3.12 and [Pipenv](https://pipenv.pypa.io/).

```bash
git clone https://github.com/Patience1m/full-auth-flask-backend.git
cd full-auth-flask-backend

pipenv install
pipenv shell

export FLASK_APP=run.py
flask db upgrade
python seed.py
```

`flask db upgrade` creates the tables from the committed migration, and `python seed.py`
adds example users and notes (safe to re-run). Seeded users are `wanjiru`, `otieno` and
`amina`, all with the password `password123`.

Optionally set your own session secret before running: `export SECRET_KEY="something-long-and-random"`.

## Running the app

```bash
flask run --port 5555
# or
python run.py
```

The API runs at `http://localhost:5555`. Port 5555 matters because the provided client proxies to it.

To use the sessions client, run `npm install` and `npm start` inside `client-with-sessions` while this server is running.

## Authentication

The API uses Flask sessions. A successful signup or login sets a signed cookie, and every
other request sends it back automatically. Routes that need a login return `401` without it.

## Endpoints

### Auth

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|---------|--------|
| `POST` | `/signup` | Create a user and log them in. Body: `username`, `password`, `password_confirmation` | `201` | `422` |
| `POST` | `/login` | Log in. Body: `username`, `password` | `200` | `401` |
| `GET` | `/check_session` | Return the logged-in user, so users stay logged in on refresh | `200` | `401` |
| `DELETE` | `/logout` | Log out | `204` | none |

### Notes (login required)

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|---------|--------|
| `GET` | `/notes?page=1&per_page=5` | List your notes, newest first, paginated | `200` | `401` |
| `GET` | `/notes/<id>` | Show one of your notes | `200` | `401`, `403`, `404` |
| `POST` | `/notes` | Create a note. Body: `title`, `content` | `201` | `401`, `422` |
| `PATCH` | `/notes/<id>` | Update `title` and/or `content` | `200` | `401`, `403`, `404`, `422` |
| `DELETE` | `/notes/<id>` | Delete a note | `204` | `401`, `403`, `404` |

Example paginated response:

```json
{
  "page": 1,
  "per_page": 5,
  "total": 8,
  "pages": 2,
  "notes": [
    { "id": 8, "title": "Plan the week", "content": "...", "created_at": "2026-10-30T10:15:00", "user_id": 1 }
  ]
}
```

`per_page` defaults to 5 and is capped at 50.

## Error format

Errors are always a list, so the frontend can show each message:

```json
{ "errors": ["Username is already taken."] }
```

| Status | Meaning |
|--------|---------|
| `401` | Not logged in, or wrong login details |
| `403` | The note exists but belongs to another user |
| `404` | Note not found |
| `422` | Invalid data, such as a blank title or mismatched passwords |

## Changing the models

If you change a model, generate and apply a new migration:

```bash
flask db migrate -m "describe the change"
flask db upgrade
```
