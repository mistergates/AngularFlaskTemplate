'''Lazy API server runner'''
import os
import argparse

from src.api.app import app, db

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watcher Server')
    parser.add_argument('--create-database', dest='create_database', action='store_true', help='Create the database')
    args = parser.parse_args()

    if args.create_database:
        db_loc = app.config['SQLALCHEMY_DATABASE_URI'].split('sqlite:///')[-1]
        if not os.path.exists(db_loc):
            print('Creating database...')
            db.create_all()

    app.run(host='0.0.0.0', port='8080', debug=True)
