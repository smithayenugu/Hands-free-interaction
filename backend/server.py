import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EYE_TRACKING_SCRIPT = os.path.join(BASE_DIR, "eye1.py")
VOICE_CONTROL_SCRIPT = os.path.join(BASE_DIR, "app.py")

# Log important paths for debugging
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Base Directory: {BASE_DIR}")
logger.info(f"Eye Tracking Script: {EYE_TRACKING_SCRIPT}")
logger.info(f"Voice Control Script: {VOICE_CONTROL_SCRIPT}")

# Store process instances
eye_tracking_process = None
voice_control_process = None

@app.route("/")
def home():
    return "Hands-Free Interaction API is Running!"

def start_process(script_path, script_name):
    """Start a subprocess for the given script"""
    try:
        if not os.path.exists(script_path):
            logger.error(f"{script_name} script not found: {script_path}")
            return None, f"Error: {script_name} script not found"

        logger.info(f"Starting {script_name} from {script_path}")

        process = subprocess.Popen(
            ["python3", script_path],  # Ensure 'python3' is used
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        returncode = process.poll()
        if returncode is not None:  # Process failed immediately
            _, stderr = process.communicate()
            logger.error(f"{script_name} failed to start: {stderr}")
            return None, f"{script_name} failed: {stderr}"

        return process, f"{script_name} started successfully"
    except Exception as e:
        logger.error(f"Error starting {script_name}: {str(e)}")
        return None, str(e)

@app.route("/start-eye-tracking", methods=["POST"])
def start_eye_tracking():
    global eye_tracking_process
    if eye_tracking_process and eye_tracking_process.poll() is None:
        return jsonify({"message": "Eye tracking is already running"}), 400

    eye_tracking_process, msg = start_process(EYE_TRACKING_SCRIPT, "Eye Tracking")
    if eye_tracking_process:
        return jsonify({"message": "Eye tracking started"}), 200
    return jsonify({"error": msg}), 500

@app.route("/stop-eye-tracking", methods=["POST"])
def stop_eye_tracking():
    global eye_tracking_process
    if eye_tracking_process:
        try:
            eye_tracking_process.terminate()
            eye_tracking_process.wait(timeout=5)
            eye_tracking_process = None
            return jsonify({"message": "Eye tracking stopped"}), 200
        except Exception as e:
            logger.error(f"Error stopping eye tracking: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Eye tracking is not running"}), 400

@app.route("/start-voice-control", methods=["POST"])
def start_voice_control():
    global voice_control_process
    if voice_control_process and voice_control_process.poll() is None:
        return jsonify({"message": "Voice control is already running"}), 400

    voice_control_process, msg = start_process(VOICE_CONTROL_SCRIPT, "Voice Control")
    if voice_control_process:
        return jsonify({"message": "Voice control started"}), 200
    return jsonify({"error": msg}), 500

@app.route("/stop-voice-control", methods=["POST"])
def stop_voice_control():
    global voice_control_process
    if voice_control_process:
        try:
            voice_control_process.terminate()
            voice_control_process.wait(timeout=5)
            voice_control_process = None
            return jsonify({"message": "Voice control stopped"}), 200
        except Exception as e:
            logger.error(f"Error stopping voice control: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Voice control is not running"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
