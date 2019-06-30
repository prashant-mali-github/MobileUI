from flask_script import Manager
from models.create_models import CreateUsersCommand
from flask.cli import FlaskGroup
from flask_migrate import MigrateCommand
from app import create_app,db

cli = FlaskGroup(create_app=create_app)
manager = Manager(create_app)


manager.add_command('db',MigrateCommand)
manager.add_command('create_tables', CreateUsersCommand)

if __name__ == "__main__":
    manager.run()