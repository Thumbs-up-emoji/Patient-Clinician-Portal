from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection
from api.ai_handler import handle_ai

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/conversations/<int:patient_id>', methods=['GET'])
def get_conversations(patient_id):
    """Fetch all conversations for a patient, along with the earliest query in each."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            c.id AS conversation_id,
            c.created_at AS conversation_created_at,
            q.id AS first_query_id,
            q.question AS first_query_question,
            q.created_at AS first_query_created_at
        FROM
            conversations c
        LEFT JOIN
            queries q ON c.id = q.conversation_id
        WHERE
            c.patient_id = %s
        AND q.id = (SELECT MIN(id) FROM queries WHERE conversation_id = c.id)
        ORDER BY
            c.created_at DESC;
        """
        cursor.execute(query, (patient_id,))
        conversations = cursor.fetchall()

        conn.close()

        # Convert the results to a list of dictionaries
        conversation_list = []
        for row in conversations:
            conversation_dict = {
                'conversation_id': row[0],
                'conversation_created_at': row[1],
                'first_query_id': row[2],
                'first_query_question': row[3],
                'first_query_created_at': row[4]
            }
            conversation_list.append(conversation_dict)

        return jsonify({"success": True, "data": conversation_list})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@patient_bp.route('/conversations/<int:conversation_id>/queries', methods=['POST'])
def add_query(conversation_id):
    """Add a new query to an existing conversation."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        data = request.get_json()
        question = data.get('question')
        image_url = data.get('image_url')

        if question is None:
            return jsonify({"success": False, "error": "Question is required"}), 400

        # Fetch conversation history
        conversation_history = get_conversation_history(conversation_id)

        query = """
        INSERT INTO queries (conversation_id, patient_id, question, image_url)
        SELECT %s, c.patient_id, %s, %s
        FROM conversations c
        WHERE c.id = %s;
        """
        values = (conversation_id, question, image_url, conversation_id)

        cursor.execute(query, values)
        conn.commit()

        query_id = cursor.lastrowid

        # Get AI response
        ai_response = handle_ai(question, image_url, conversation_history)

        if ai_response:
            # Store AI response
            success, message = store_ai_response(query_id, ai_response)
            if not success:
                return jsonify({"success": False, "error": message}), 500
        else:
            return jsonify({"success": False, "error": "Failed to get AI response"}), 500

        conn.close()
        return jsonify({"success": True, "message": "Query added successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@patient_bp.route('/conversations', methods=['POST'])
def create_conversation_and_query():
    """Create a new conversation and add a new query to it."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        data = request.get_json()
        patient_id = data.get('patient_id')
        question = data.get('question')
        image_url = data.get('image_url')

        if patient_id is None or question is None:
            return jsonify({"success": False, "error": "Patient ID and question are required"}), 400

        # Create a new conversation
        query_conversation = """
        INSERT INTO conversations (patient_id)
        VALUES (%s);
        """
        values_conversation = (patient_id,)
        cursor.execute(query_conversation, values_conversation)
        conn.commit()

        # Get the ID of the newly created conversation
        conversation_id = cursor.lastrowid

        # Fetch conversation history (empty for new conversation)
        conversation_history = ""

        # Add the new query to the conversation
        query_add_query = """
        INSERT INTO queries (conversation_id, patient_id, question, image_url)
        VALUES (%s, %s, %s, %s);
        """
        values_add_query = (conversation_id, patient_id, question, image_url)
        cursor.execute(query_add_query, values_add_query)
        conn.commit()

        query_id = cursor.lastrowid

       # Get AI response
        ai_response = handle_ai(question, image_url, conversation_history)

        if ai_response:
            # Store AI response
            success, message = store_ai_response(query_id, ai_response)
            if not success:
                return jsonify({"success": False, "error": message}), 500
        else:
            return jsonify({"success": False, "error": "Failed to get AI response"}), 500

        conn.close()
        return jsonify({"success": True, "message": "Conversation and query added successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def get_conversation_history(conversation_id):
    """Fetches the conversation history for a given conversation."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            q.question,
            COALESCE(r.clinician_response, r.ai_response) AS response
        FROM
            queries q
        LEFT JOIN
            responses r ON q.id = r.query_id
        WHERE
            q.conversation_id = %s
        ORDER BY
            q.created_at ASC;
        """
        cursor.execute(query, (conversation_id,))
        history = cursor.fetchall()
        conn.close()

        # Format the conversation history into a string
        formatted_history = ""
        for question, response in history:
            formatted_history += f"Patient: {question}\nResponse: {response}\n"

        return formatted_history

    except Exception as e:
        print(f"Error fetching conversation history: {e}")
        return ""

def store_ai_response(query_id, ai_response):
    """Stores the AI response to a patient query."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO responses (query_id, ai_response, clinician_response, status)
        VALUES (%s, %s, NULL, 'unreviewed');
        """
        values = (query_id, ai_response)

        cursor.execute(query, values)
        conn.commit()

        conn.close()
        return True, "AI response added successfully"

    except Exception as e:
        return False, str(e)

