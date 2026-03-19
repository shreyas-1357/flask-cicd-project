from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Flask CI/CD Pipeline",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENV", "development"),
        "status": "healthy"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/version')
def version():
    return jsonify({"version": os.getenv("APP_VERSION", "1.0.0")}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)


