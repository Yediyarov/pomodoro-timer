# Pomodoro Timer API

A FastAPI-based backend service for managing Pomodoro tasks with Redis caching, PostgreSQL storage, and Google OAuth integration.

## Features

- Task Management (CRUD operations)
- Category-based Task Organization
- Redis Caching for Performance
- PostgreSQL Database Storage
- Google OAuth Authentication
- JWT-based Authorization
- Docker Containerization
- Environment-based Configuration

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy (with asyncpg)
- Alembic (Migrations)
- Redis
- PostgreSQL
- Poetry (Package Management)
- Docker & Docker Compose
- pytest (Testing)

## Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose
- Poetry for dependency management

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
```

2. Install dependencies:

```bash
poetry install
```

3. Create environment file:
   - Copy `.env.example` to `.local.env` for local development
   - Adjust the values according to your setup

## Environment Variables

Key environment variables (see `.env.example` for full list):
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `POSTGRES_PORT` - Database port
- `CACHE_HOST` - Redis host
- `CACHE_PORT` - Redis port
- `JWT_SECRET` - Secret key for JWT tokens
- `JWT_ALGORITHM` - Algorithm for JWT (default: HS256)
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_SECRET_KEY` - Google OAuth secret key
- `GOOGLE_REDIRECT_URI` - Google OAuth redirect URI

## Running the Application

### Local Development

1. Start the services:

```bash
make docker-up ENV=local
```

2. Apply database migrations:

```bash
make alembic-upgrade
```

3. Run the application:

```bash
make run ENV=local
```

The API will be available at `http://localhost:8000`

### Production

1. Create `.prod.env` with production settings
2. Run:

```bash
make docker-up ENV=prod
make migrate-apply ENV=prod
make run ENV=prod
```


## API Endpoints

### Tasks
- `GET /tasks/all` - Get all tasks
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/category/{category_name}` - Get tasks by category

### Authentication
- `POST /auth/login` - User login
- `GET /auth/login/google` - Google OAuth login
- `GET /auth/google` - Google OAuth callback

### User Management
- `POST /user` - Register new user

## Project Structure

```bash
├── app/
│ ├── infrastructure/ # Core infrastructure components
│ │ ├── cache/ # Redis implementation
│ │ └── database/ # Database configuration
│ ├── tasks/ # Task management
│ │ ├── handlers/ # API endpoints
│ │ ├── models/ # Database models
│ │ ├── repository/ # Data access layer
│ │ ├── schema/ # Pydantic models
│ │ └── service/ # Business logic
│ └── users/ # User management
│ ├── auth/ # Authentication
│ └── user_profile/ # User profiles
├── tests/ # Test suite
├── alembic/ # Database migrations
└── docker-compose.yml # Docker services configuration
```

## Development

### Creating New Migrations

```bash
make migrate-create MIGRATION="description_of_changes"
```

### Adding Dependencies

```bash
make install LIBRARY=package_name
```

### Running Tests

```bash
poetry run pytest
```


## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)