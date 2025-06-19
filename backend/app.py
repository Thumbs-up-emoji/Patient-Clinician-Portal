from flask import Flask, jsonify
from api.clinician_routes import clinician_bp
from api.patient_routes import patient_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(clinician_bp, url_prefix='/api/clinician')
app.register_blueprint(patient_bp, url_prefix='/api/patient')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)