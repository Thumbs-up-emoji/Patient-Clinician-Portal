from flask import Blueprint, request, jsonify
from backend.config.db_config import get_db_connection

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
        ORDER BY r.created_at DESC
        """
        
        cursor.execute(query)
        reviews = cursor.fetchall()
        
        conn.close()
        return jsonify({"success": True, "data": reviews})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500