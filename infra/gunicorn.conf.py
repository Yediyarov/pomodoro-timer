import os
from dotenv import load_dotenv

# Load environment variables from the appropriate .env file
env = os.getenv('ENV', 'local')
load_dotenv(f'.{env}.env')

# Binding
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')

# Worker Settings
workers = os.getenv('GUNICORN_WORKERS', 4)
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'uvicorn.workers.UvicornWorker')
worker_connections = os.getenv('GUNICORN_WORKER_CONNECTIONS', 1000)

# Process naming
proc_name = os.getenv('GUNICORN_PROC_NAME', 'pomodoro-api')

# Development settings
reload = env != 'prod'  # Auto-reload in non-prod environments



