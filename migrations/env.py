from logging.config import fileConfig
import sys
import os

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importe seu Base e models para refletir no metadata
from app.db.base import Base
from app.models.users import User
from app.models.employee import Employee
from app.models.product import Products
from app.models.messages import SummaryMessage, MessageFlow
from app.models.block import ScheduleBlock
from app.models.schedule import ScheduleService
from app.models.time_recording import ScheduleEmployee



# Configuração padrão do Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Injeta a DATABASE_URL do .env manualmente
database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
if not database_url:
    raise RuntimeError("DATABASE_URL não encontrada no .env")

config.set_main_option("sqlalchemy.url", database_url)

# Associa o metadata usado no autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações em modo offline (gera SQL sem conexão)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações em modo online (conectado ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# Define qual modo rodar
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
