from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection

clinician_bp = Blueprint('clinician', __name__)

@clinician_bp.route('/pending-reviews', methods=['GET'])
def get_pending_reviews():
    """Get all responses pending review, along with conversation ID and the first unreviewed query."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            r.id,
            q.question,
            c.id AS conversation_id
        FROM
            responses r
        JOIN
            queries q ON r.query_id = q.id
        JOIN
            conversations c ON q.conversation_id = c.id
        WHERE
            r.status = 'unreviewed'
        ORDER BY
            c.created_at ASC, r.created_at ASC
        LIMIT 1;
        """

        cursor.execute(query)
        review = cursor.fetchall()

        conn.close()
        if review:
            # Convert the review tuple to a dictionary for better readability
            review_dict = {
                'id': review[0],
                'question': review[1],
                'conversation_id': review[2]
            }
            return jsonify({"success": True, "data": review_dict})
        else:
            return jsonify({"success": True, "data": None}) # No pending reviews

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@clinician_bp.route('/responses/edit/<int:response_id>', methods=['PUT'])
def update_response(response_id):
    """Update a response."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        data = request.get_json()
        clinician_response = data.get('clinician_response')

        if clinician_response is None:
            return jsonify({"success": False, "error": "clinician_response is required"}), 400

        query = """
            UPDATE responses
            SET clinician_response = %s, status = 'reviewed', reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
        values = (clinician_response, response_id)

        cursor.execute(query, values)
        conn.commit()

        conn.close()
        return jsonify({"success": True, "message": "Response updated successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@clinician_bp.route('/responses/verify/<int:response_id>', methods=['PUT'])
def verify_response(response_id):
    """Verify a response by setting its status to 'reviewed'."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE responses
            SET status = 'reviewed'
            WHERE id = %s
            """
        values = (response_id,)

        cursor.execute(query, values)
        conn.commit()

        conn.close()
        return jsonify({"success": True, "message": "Response verified successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@clinician_bp.route('/conversation/<int:conversation_id>', methods=['GET'])
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
            r.response,
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

        conn.close()

        # Convert the results to a list of dictionaries
        conversation_list = []
        for row in conversation:
            query_dict = {
                'query_id': row[0],
                'question': row[1],
                'query_created_at': row[2],
                'response_id': row[3],
                'response': row[4],
                'clinician_response': row[5],
                'status': row[6],
                'response_created_at': row[7]
            }
            conversation_list.append(query_dict)

        return jsonify({"success": True, "data": conversation_list})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500