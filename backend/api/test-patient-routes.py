import json
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from patient_routes import patient_bp

class TestPatientRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        self.app = Flask(__name__)
        self.app.register_blueprint(patient_bp)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_get_conversations_success(self):
        """Test successful retrieval of patient conversations."""
        # Mock data that would be returned from the database
        mock_conversations = [
            (1, '2023-01-01 10:00:00', 101, 'How do I manage my medication?', '2023-01-01 10:01:00'),
            (2, '2023-01-02 11:00:00', 102, 'What are the side effects?', '2023-01-02 11:01:00')
        ]
        
        # Set up the mock for database connection
        with patch('patient_routes.get_db_connection') as mock_get_db:
            # Configure the mock connection and cursor
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_get_db.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Set up the mock cursor to return our test data
            mock_cursor.fetchall.return_value = mock_conversations
            
            # Make the GET request to our endpoint
            response = self.client.get('/conversations/1')
            
            # Assert the response is as expected
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Verify the correct data was returned
            self.assertEqual(len(data['data']), 2)
            self.assertEqual(data['data'][0]['conversation_id'], 1)
            self.assertEqual(data['data'][1]['first_query_question'], 'What are the side effects?')
            
            # Verify our database was called correctly
            mock_cursor.execute.assert_called_once()
            self.assertIn('patient_id = %s', mock_cursor.execute.call_args[0][0])
            self.assertEqual(mock_cursor.execute.call_args[0][1], (1,))

    def test_get_conversations_db_error(self):
        """Test error handling when database throws an exception."""
        with patch('patient_routes.get_db_connection') as mock_get_db:
            # Configure the mock to raise an exception
            mock_get_db.side_effect = Exception("Database connection error")
            
            # Make the GET request
            response = self.client.get('/conversations/1')
            
            # Assert the response indicates failure
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn("Database connection error", data['error'])

    def test_add_query_success(self):
        """Test successful addition of a query to an existing conversation."""
        with patch('patient_routes.get_db_connection') as mock_get_db:
            # Configure the mock connection and cursor
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_get_db.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Make the POST request with json data
            response = self.client.post(
                '/conversations/1/queries',
                data=json.dumps({'question': 'How often should I take this medication?'}),
                content_type='application/json'
            )
            
            # Assert the response is as expected
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Verify database was called correctly
            mock_cursor.execute.assert_called_once()
            self.assertIn('INSERT INTO queries', mock_cursor.execute.call_args[0][0])
            self.assertEqual(
                mock_cursor.execute.call_args[0][1],
                (1, 'How often should I take this medication?', 1)
            )
            mock_conn.commit.assert_called_once()

    def test_add_query_missing_data(self):
        """Test error handling when required data is missing."""
        with patch('patient_routes.get_db_connection'):
            # Make the POST request without question data
            response = self.client.post(
                '/conversations/1/queries',
                data=json.dumps({}),
                content_type='application/json'
            )
            
            # Assert the response indicates failure
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn("Question is required", data['error'])

    def test_create_conversation_and_query_success(self):
        """Test successful creation of a conversation with initial query."""
        with patch('patient_routes.get_db_connection') as mock_get_db:
            # Configure the mock connection and cursor
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_get_db.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Set up the cursor to return a conversation ID
            mock_cursor.lastrowid = 5
            
            # Make the POST request with json data
            response = self.client.post(
                '/conversations',
                data=json.dumps({
                    'patient_id': 123,
                    'question': 'Is this medication safe during pregnancy?'
                }),
                content_type='application/json'
            )
            
            # Assert the response is as expected
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Verify database was called correctly for both inserts
            self.assertEqual(mock_cursor.execute.call_count, 2)
            
            # Check first call (create conversation)
            first_call = mock_cursor.execute.call_args_list[0]
            self.assertIn('INSERT INTO conversations', first_call[0][0])
            self.assertEqual(first_call[0][1], (123,))
            
            # Check second call (add query)
            second_call = mock_cursor.execute.call_args_list[1]
            self.assertIn('INSERT INTO queries', second_call[0][0])
            self.assertEqual(second_call[0][1], (5, 123, 'Is this medication safe during pregnancy?'))
            
            # Verify commits were called
            self.assertEqual(mock_conn.commit.call_count, 2)

    def test_create_conversation_missing_data(self):
        """Test error handling when required data is missing for conversation creation."""
        with patch('patient_routes.get_db_connection'):
            # Test missing patient_id
            response1 = self.client.post(
                '/conversations',
                data=json.dumps({'question': 'Test question'}),
                content_type='application/json'
            )
            self.assertEqual(response1.status_code, 400)
            
            # Test missing question
            response2 = self.client.post(
                '/conversations',
                data=json.dumps({'patient_id': 123}),
                content_type='application/json'
            )
            self.assertEqual(response2.status_code, 400)
            
            # Test empty request
            response3 = self.client.post(
                '/conversations',
                data=json.dumps({}),
                content_type='application/json'
            )
            self.assertEqual(response3.status_code, 400)

if __name__ == '__main__':
    unittest.main()
