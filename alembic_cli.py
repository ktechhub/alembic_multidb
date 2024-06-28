# alemibic_cli.py is a script that allows you to run Alembic migrations for multiple databases.
from datetime import datetime
import os
import argparse
from alembic.config import Config
from alembic import command

from dotenv import load_dotenv

load_dotenv()

# Define databases
DATABASES = {"dev", "test", "qa", "prod"}
print(DATABASES)


def generate_db_url(db_name):
    return f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{db_name}"


def create_revision(db_name, config_path, message):
    """Create a new revision for a specific db_name."""
    versions_dir = os.path.join("alembic", "versions", db_name)
    os.makedirs(versions_dir, exist_ok=True)

    config = Config(config_path)
    config.set_main_option("version_locations", versions_dir)
    config.set_main_option(
        "sqlalchemy.url",
        generate_db_url(db_name),
    )
    print(f"revision for {db_name}: {config.get_main_option('sqlalchemy.url')}")
    command.revision(
        config, message=f"{message} on {datetime.now()}", autogenerate=True
    )


def upgrade_head(db_name, config_path):
    """Upgrade to head for a specific db_name."""
    config = Config(config_path)
    config.set_main_option(
        "sqlalchemy.url",
        generate_db_url(db_name),
    )
    config.set_main_option(
        "version_locations", os.path.join("alembic", "versions", db_name)
    )
    print(f"upgrade for {db_name}: {config.get_main_option('sqlalchemy.url')}")
    command.upgrade(config, "head")


def downgrade(db_name, revision, config_path):
    """Downgrade to a specific revision for a customer."""
    config = Config(config_path)
    config.set_main_option("sqlalchemy.url", generate_db_url(db_name))
    config.set_main_option(
        "version_locations", os.path.join("alembic", "versions", db_name)
    )
    print(f"downgrade for {db_name}: {config.get_main_option('sqlalchemy.url')}")
    command.downgrade(config=config, revision=revision)


def migrate_database(db_name, action, config_path, message, revision=None):
    """Run migration for a specific db_name."""
    if action == "revision":
        create_revision(db_name, config_path, message)
    elif action == "upgrade":
        upgrade_head(db_name, config_path)
    elif action == "downgrade" and revision:
        downgrade(db_name, revision, config_path)
    else:
        print(f"Error: Invalid action or missing revision for downgrade.")


def migrate_all(action, config_path, message):
    """Run migrations for all db_names."""
    for db_name in DATABASES:
        migrate_database(db_name, action, config_path, message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Alembic migrations for db_names.")
    parser.add_argument(
        "action",
        choices=["revision", "upgrade", "downgrade"],
        help="Action to perform: 'revision' or 'upgrade', or 'downgrade'",
    )
    parser.add_argument("--db", help="Specify a db_name to run the migration for")
    parser.add_argument(
        "--message", help="Revision message for the migration", default="rev"
    )
    parser.add_argument(
        "--revision",
        help="Specify the revision for downgrade (required for 'downgrade' action)",
    )
    args = parser.parse_args()

    config_path = "./alembic.ini"

    if args.action == "downgrade" and not args.revision:
        print("Error: Missing revision for downgrade.")
        exit(1)

    if args.db:
        if args.db in DATABASES:
            migrate_database(
                args.db, args.action, config_path, args.message, args.revision
            )
        else:
            print(f"Error: Database '{args.db}' not found in the list of databases.")
    else:
        migrate_all(args.action, config_path, args.message)
