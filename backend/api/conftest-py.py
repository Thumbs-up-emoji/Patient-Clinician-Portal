import pytest
from flask import Flask
from patient_routes import patient_bp

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = Flask(__name__)
    app.register_blueprint(patient_bp)
    app.config['TESTING'] = True
    
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
