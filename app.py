from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.user import User
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app) # initialize SQLAlchemy and setup Flask-Migrate
    register_resources(app) # sets up resource routing

    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    """Add resource routing by passing in the URL. 
    This will route directly to our resources using HTTP methods"""

    api.add_resource(RecipeListResource, "/recipes")
    api.add_resource(RecipeResource, "/recipes/<int:recipe_id>")
    api.add_resource(RecipePublishResource, "/recipes/<int:recipe_id>/publish")

if __name__ == "__main__":
    app = create_app() # Creates the Flask app
    app.run() # Starts the application






