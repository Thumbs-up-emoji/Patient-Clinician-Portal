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