from flask import Blueprint, request, jsonify
from api.config.db_config import get_db_connection
from .ai_handler import handle_ai

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/conversations/<int:patient_id>', methods=['GET'])
def get_conversations(patient_id):
    """Fetch all conversations for a patient, along with the earliest query in each."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Modified query to handle empty conversations
        query = """
        SELECT
            c.id AS conversation_id,
            c.created_at AS conversation_created_at,
            q.id AS first_query_id,
            q.question AS first_query_question,
            q.created_at AS first_query_created_at
        FROM
            conversations c
        LEFT JOIN (
            SELECT 
                conversation_id, 
                MIN(id) as min_id
            FROM 
                queries
            GROUP BY 
                conversation_id
        ) as min_q ON c.id = min_q.conversation_id
        LEFT JOIN
            queries q ON min_q.min_id = q.id
        WHERE
            c.patient_id = %s
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
                'conversation_id': row['conversation_id'],
                'conversation_created_at': row['conversation_created_at'],
                'first_query_id': row['first_query_id'],
                'first_query_question': row['first_query_question'],
                'first_query_created_at': row['first_query_created_at']
            }
            conversation_list.append(conversation_dict)

        return jsonify({"success": True, "data": conversation_list})

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        error_message = f"{type(e).__name__}: {str(e)}"
        print(f"Error in get_conversations: {error_message}")
        print(f"Traceback: {error_traceback}")
        return jsonify({"success": False, "error": error_message, "traceback": error_traceback}), 500

@patient_bp.route('/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get all queries and responses for a conversation."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            q.id AS query_id,
            q.question,
            q.created_at AS query_created_at,
            r.id AS response_id,
            r.ai_response,
            r.clinician_response,
            r.status,
            r.created_at AS response_created_at
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
        conversation = cursor.fetchall()
        if not conversation:
            return jsonify({"success": True, "data": [], "message": "No queries found for this conversation"}), 200
        conn.close()

        # Convert the results to a list of dictionaries
        conversation_list = []
        for row in conversation:
            query_dict = {
                'query_id': row['query_id'],
                'question': row['question'],
                'query_created_at': row['query_created_at'],
                'response_id': row['response_id'],
                'response': row['ai_response'],
                'clinician_response': row['clinician_response'],
                'status': row['status'],
                'response_created_at': row['response_created_at']
            }
            conversation_list.append(query_dict)

        return jsonify({"success": True, "data": conversation_list})

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  # Shows full stack trace
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
            # Store AI response using the SAME connection
            query = """
            INSERT INTO responses (query_id, ai_response, clinician_response, status)
            VALUES (%s, %s, NULL, 'unreviewed');
            """
            print(1)
            values = (query_id, ai_response)
            print(2)
            cursor.execute(query, values)
            print(3)
            conn.commit()
            print(4)
        else:
            conn.close()
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
        return jsonify({
            "success": True, 
            "message": "Conversation and query added successfully",
            "conversation_id": conversation_id
        }), 201

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

