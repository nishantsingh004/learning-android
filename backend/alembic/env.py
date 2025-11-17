from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.session import Base
from app.models import tables
config = context.config
db_user = os.getenv("POSTGRES_USER", "postgres")
db_pass = os.getenv("POSTGRES_PASSWORD", "yellowbus")
db_name = os.getenv("POSTGRES_DB", "kifagri")
db_host = os.getenv("POSTGRES_HOST", "49.205.172.128")
db_port = os.getenv("POSTGRES_PORT", "5432")
config.set_main_option("sqlalchemy.url", f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
