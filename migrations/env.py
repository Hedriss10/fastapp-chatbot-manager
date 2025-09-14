import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Caminho raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa Base e models
from app.db.base import Base
from app.models.users import User
from app.models.employee import Employee
from app.models.product import Products
from app.models.messages import SummaryMessage, MessageFlow
from app.models.block import ScheduleBlock
from app.models.schedule import ScheduleService
from app.models.time_recording import ScheduleEmployee

# Config do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("SQLALCHEMY_DATABASE_URI_MIGRATIONS")
if not database_url:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI_MIGRATIONS não encontrada no .env")

config.set_main_option("sqlalchemy.url", database_url)
target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    # if type_ == "table" and name in [
    #     "summary_message", "employees", "products", "schedule", "message_flow",
    #     "products_employees", "block", "schedule_employee"
    # ]:
    #     return False
    return True

def run_migrations_offline():
    """Rodar migrations em modo offline (gera SQL sem conectar)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Rodar migrations em modo sync (psycopg2)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


run_migrations()
