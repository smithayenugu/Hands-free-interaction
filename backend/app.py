# import cv2
# import mediapipe as mp
# from pynput.mouse import Controller, Button
# import time

# # Initialize webcam and Face Mesh
# cam = cv2.VideoCapture(0)
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# # Set screen size (adjust to your resolution)
# screen_w, screen_h = 1920, 1080

# # Initialize Mouse Controller
# mouse = Controller()

# # Track last cursor position
# last_x, last_y = 0, 0

# # Click prevention variables
# last_click_time = 0
# click_cooldown = 0.7  # seconds

# while cam.isOpened():
#     success, frame = cam.read()
#     if not success:
#         break

#     # Flip and convert frame to RGB
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb_frame)
#     frame_h, frame_w, _ = frame.shape

#     if output.multi_face_landmarks:
#         landmarks = output.multi_face_landmarks[0].landmark

#         # Track the gaze points using landmarks 474 to 477
#         for idx, landmark in enumerate(landmarks[474:478]):
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

#             if idx == 1:
#                 # Compute the relative position (0 to 1)
#                 rel_x = x / frame_w
#                 rel_y = y / frame_h

#                 # Amplify the relative movement around the center (0.5)
#                 amp_factor = 1.8  # Adjust this factor as needed
#                 new_rel_x = (rel_x - 0.5) * amp_factor + 0.5
#                 new_rel_y = (rel_y - 0.5) * amp_factor + 0.5

#                 # Clamp between 0 and 1
#                 new_rel_x = min(max(new_rel_x, 0), 1)
#                 new_rel_y = min(max(new_rel_y, 0), 1)

#                 # Map to full screen coordinates
#                 screen_x = int(new_rel_x * screen_w)
#                 screen_y = int(new_rel_y * screen_h)

#                 # Only update if movement is significant to reduce jitter
#                 if abs(screen_x - last_x) > 5 or abs(screen_y - last_y) > 5:
#                     last_x, last_y = screen_x, screen_y
#                     mouse.position = (screen_x, screen_y)

#         # Detect eye blink for clicking using left eye landmarks (145 and 159)
#         left_eye = [landmarks[145], landmarks[159]]
#         for landmark in left_eye:
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

#         # Check blink detection threshold (adjusted to 0.02 to reduce false clicks)
#         current_time = time.time()
#         if (left_eye[0].y - left_eye[1].y) < 0.02 and (current_time - last_click_time > click_cooldown):
#             print("Click detected")
#             mouse.click(Button.left, 2)
#             last_click_time = current_time

#     cv2.imshow("Eye Controlled Mouse", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()







# import cv2
# import mediapipe as mp
# from pynput.mouse import Controller, Button
# import time
# import speech_recognition as sr
# import pyautogui
# import os
# import subprocess

# # Initialize webcam and Face Mesh
# cam = cv2.VideoCapture(0)
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# # Set screen size
# screen_w, screen_h = 1920, 1080

# # Initialize Mouse Controller
# mouse = Controller()

# # Click prevention pip install SpeechRecognition pyautogui pyaudio

# last_click_time = 0
# click_cooldown = 0.7  # seconds

# # Initialize speech recognizer
# recognizer = sr.Recognizer()

# # Function to open applications
# def open_app(command):
#     apps = {
#         "notepad": "notepad",
#         "word": "winword",
#         "chrome": "chrome",
#         "google docs": "chrome https://docs.google.com"
#     }
#     for key in apps:
#         if key in command:
#             subprocess.Popen(apps[key], shell=True)
#             return f"Opening {key}"

#     return "Application not recognized"

# # Function to convert speech to text
# def voice_to_text():
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Listening for text input...")
#         audio = recognizer.listen(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         pyautogui.typewrite(text)
#         pyautogui.press("enter")
#     except sr.UnknownValueError:
#         print("Could not understand the audio")
#     except sr.RequestError:
#         print("Error with the speech recognition service")

# # Voice control loop
# def voice_control():
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Listening for commands...")
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"Command: {command}")

#         if "open" in command:
#             print(open_app(command))
#         elif "type" in command:
#             voice_to_text()
#         else:
#             print("Command not recognized")
#     except sr.UnknownValueError:
#         print("Could not understand the command")
#     except sr.RequestError:
#         print("Speech recognition service error")

