from flask import Blueprint, request, jsonify
from api.config.db_config import get_db_connection
from .ai_handler import handle_ai

admin_bp = Blueprint('admin', __name__)

# For updating existing records:
@admin_bp.route('/fix-empty-responses', methods=['PATCH'])
def fix_empty_responses():
    """Check for queries with NULL or empty AI responses and regenerate them."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find queries that have response entries but NULL or empty ai_response
        query_empty_response = """
        SELECT q.id, q.conversation_id, q.question, q.image_url, r.id as response_id
        FROM queries q
        JOIN responses r ON q.id = r.query_id
        WHERE r.ai_response IS NULL OR r.ai_response = ''
        ORDER BY q.created_at ASC;
        """
        
        cursor.execute(query_empty_response)
        queries_with_empty_responses = cursor.fetchall()
        
        if not queries_with_empty_responses:
            conn.close()
            return jsonify({
                "success": True, 
                "message": "No queries found with empty responses",
                "processed": 0
            }), 200
        
        processed_count = 0
        failed_queries = []
        
        for query_row in queries_with_empty_responses:
            try:
                query_id = query_row['id']
                conversation_id = query_row['conversation_id']
                question = query_row['question']
                image_url = query_row['image_url']
                response_id = query_row['response_id']
                
                # Get conversation history for this query
                conversation_history = get_conversation_history_for_query(conversation_id, query_id)
                
                # Get AI response
                ai_response = handle_ai(question, image_url, conversation_history)
                
                if ai_response:
                    # Update existing response
                    update_response_query = """
                    UPDATE responses 
                    SET ai_response = %s
                    WHERE id = %s;
                    """
                    cursor.execute(update_response_query, (ai_response, response_id))
                    conn.commit()
                    processed_count += 1
                else:
                    failed_queries.append(f"Query ID {query_id}: Failed to get AI response")
                    
            except Exception as e:
                failed_queries.append(f"Query ID {query_row['id']}: {str(e)}")
                continue
        
        conn.close()
        
        response_data = {
            "success": True,
            "message": f"Updated {processed_count} responses successfully",
            "processed": processed_count,
            "total_found": len(queries_with_empty_responses)
        }
        
        if failed_queries:
            response_data["failures"] = failed_queries
        
        return jsonify(response_data), 200
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in fix_empty_responses: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return jsonify({"success": False, "error": str(e)}), 500

# For creating new records:
@admin_bp.route('/fix-missing-responses', methods=['POST'])
def fix_missing_responses():
    """Check for queries without AI responses and generate them."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find queries that don't have any response entry
        query_no_response = """
        SELECT q.id, q.conversation_id, q.question, q.image_url
        FROM queries q
        LEFT JOIN responses r ON q.id = r.query_id
        WHERE r.query_id IS NULL
        ORDER BY q.created_at ASC;
        """
        
        cursor.execute(query_no_response)
        queries_without_responses = cursor.fetchall()
        
        if not queries_without_responses:
            conn.close()
            return jsonify({
                "success": True, 
                "message": "No queries found without responses",
                "processed": 0
            }), 200
        
        processed_count = 0
        failed_queries = []
        
        for query_row in queries_without_responses:
            try:
                query_id = query_row['id']
                conversation_id = query_row['conversation_id']
                question = query_row['question']
                image_url = query_row['image_url']
                
                # Get conversation history for this query
                conversation_history = get_conversation_history_for_query(conversation_id, query_id)
                
                # Get AI response
                ai_response = handle_ai(question, image_url, conversation_history)
                
                if ai_response:
                    # Store AI response
                    insert_response_query = """
                    INSERT INTO responses (query_id, ai_response, clinician_response, status)
                    VALUES (%s, %s, NULL, 'unreviewed');
                    """
                    cursor.execute(insert_response_query, (query_id, ai_response))
                    conn.commit()
                    processed_count += 1
                else:
                    failed_queries.append(f"Query ID {query_id}: Failed to get AI response")
                    
            except Exception as e:
                failed_queries.append(f"Query ID {query_row['id']}: {str(e)}")
                continue
        
        conn.close()
        
        response_data = {
            "success": True,
            "message": f"Processed {processed_count} queries successfully",
            "processed": processed_count,
            "total_found": len(queries_without_responses)
        }
        
        if failed_queries:
            response_data["failures"] = failed_queries
        
        return jsonify(response_data), 200
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in fix_missing_responses: {str(e)}")
        print(f"Traceback: {error_traceback}")
        return jsonify({"success": False, "error": str(e)}), 500

def get_conversation_history_for_query(conversation_id, current_query_id):
    """Fetches the conversation history for a given conversation up to but not including the current query."""
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
            q.conversation_id = %s AND q.id < %s
        ORDER BY
            q.created_at ASC;
        """
        cursor.execute(query, (conversation_id, current_query_id))
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