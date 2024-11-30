from flask import Flask
from .dao.database import engine
from .templates import models
from .controllers.item_controller import item_bp

# Initialize Flask app
app = Flask(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Import controllers
def register_blueprints(app):
    app.register_blueprint(item_bp)

register_blueprints(app)
