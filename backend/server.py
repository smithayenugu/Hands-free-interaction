import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get absolute path to backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Store process IDs
eye_tracking_process = None
voice_control_process = None

@app.route("/")
def home():
    return "Hands-Free Interaction API is Running!"

@app.route("/start-eye-tracking", methods=["POST"])
def start_eye_tracking():
    global eye_tracking_process
    if eye_tracking_process is None:
        eye_tracking_process = subprocess.Popen(["python", os.path.join(BASE_DIR, "eye1.py")])
        return jsonify({"message": "Eye tracking started"}), 200
    return jsonify({"message": "Eye tracking is already running"}), 400

@app.route("/stop-eye-tracking", methods=["POST"])
def stop_eye_tracking():
    global eye_tracking_process
    if eye_tracking_process:
        eye_tracking_process.terminate()
        eye_tracking_process = None
        return jsonify({"message": "Eye tracking stopped"}), 200
    return jsonify({"message": "Eye tracking is not running"}), 400

@app.route("/start-voice-control", methods=["POST"])
def start_voice_control():
    global voice_control_process
    if voice_control_process is None:
        voice_control_process = subprocess.Popen(["python", os.path.join(BASE_DIR, "app.py")])
        return jsonify({"message": "Voice control started"}), 200
    return jsonify({"message": "Voice control is already running"}), 400

@app.route("/stop-voice-control", methods=["POST"])
def stop_voice_control():
    global voice_control_process
    if voice_control_process:
        voice_control_process.terminate()
        voice_control_process = None
        return jsonify({"message": "Voice control stopped"}), 200
    return jsonify({"message": "Voice control is not running"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a port automatically
    app.run(host="0.0.0.0", port=port)
