import pytest
from flask import Flask
from unittest.mock import patch, MagicMock

# Import the blueprint we want to test
from clinician_routes import clinician_bp

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = Flask(__name__)
    app.register_blueprint(clinician_bp)
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()

@pytest.fixture
def mock_db_connection():
    """Mock the database connection"""
    with patch('clinician_routes.get_db_connection') as mock_get_db:
        # Create mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        yield {
            'connection': mock_conn,
            'cursor': mock_cursor,
            'get_db': mock_get_db
        }
