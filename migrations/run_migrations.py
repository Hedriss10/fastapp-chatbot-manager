import logging
import os
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# Carrega .env da raiz
load_dotenv(dotenv_path=BASE_DIR / ".env")

DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
if not DATABASE_URI:
    raise ValueError(
        "❌ Variável SQLALCHEMY_DATABASE_URI não encontrada no .env"
    )


def run_migrations_online():
    print("🔧 Iniciando migrações...")

    config = Config(str(BASE_DIR / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", DATABASE_URI)
    config.set_main_option("script_location", str(BASE_DIR / "migrations"))

    logging.basicConfig()
    logging.getLogger("alembic").setLevel(logging.INFO)

    print("✅ Aplicando migrations...")
    command.upgrade(config, "head")
    print("✅ Migrações aplicadas com sucesso!")


if __name__ == "__main__":
    run_migrations_online()