# while cam.isOpened():
#     success, frame = cam.read()
#     if not success:
#         break

#     # Flip and convert frame to RGB
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     output = face_mesh.process(rgb_frame)
#     frame_h, frame_w, _ = frame.shape

#     if output.multi_face_landmarks:
#         landmarks = output.multi_face_landmarks[0].landmark

#         # Track gaze points (landmarks 474 to 477)
#         for idx, landmark in enumerate(landmarks[474:478]):
#             x = int(landmark.x * frame_w)
#             y = int(landmark.y * frame_h)
#             cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

#             if idx == 1:
#                 screen_x = int((x / frame_w) * screen_w)
#                 screen_y = int((y / frame_h) * screen_h)
#                 mouse.position = (screen_x, screen_y)

#         # Blink detection for clicking
#         left_eye = [landmarks[145], landmarks[159]]
#         if (left_eye[0].y - left_eye[1].y) < 0.02 and (time.time() - last_click_time > click_cooldown):
#             print("Click detected")
#             mouse.click(Button.left, 2)
#             last_click_time = time.time()

#     # Show frame
#     cv2.imshow("Eye Controlled Mouse", frame)

#     # Voice trigger key
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('v'):  # Press 'v' to activate voice control
#         voice_control()
#     if key == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()









# import speech_recognition as sr
# import pyttsx3
# import pyautogui
# import subprocess
# import os
# import time

# # Initialize text-to-speech engine
# engine = pyttsx3.init()
# engine.setProperty("rate", 150)

# # Flag to control dictation mode
# is_dictating = False

# # Map commands to application paths
# app_paths = {
#     "files": "nautilus",
#     "text editor": "gedit",
#     "chrome": "google-chrome",
#     "vscode": "code",
#     "terminal": "gnome-terminal",
# }

# # Dictionary for mouse and keyboard actions
# actions = {
#     "left click": pyautogui.click,
#     "right click": pyautogui.rightClick,
#     "double click": pyautogui.doubleClick,
#     "scroll up": lambda: pyautogui.scroll(200),
#     "scroll down": lambda: pyautogui.scroll(-200),
#     "move up": lambda: pyautogui.move(0, -50),
#     "move down": lambda: pyautogui.move(0, 50),
#     "move left": lambda: pyautogui.move(-50, 0),
#     "move right": lambda: pyautogui.move(50, 0),
#     "enter": lambda: pyautogui.press("enter"),
#     "backspace": lambda: pyautogui.press("backspace"),
#     "space": lambda: pyautogui.press("space"),
#     "tab": lambda: pyautogui.press("tab"),
#     "escape": lambda: pyautogui.press("esc"),
#     "close window": lambda: pyautogui.hotkey("alt", "f4"),
#     "switch window": lambda: pyautogui.hotkey("alt", "tab"),
#     "copy": lambda: pyautogui.hotkey("ctrl", "c"),
#     "paste": lambda: pyautogui.hotkey("ctrl", "v"),
#     "cut": lambda: pyautogui.hotkey("ctrl", "x"),
#     "select all": lambda: pyautogui.hotkey("ctrl", "a"),
#     "save": lambda: pyautogui.hotkey("ctrl", "s"),
#     "undo": lambda: pyautogui.hotkey("ctrl", "z"),
#     "redo": lambda: pyautogui.hotkey("ctrl", "y"),
# }


# # -----------------------------
# #  Utility Functions
# # -----------------------------

# def speak(text):
#     """Convert text to speech."""
#     engine.say(text)
#     engine.runAndWait()


# def recognize_speech():
#     """Recognize voice commands."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"Recognized: {command}")
#         return command
#     except (sr.UnknownValueError, sr.RequestError):
#         return ""


# def get_app_path(app_name):
#     """Get application path from dictionary or return the name."""
#     return app_paths.get(app_name, app_name)


# def is_app_running(app_name):
#     """Check if an app is running."""
#     try:
#         result = subprocess.run(["pgrep", "-f", app_name], stdout=subprocess.PIPE)
#         return result.returncode == 0
#     except Exception:
#         return False


# def focus_existing_window(app_name):
#     """Focus on an existing app window."""
#     try:
#         result = subprocess.run(["wmctrl", "-l"], stdout=subprocess.PIPE)
#         windows = result.stdout.decode().lower()

