from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection

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

        if question is None:
            return jsonify({"success": False, "error": "Question is required"}), 400

        query = """
        INSERT INTO queries (conversation_id, patient_id, question)
        SELECT %s, c.patient_id, %s
        FROM conversations c
        WHERE c.id = %s;
        """
        values = (conversation_id, question, conversation_id)

        cursor.execute(query, values)
        conn.commit()

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

        # Add the new query to the conversation
        query_add_query = """
        INSERT INTO queries (conversation_id, patient_id, question)
        VALUES (%s, %s, %s);
        """
        values_add_query = (conversation_id, patient_id, question)
        cursor.execute(query_add_query, values_add_query)
        conn.commit()

        conn.close()
        return jsonify({"success": True, "message": "Conversation and query added successfully"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500