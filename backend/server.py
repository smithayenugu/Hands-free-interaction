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

# Dynamic path handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# Add directories to Python path
sys.path.extend([BASE_DIR, PARENT_DIR, SCRIPTS_DIR])

# Define script paths
EYE_TRACKING_SCRIPT = os.path.join(SCRIPTS_DIR, "eye1.py")
VOICE_CONTROL_SCRIPT = os.path.join(SCRIPTS_DIR, "app.py")

# Create scripts directory if it doesn't exist
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Store process instances
eye_tracking_process = None
voice_control_process = None

# Log directory structure
logger.info(f"Base Directory: {BASE_DIR}")
logger.info(f"Parent Directory: {PARENT_DIR}")
logger.info(f"Scripts Directory: {SCRIPTS_DIR}")
logger.info(f"Eye Tracking Script Path: {EYE_TRACKING_SCRIPT}")
logger.info(f"Voice Control Script Path: {VOICE_CONTROL_SCRIPT}")

@app.route("/")
def home():
    return "Hands-Free Interaction API is Running!"

def start_process(script_path, script_name):
    try:
        logger.info(f"Attempting to start {script_name} from {script_path}")
        
        if not os.path.exists(script_path):
            logger.error(f"Script not found: {script_path}")
            return None, f"Error: {script_name} not found at {script_path}"

        # Add environment variables
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{PARENT_DIR}:{BASE_DIR}:{SCRIPTS_DIR}:{env.get('PYTHONPATH', '')}"

        process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            cwd=SCRIPTS_DIR  # Set working directory to scripts folder
        )
        
        # Check immediate errors
        returncode = process.poll()
        if returncode is not None:
            _, stderr = process.communicate()
            logger.error(f"Process failed to start: {stderr}")
            return None, f"Process failed: {stderr}"

        logger.info(f"Successfully started {script_name}")
        return process, "Success"
    except Exception as e:
        logger.error(f"Error starting process: {str(e)}")
        return None, str(e)

@app.route("/start-eye-tracking", methods=["POST"])
def start_eye_tracking():
    global eye_tracking_process
    
    if eye_tracking_process:
        if eye_tracking_process.poll() is None:
            return jsonify({"message": "Eye tracking is already running"}), 400
        eye_tracking_process = None

    logger.info("Starting eye tracking process")
    eye_tracking_process, msg = start_process(EYE_TRACKING_SCRIPT, "eye tracking")
    
    if eye_tracking_process:
        return jsonify({"message": "Eye tracking started"}), 200
    return jsonify({"error": msg}), 500

@app.route("/stop-eye-tracking", methods=["POST"])
def stop_eye_tracking():
    global eye_tracking_process
    if eye_tracking_process:
        try:
            logger.info("Stopping eye tracking process")
            eye_tracking_process.terminate()
            eye_tracking_process.wait(timeout=5)
            eye_tracking_process = None
            return jsonify({"message": "Eye tracking stopped"}), 200
        except subprocess.TimeoutExpired:
            logger.error("Force killing eye tracking process")
            eye_tracking_process.kill()
            eye_tracking_process = None
            return jsonify({"message": "Eye tracking force stopped"}), 200
        except Exception as e:
            logger.error(f"Error stopping eye tracking: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Eye tracking is not running"}), 400

@app.route("/start-voice-control", methods=["POST"])
def start_voice_control():
    global voice_control_process
    
    if voice_control_process:
        if voice_control_process.poll() is None:
            return jsonify({"message": "Voice control is already running"}), 400
        voice_control_process = None

    logger.info("Starting voice control process")
    voice_control_process, msg = start_process(VOICE_CONTROL_SCRIPT, "voice control")
    
    if voice_control_process:
        return jsonify({"message": "Voice control started"}), 200
    return jsonify({"error": msg}), 500

@app.route("/stop-voice-control", methods=["POST"])
def stop_voice_control():
    global voice_control_process
    if voice_control_process:
        try:
            logger.info("Stopping voice control process")
            voice_control_process.terminate()
            voice_control_process.wait(timeout=5)
            voice_control_process = None
            return jsonify({"message": "Voice control stopped"}), 200
        except subprocess.TimeoutExpired:
            logger.error("Force killing voice control process")
            voice_control_process.kill()
            voice_control_process = None
            return jsonify({"message": "Voice control force stopped"}), 200
        except Exception as e:
            logger.error(f"Error stopping voice control: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Voice control is not running"}), 400

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({
        "eye_tracking": {
            "status": "running" if eye_tracking_process and eye_tracking_process.poll() is None else "stopped",
            "script_exists": os.path.exists(EYE_TRACKING_SCRIPT),
            "script_path": EYE_TRACKING_SCRIPT
        },
        "voice_control": {
            "status": "running" if voice_control_process and voice_control_process.poll() is None else "stopped",
            "script_exists": os.path.exists(VOICE_CONTROL_SCRIPT),
            "script_path": VOICE_CONTROL_SCRIPT
        },
        "directories": {
            "base_dir": BASE_DIR,
            "parent_dir": PARENT_DIR,
            "scripts_dir": SCRIPTS_DIR
        },
        "python_path": sys.path
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
