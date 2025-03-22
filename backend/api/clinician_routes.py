from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection

clinician_bp = Blueprint('clinician', __name__)

@clinician_bp.route('/pending-reviews', methods=['GET'])
def get_pending_reviews():
    """Get all responses pending review"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT r.id, r.ai_response, q.question, r.created_at, u.name as patient_name 
        FROM responses r
        JOIN queries q ON r.query_id = q.id
        JOIN users u ON q.patient_id = u.id
        WHERE r.status = 'unreviewed'
        ORDER BY r.created_at ASC
        """
        
        cursor.execute(query)
        reviews = cursor.fetchall()
        
        conn.close()
        return jsonify({"success": True, "data": reviews})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@clinician_bp.route('/responses/<int:response_id>', methods=['PUT'])
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