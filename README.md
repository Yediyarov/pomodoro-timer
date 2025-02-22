# Pomodoro Timer API

A FastAPI-based backend service for managing Pomodoro tasks with Redis caching and PostgreSQL storage.

## Features

- Task Management (CRUD operations)
- Category-based Task Organization
- Redis Caching for Performance
- PostgreSQL Database Storage
- Docker Containerization
- Environment-based Configuration

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- Alembic (Migrations)
- Redis
- PostgreSQL
- Poetry (Package Management)
- Docker & Docker Compose

## Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- Poetry for dependency management

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
```

2. Install dependencies:


```poetry install```

3. Create environment file:
   - Copy `.env.example` to `.local.env` for local development
   - Adjust the values according to your setup

## Running the Application

### Local Development

1. Start the services:

```make docker-up ENV=local```

2. Apply database migrations:

```make migrate-apply ENV=local```

3. Run the application:

```make run ENV=local```

The API will be available at `http://localhost:8000`

### Production

1. Create `.prod.env` with production settings
2. Run:

```make docker-up ENV=prod```
```make migrate-apply ENV=prod```
```make run ENV=prod```

## API Endpoints

- `GET /tasks/all` - Get all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/category/{category_name}` - Get tasks by category

## Project Structure

```
pomodoro-timer/
├── alembic/              # Database migrations
├── cache/                # Redis cache implementation
├── database/             # Database models and connection
├── repository/           # Data access layer
├── schema/               # Pydantic models
├── service/              # Business logic
├── scripts/              # Utility scripts
└── docker-compose.yml    # Docker services configuration
```

## Development

### Creating New Migrations

```make migrate-create MIGRATION="description_of_changes"```

### Adding Dependencies

```make install LIBRARY=package_name```

### Running Tests

```poetry run pytest```

## Environment Variables

Key environment variables (see `.env.example` for full list):
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `POSTGRES_PORT` - Database port
- `CACHE_HOST` - Redis host
- `CACHE_PORT` - Redis port

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)

