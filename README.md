# Task Manager API

A task management REST API built with FastAPI, PostgreSQL, and SQLAlchemy.

## Getting Started

### Prerequisites

- Python 3.10+
- `make` installed on your system

### Running the Server

Start the production server with:

```bash
make run-prod
```

This spins up the FastAPI backend (via `uvicorn`) bound to `0.0.0.0` without
auto-reload, suitable for a production-style run. Once started, the API will
be available at:

```
http://localhost:8000
```

Interactive API docs (Swagger UI) are available at:

```
http://localhost:8000/docs
```
