#!/usr/bin/python3
"""Main module for the Flask web application."""
import os

from flask import Flask
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

# Create a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint for API routes
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close(CXT):
    """Close the database session after each request."""
    storage.close()


@app.errorhandler(404)
def not_found(EXP):
    """Handle 404 errors by returning a JSON response."""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    HOST = os.getenv('HBNB_API_HOST', "0.0.0.0")
    PORT = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
