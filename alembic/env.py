import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.settings import settings
from models import Base  # Import your Base model which includes all your models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = settings.get_db_url
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(settings.get_db_url, echo=settings.DB_ECHO)

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata,
                render_as_batch=True,  # Use this if you need batch mode for SQLite
            )
        )

        async with connection.begin():
            await connection.run_sync(context.run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())