from flask import Flask
from flask_restx import Api


def create_app():
    from thoughts_backend.api_namespace import api_namespace
    from thoughts_backend.admin_namespace import admin_namespace

    app = Flask(__name__)
    api = Api(app, version='0.1', title='Thoughts Backend API',
              description='A Simple CRUD API')

    from thoughts_backend.db import db, db_config
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.config.update(db_config)
    db.init_app(app)
    app.db = db

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)
    return app
