from flask import Flask, jsonify
from api.clinician_routes import clinician_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(clinician_bp, url_prefix='/api/clinician')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"})

if __name__ == '__main__':
    app.run(debug=True)