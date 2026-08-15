# User Directory App

A small full-stack user directory built with React, FastAPI, SQLAlchemy, and PostgreSQL. The complete application runs using Docker Compose.

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- TanStack Query

### Backend

- FastAPI
- SQLAlchemy 2
- PostgreSQL
- uv

### Infrastructure

- Docker
- Docker Compose

## Project Structure

```text
user-directory-app/
├── backend/
│   ├── db.py
│   ├── main.py
│   ├── model.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Running the Application

### Requirements

Only Docker and Docker Compose are required.

### Start all services

Clone the repository and run:

```bash
docker compose up --build
```

Docker Compose starts:

- PostgreSQL database
- FastAPI backend
- React frontend

No additional setup or database initialization is required.

### Application URLs

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

Click **Fetch Users** in the frontend to load user data from PostgreSQL.

### Stop the application

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```

## API

### `GET /users`

Returns all users stored in the database.

Example response:

```json
[
  {
    "id": 1,
    "name": "Zakarea Alkashef",
    "email": "zak@example.com",
    "created_at": "2026-08-15T09:00:00Z",
    "updated_at": "2026-08-15T09:00:00Z"
  }
]
```

## Architecture

The frontend sends an HTTP request to FastAPI. FastAPI uses a SQLAlchemy session to query PostgreSQL and returns the user records as JSON. TanStack Query manages the frontend request, loading state, error state, and cached data.

PostgreSQL data is persisted in a Docker volume. The backend waits for the database health check before starting.