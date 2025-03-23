import json
from datetime import datetime
import pytest

# We're using the fixtures from conftest.py

def test_update_response_success(client, mock_db_connection):
    """Test successful response update"""
    # Define test data
    response_id = 1
    test_data = {'clinician_response': 'Updated response text'}
    
    # Make the request
    response = client.put(
        f'/responses/edit/{response_id}',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify DB operations
    mock_cursor = mock_db_connection['cursor']
    mock_conn = mock_db_connection['connection']
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

def test_update_response_missing_data(client, mock_db_connection):
    """Test response update with missing data"""
    # Make request with empty data
    response = client.put(
        '/responses/edit/1',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    # Assert response
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'clinician_response is required' in data['error']

def test_update_response_db_error(client, mock_db_connection):
    """Test response update with database error"""
    # Setup mock to raise exception
    mock_cursor = mock_db_connection['cursor']
    mock_cursor.execute.side_effect = Exception("Database error")
    
    # Make the request
    response = client.put(
        '/responses/edit/1',
        data=json.dumps({'clinician_response': 'test'}),
        content_type='application/json'
    )
    
    # Assert response
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'Database error' in data['error']

def test_verify_response_success(client, mock_db_connection):
    """Test successful response verification"""
    # Make request
    response = client.put('/responses/verify/1')
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    
    # Verify DB operations
    mock_cursor = mock_db_connection['cursor']
    mock_conn = mock_db_connection['connection']
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

def test_get_conversation_success(client, mock_db_connection):
    """Test successfully getting a conversation"""
    # Setup mock with sample data
    mock_cursor = mock_db_connection['cursor']
    
    # Sample data that would be returned from the database
    sample_data = [
        (1, "How are you feeling?", datetime.now(), 
         10, "I'm the AI response", "I'm the clinician response", 
         "reviewed", datetime.now())
    ]
    mock_cursor.fetchall.return_value = sample_data
    
    # Make request
    response = client.get('/conversation/1')
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 1
    
    # Check data structure
    conversation_item = data['data'][0]
    assert conversation_item['query_id'] == 1
    assert conversation_item['question'] == "How are you feeling?"
    assert conversation_item['response_id'] == 10

def test_get_conversation_empty(client, mock_db_connection):
    """Test getting a conversation that returns no data"""
    # Setup mock to return empty list
    mock_cursor = mock_db_connection['cursor']
    mock_cursor.fetchall.return_value = []
    
    # Make request
    response = client.get('/conversation/999')  # Non-existent ID
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 0

def test_get_pending_conversations_success(client, mock_db_connection):
    """Test successfully getting pending conversations"""
    # Setup mock
    mock_cursor = mock_db_connection['cursor']
    
    # Sample data
    sample_data = [
        (1, datetime.now(), datetime.now()),
        (2, datetime.now(), datetime.now())
    ]
    mock_cursor.fetchall.return_value = sample_data
    
    # Make request
    response = client.get('/pending-conversations')
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 2
    
    # Check data structure
    assert data['data'][0]['conversation_id'] == 1
    assert data['data'][1]['conversation_id'] == 2

def test_get_pending_conversations_empty(client, mock_db_connection):
    """Test getting pending conversations when none exist"""
    # Setup mock to return empty list
    mock_cursor = mock_db_connection['cursor']
    mock_cursor.fetchall.return_value = []
    
    # Make request
    response = client.get('/pending-conversations')
    
    # Assert response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['data']) == 0
