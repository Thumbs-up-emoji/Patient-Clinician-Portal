from flask import Blueprint, request, jsonify
from config.db_config import get_db_connection
import pywhatkit
import pyautogui
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

clinician_bp = Blueprint('clinician', __name__)

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
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  # Shows full stack trace
        return jsonify({"success": False, "error": str(e)}), 500
    
@clinician_bp.route('/responses/verify/<int:response_id>', methods=['PUT'])
def verify_response(response_id):
    """Verify a response by setting its status to 'reviewed'."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE responses
            SET status = 'reviewed', reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
        values = (response_id,)

        cursor.execute(query, values)
        conn.commit()

        conn.close()
        return jsonify({"success": True, "message": "Response verified successfully"})

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  # Shows full stack trace
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

@clinician_bp.route('/pending-conversations', methods=['GET'])
def get_pending_conversations():
    """Get all conversations with any unreviewed responses, sorted by the earliest unreviewed query."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            c.id AS conversation_id,
            c.created_at AS conversation_created_at,
            MIN(q.created_at) AS earliest_unreviewed_query
        FROM
            conversations c
        JOIN
            queries q ON c.id = q.conversation_id
        JOIN
            responses r ON q.id = r.query_id
        WHERE
            r.status = 'unreviewed'
        GROUP BY
            c.id, c.created_at
        ORDER BY
            earliest_unreviewed_query ASC;
        """

        cursor.execute(query)
        conversations = cursor.fetchall()
        if not conversations:
            return jsonify({"success": True, "data": [], "message": "No unreviewed responses found"}), 200
        
        conn.close()

        # Convert the results to a list of dictionaries
        conversation_list = []
        for row in conversations:
            conversation_dict = {
                'conversation_id': row['conversation_id'],
                'conversation_created_at': row['conversation_created_at'],
                'earliest_unreviewed_query': row['earliest_unreviewed_query']
            }
            conversation_list.append(conversation_dict)

        return jsonify({"success": True, "data": conversation_list})

    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  # Shows full stack trace
        return jsonify({"success": False, "error": str(e)}), 500
    
def notify(num, answer_edited, email):
    # Notifies relevant patients about their queries
    pywhatkit.sendwhatmsg_instantly(num, "Query updated on patient-clinician-portal!", wait_time=10, tab_close=True, close_time=2)
    pyautogui.press("enter")
    if answer_edited:
        send_email("Answer Edited", "Query updated on patient-clinician-portal!", "patientclinicianportal@gmail.com", email, os.environ.get('EMAIL_PASSWORD'))
    else:
        send_email("Answer Verified", "Query updated on patient-clinician-portal!", "patientclinicianportal@gmail.com", email, os.environ.get('EMAIL_PASSWORD'))

def send_email(subject, message, from_addr, to_addr, password):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()