#         if app_name.lower() in windows:
#             subprocess.run(["wmctrl", "-a", app_name], check=True)
#             speak(f"Switched to {app_name}")
#             return True
#     except subprocess.CalledProcessError:
#         pass
#     return False


# # -----------------------------
# #  Application and Dictation Control
# # -----------------------------

# def open_application(command):
#     """Open or switch to an application."""
#     app_name = command.replace("open ", "").strip()
#     app_path = get_app_path(app_name)

#     print(f"Opening: {app_name}")  

#     if is_app_running(app_name):
#         print(f"{app_name} is already running.")
#         if not focus_existing_window(app_name):
#             speak(f"Could not focus on {app_name}, opening a new instance.")
#             subprocess.Popen([app_path])
#     else:
#         speak(f"Opening {app_name}")
#         try:
#             subprocess.Popen([app_path])
#             time.sleep(2)
#             speak(f"{app_name} opened")
#         except Exception as e:
#             speak(f"Could not open {app_name}: {str(e)}")
#             print(f"Error: {e}")


# import speech_recognition as sr
# import pyttsx3
# import pyautogui
# import subprocess
# import os
# import time

# # Initialize text-to-speech engine
# engine = pyttsx3.init()
# engine.setProperty("rate", 150)

# # Flag to control dictation mode
# is_dictating = False

# # Map commands to application paths
# app_paths = {
#     "files": "nautilus",
#     "text editor": "gedit",
#     "chrome": "google-chrome",
#     "vscode": "code",
#     "terminal": "gnome-terminal",
# }

# # Dictionary for mouse and keyboard actions
# actions = {
#     "left click": pyautogui.click,
#     "right click": pyautogui.rightClick,
#     "double click": pyautogui.doubleClick,
#     "scroll up": lambda: pyautogui.scroll(200),
#     "scroll down": lambda: pyautogui.scroll(-200),
#     "move up": lambda: pyautogui.move(0, -50),
#     "move down": lambda: pyautogui.move(0, 50),
#     "move left": lambda: pyautogui.move(-50, 0),
#     "move right": lambda: pyautogui.move(50, 0),
#     "enter": lambda: pyautogui.press("enter"),
#     "backspace": lambda: pyautogui.press("backspace"),
#     "space": lambda: pyautogui.press("space"),
#     "tab": lambda: pyautogui.press("tab"),
#     "escape": lambda: pyautogui.press("esc"),
#     "close window": lambda: pyautogui.hotkey("alt", "f4"),
#     "switch window": lambda: pyautogui.hotkey("alt", "tab"),
#     "copy": lambda: pyautogui.hotkey("ctrl", "c"),
#     "paste": lambda: pyautogui.hotkey("ctrl", "v"),
#     "cut": lambda: pyautogui.hotkey("ctrl", "x"),
#     "select all": lambda: pyautogui.hotkey("ctrl", "a"),
#     "save": lambda: pyautogui.hotkey("ctrl", "s"),
#     "undo": lambda: pyautogui.hotkey("ctrl", "z"),
#     "redo": lambda: pyautogui.hotkey("ctrl", "y"),
# }


# # -----------------------------
# #  Utility Functions
# # -----------------------------

# def speak(text):
#     """Convert text to speech."""
#     engine.say(text)
#     engine.runAndWait()


# def recognize_speech():
#     """Recognize voice commands."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"Recognized: {command}")
#         return command
#     except (sr.UnknownValueError, sr.RequestError):
#         return ""


# def get_app_path(app_name):
#     """Get application path from dictionary or return the name."""
#     return app_paths.get(app_name, app_name)


# def is_app_running(app_name):
#     """Check if an app is running."""
#     try:
#         result = subprocess.run(["pgrep", "-f", app_name], stdout=subprocess.PIPE)
#         return result.returncode == 0
#     except Exception:
#         return False


# def focus_existing_window(app_name):
#     """Focus on an existing app window."""
#     try:
#         result = subprocess.run(["wmctrl", "-l"], stdout=subprocess.PIPE)
#         windows = result.stdout.decode().lower()

#         if app_name.lower() in windows:
#             subprocess.run(["wmctrl", "-a", app_name], check=True)
#             speak(f"Switched to {app_name}")
#             return True
#     except subprocess.CalledProcessError:
#         pass
#     return False


