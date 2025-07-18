from flask import Flask, jsonify
from api.clinician_routes import clinician_bp
from api.patient_routes import patient_bp
from api.admin_routes import admin_bp
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

app = Flask(__name__)

# Register blueprints
app.register_blueprint(clinician_bp, url_prefix='/api/clinician')
app.register_blueprint(patient_bp, url_prefix='/api/patient')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
#    app.run(debug=True, use_reloader=False)
