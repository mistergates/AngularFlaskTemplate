from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.api.app import app, db
from src.database import models

migrate = Migrate(app, db)
manager = Manager(app)

# migrations for database model changes
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    '''Creates database and tables'''
    db.create_all()


@manager.command
def drop_db():
    '''Drops the database tables'''
    db.drop_all()


if __name__ == '__main__':
    manager.run()