# # -----------------------------
# #  Application and Dictation Control
# # -----------------------------

# def open_application(command):
#     """Open or switch to an application."""
#     app_name = command.replace("open ", "").strip()
#     app_path = get_app_path(app_name)

#     print(f"Opening: {app_name}")  

#     if is_app_running(app_name):
#         print(f"{app_name} is already running.")
#         if not focus_existing_window(app_name):
#             speak(f"Could not focus on {app_name}, opening a new instance.")
#             subprocess.Popen([app_path])
#     else:
#         speak(f"Opening {app_name}")
#         try:
#             subprocess.Popen([app_path])
#             time.sleep(2)
#             speak(f"{app_name} opened")
#         except Exception as e:
#             speak(f"Could not open {app_name}: {str(e)}")
#             print(f"Error: {e}")


# def handle_special_commands(text):
#     """Handle special commands and punctuation during dictation."""
#     replacements = {
#         "comma": ",",
#         "dot": ".",
#         "period": ".",
#         "question mark": "?",
#         "exclamation mark": "!",
#         "colon": ":",
#         "semicolon": ";",
#         "apostrophe": "'",
#         "quote": "\"",
#         "open bracket": "[",
#         "close bracket": "]",
#         "open parenthesis": "(",
#         "close parenthesis": ")",
#         "hashtag": "#",
#         "dollar sign": "$",
#         "percent": "%",
#         "ampersand": "&",
#         "asterisk": "*",
#         "hyphen": "-",
#         "dash": "-",
#         "underscore": "_",
#         "plus": "+",
#         "equal": "=",
#         "space": " ",
#         "backspace": "\b",
#         "tab": "\t",
#         "new line": "\n",
#         "enter": "\n"
#     }

#     words = text.split()

#     for word in words:
#         if word in replacements:
#             symbol = replacements[word]

#             if symbol == "\b":
#                 pyautogui.press("backspace")
#             elif symbol == "\n":
#                 pyautogui.press("enter")
#             elif symbol == "\t":
#                 pyautogui.press("tab")
#             elif symbol == " ":
#                 pyautogui.press("space")
#             else:
#                 pyautogui.typewrite(symbol)
#         else:
#             pyautogui.typewrite(word + " ")


# def enter_text():
#     """Activate dictation mode."""
#     global is_dictating

#     while is_dictating:
#         print("Dictating...")
#         text = recognize_speech()

#         if "stop dictating" in text:
#             is_dictating = False
#             speak("Dictation mode stopped.")
#             break
#         elif text:
#             handle_special_commands(text)
#         else:
#             speak("No text recognized. Try again.")


# # -----------------------------
# #  Main Action Handler
# # -----------------------------

# def perform_action(command):
#     """Execute mouse, keyboard, app, or dictation actions."""
#     global is_dictating

#     if command in actions:
#         actions[command]()
#         speak(f"{command} performed")

#     elif "open" in command:
#         open_application(command)

#     elif "start dictating" in command:
#         if not is_dictating:
#             is_dictating = True
#             speak("Dictation mode enabled. Start speaking.")
#             enter_text()
#         else:
#             speak("Dictation mode is already active.")

#     elif "stop dictating" in command:
#         is_dictating = False
#         speak("Dictation mode stopped.")
        
#     elif "exit" in command:
#         speak("Exiting voice control")
#         exit()
    
#     else:
#         speak("Command not recognized")


# # -----------------------------
# #  Main Loop
# # -----------------------------

# if __name__ == "__main__":
#     speak("Voice control activated. Say a command.")
    
#     while True:
#         command = recognize_speech()
#         if command:
#             perform_action(command)

# def handle_special_commands(text):
#     """Handle special commands and punctuation during dictation."""
#     replacements = {
#         "comma": ",",
#         "dot": ".",
#         "period": ".",
#         "question mark": "?",
#         "exclamation mark": "!",
#         "colon": ":",
#         "semicolon": ";",
#         "apostrophe": "'",
#         "quote": "\"",
#         "open bracket": "[",
#         "close bracket": "]",
#         "open parenthesis": "(",
#         "close parenthesis": ")",
#         "hashtag": "#",
#         "dollar sign": "$",
#         "percent": "%",
#         "ampersand": "&",
#         "asterisk": "*",
#         "hyphen": "-",
#         "dash": "-",
#         "underscore": "_",
#         "plus": "+",
#         "equal": "=",
#         "space": " ",
#         "backspace": "\b",
#         "tab": "\t",
#         "new line": "\n",
#         "enter": "\n"
#     }

#     words = text.split()

#     for word in words:
#         if word in replacements:
#             symbol = replacements[word]

#             if symbol == "\b":
#                 pyautogui.press("backspace")
#             elif symbol == "\n":
#                 pyautogui.press("enter")
#             elif symbol == "\t":
#                 pyautogui.press("tab")
#             elif symbol == " ":
#                 pyautogui.press("space")
#             else:
#                 pyautogui.typewrite(symbol)
#         else:
#             pyautogui.typewrite(word + " ")


# def enter_text():
#     """Activate dictation mode."""
#     global is_dictating

#     while is_dictating:
#         print("Dictating...")
#         text = recognize_speech()

#         if "stop dictating" in text:
#             is_dictating = False
#             speak("Dictation mode stopped.")
#             break
#         elif text:
#             handle_special_commands(text)
#         else:
#             speak("No text recognized. Try again.")


# # -----------------------------
# #  Main Action Handler
# # -----------------------------

# def perform_action(command):
#     """Execute mouse, keyboard, app, or dictation actions."""
#     global is_dictating

#     if command in actions:
#         actions[command]()
#         speak(f"{command} performed")

#     elif "open" in command:
#         open_application(command)

#     elif "start dictating" in command:
#         if not is_dictating:
#             is_dictating = True
#             speak("Dictation mode enabled. Start speaking.")
#             enter_text()
#         else:
#             speak("Dictation mode is already active.")

#     elif "stop dictating" in command:
#         is_dictating = False
#         speak("Dictation mode stopped.")
        
#     elif "exit" in command:
#         speak("Exiting voice control")
#         exit()
    
#     else:
#         speak("Command not recognized")


# # -----------------------------
# #  Main Loop
# # -----------------------------

# if __name__ == "__main__":
#     speak("Voice control activated. Say a command.")
    
#     while True:
#         command = recognize_speech()
#         if command:
#             perform_action(command)






import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import pyautogui
import subprocess
import os
import time
import wave

# -----------------------------
#  Initialization
# -----------------------------

# Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Dictation mode flag
is_dictating = False

# Map commands to application paths
app_paths = {
    "files": "nautilus",
    "text editor": "gedit",
    "chrome": "google-chrome",
    "vscode": "code",
    "terminal": "gnome-terminal",
}

# Mouse and keyboard actions
actions = {
    "left click": pyautogui.click,
    "right click": pyautogui.rightClick,
    "double click": pyautogui.doubleClick,
    "scroll up": lambda: pyautogui.scroll(200),
    "scroll down": lambda: pyautogui.scroll(-200),
    "move up": lambda: pyautogui.move(0, -50),
    "move down": lambda: pyautogui.move(0, 50),
    "move left": lambda: pyautogui.move(-50, 0),
    "move right": lambda: pyautogui.move(50, 0),
    "enter": lambda: pyautogui.press("enter"),
    "backspace": lambda: pyautogui.press("backspace"),
    "space": lambda: pyautogui.press("space"),
    "tab": lambda: pyautogui.press("tab"),
    "escape": lambda: pyautogui.press("esc"),
    "close window": lambda: pyautogui.hotkey("alt", "f4"),
    "switch window": lambda: pyautogui.hotkey("alt", "tab"),
    "copy": lambda: pyautogui.hotkey("ctrl", "c"),
    "paste": lambda: pyautogui.hotkey("ctrl", "v"),
    "cut": lambda: pyautogui.hotkey("ctrl", "x"),
    "select all": lambda: pyautogui.hotkey("ctrl", "a"),
    "save": lambda: pyautogui.hotkey("ctrl", "s"),
    "undo": lambda: pyautogui.hotkey("ctrl", "z"),
    "redo": lambda: pyautogui.hotkey("ctrl", "y"),
}


# -----------------------------
#  Utility Functions
# -----------------------------

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def record_and_recognize():
    """Record audio and recognize speech using sounddevice."""
    fs = 16000
    duration = 5  # Max recording duration
    speak("Listening...")

    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Save recording to WAV
        with wave.open("output.wav", "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(fs)
            f.writeframes(recording.tobytes())

        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        command = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {command}")
        return command

    except Exception as e:
        print(f"Error: {e}")
        return ""


def get_app_path(app_name):
    """Get application path from dictionary or return the name."""
    return app_paths.get(app_name, app_name)


def is_app_running(app_name):
    """Check if an app is running."""
    try:
        result = subprocess.run(["pgrep", "-f", app_name], stdout=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False


def focus_existing_window(app_name):
    """Focus on an existing app window."""
    try:
        result = subprocess.run(["wmctrl", "-l"], stdout=subprocess.PIPE)
        windows = result.stdout.decode().lower()

        if app_name.lower() in windows:
            subprocess.run(["wmctrl", "-a", app_name], check=True)
            speak(f"Switched to {app_name}")
            return True
    except subprocess.CalledProcessError:
        pass
    return False


# -----------------------------
#  Application and Dictation Control
# -----------------------------

def open_application(command):
    """Open or switch to an application."""
    app_name = command.replace("open ", "").strip()
    app_path = get_app_path(app_name)

    print(f"Opening: {app_name}")  

    if is_app_running(app_name):
        print(f"{app_name} is already running.")
        if not focus_existing_window(app_name):
            speak(f"Could not focus on {app_name}, opening a new instance.")
            subprocess.Popen([app_path])
    else:
        speak(f"Opening {app_name}")
        try:
            subprocess.Popen([app_path])
            time.sleep(2)
            speak(f"{app_name} opened")
        except Exception as e:
            speak(f"Could not open {app_name}: {str(e)}")
            print(f"Error: {e}")


def handle_special_commands(text):
    """Handle special commands and punctuation during dictation."""
    replacements = {
        "comma": ",",
        "dot": ".",
        "period": ".",
        "question mark": "?",
        "exclamation mark": "!",
        "colon": ":",
        "semicolon": ";",
        "apostrophe": "'",
        "quote": "\"",
        "open bracket": "[",
        "close bracket": "]",
        "open parenthesis": "(",
        "close parenthesis": ")",
        "hashtag": "#",
        "dollar sign": "$",
        "percent": "%",
        "ampersand": "&",
        "asterisk": "*",
        "hyphen": "-",
        "dash": "-",
        "underscore": "_",
        "plus": "+",
        "equal": "=",
        "space": " ",
        "backspace": "\b",
        "tab": "\t",
        "new line": "\n",
        "enter": "\n"
    }

    words = text.split()

    for word in words:
        if word in replacements:
            symbol = replacements[word]

            if symbol == "\b":
                pyautogui.press("backspace")
            elif symbol == "\n":
                pyautogui.press("enter")
            elif symbol == "\t":
                pyautogui.press("tab")
            elif symbol == " ":
                pyautogui.press("space")
            else:
                pyautogui.typewrite(symbol)
        else:
            pyautogui.typewrite(word + " ")


def enter_text():
    """Activate dictation mode."""
    global is_dictating

    while is_dictating:
        print("Dictating...")
        text = record_and_recognize()

        if "stop dictating" in text:
            is_dictating = False
            speak("Dictation mode stopped.")
            break
        elif text:
            handle_special_commands(text)
        else:
            speak("No text recognized. Try again.")


# -----------------------------
#  Main Action Handler
# -----------------------------

def perform_action(command):
    """Execute mouse, keyboard, app, or dictation actions."""
    global is_dictating

    if command in actions:
        actions[command]()
        speak(f"{command} performed")

    elif "open" in command:
        open_application(command)

    elif "start dictating" in command:
        if not is_dictating:
            is_dictating = True
            speak("Dictation mode enabled. Start speaking.")
            enter_text()
        else:
            speak("Dictation mode is already active.")

    elif "stop dictating" in command:
        is_dictating = False
        speak("Dictation mode stopped.")
        
    elif "exit" in command:
        speak("Exiting voice control")
        exit()
    
    else:
        speak("Command not recognized")


# -----------------------------
#  Main Loop
# -----------------------------

if __name__ == "__main__":
    speak("Voice control activated. Say a command.")
    
    while True:
        command = record_and_recognize()
        if command:
            perform_action(command)