import os
import sys
import time
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# 1. TEXT-TO-SPEECH & SPEECH RECOGNITION (SAFE FOR WINDOWS)
# ---------------------------------------------------------------------------
def speak(text):
    """Re-initializes engine per call to prevent pyttsx3 from freezing on Windows."""
    print(f"\nJARVIS: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[Speech Error]: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("[Recognizing...]")
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Speech recognition service is offline.")
            return ""

# ---------------------------------------------------------------------------
# 2. GEMINI AI CORE SETUP WITH STABLE ENDPOINT & QUOTA HANDLING
# ---------------------------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("\n[WARNING]: GEMINI_API_KEY environment variable not found.")
    client = None
else:
    try:
        # Enforce v1 endpoint options to ensure model alias compatibility
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version="v1")
        )
    except Exception as e:
        print(f"\n[CLIENT INIT ERROR]: {e}")
        client = None

SYSTEM_INSTRUCTION = """
You are JARVIS, an ultra-intelligent, polite, and advanced AI assistant built to help with anything and everything.
- Respond conversationally and naturally to ANY question, topic, or request.
- Keep spoken answers concise (2 to 3 sentences maximum) so output is fast and clear to listen to.
- You can explain complex concepts, write/debug code, solve math, give advice, or chat casually.
"""

def ask_gemini(prompt):
    if not client:
        return "My AI core is currently offline, sir. Please check your API key variable."
    
    # Priority model list supported across Gemini endpoints
    candidate_models = [
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash'
    ]
    
    for model_name in candidate_models:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )
                if response.text:
                    return response.text
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    print(f"\n[Rate Limit on {model_name}]: Retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    print(f"\n[Model {model_name} skipped]: {e}")
                    break  # Move to next model
            
    return "My core processing unit is experiencing high traffic right now. Please try asking again in a few seconds."

# ---------------------------------------------------------------------------
# 3. APPLICATION TERMINATION HELPER
# ---------------------------------------------------------------------------
def close_app(process_name, display_name):
    try:
        os.system(f"taskkill /f /im {process_name}")
        speak(f"Closed {display_name}.")
    except Exception as e:
        speak(f"Failed to close {display_name}.")

# ---------------------------------------------------------------------------
# 4. ACTION & COMMAND PROCESSOR
# ---------------------------------------------------------------------------
def process_command(command):
    if not command:
        return True

    # System Exit
    if any(word in command for word in ['exit', 'quit', 'goodbye', 'sleep', 'power down']):
        speak("Powering down systems. Goodbye, sir!")
        return False

    # Time & Date
    elif 'time' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif 'date' in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    # Open App / Web Commands
    elif 'open youtube' in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif 'open github' in command:
        speak("Opening GitHub.")
        webbrowser.open("https://www.github.com")

    elif 'open notepad' in command:
        speak("Opening Notepad.")
        os.system("start notepad.exe")

    elif 'open calculator' in command:
        speak("Opening Calculator.")
        os.system("start calc.exe")

    elif 'open command prompt' in command or 'open cmd' in command:
        speak("Opening Command Prompt.")
        os.system("start cmd")

    elif 'open prime' in command:
        speak("Opening Amazon Prime Video.")
        webbrowser.open("https://www.primevideo.com/")

    # Close App Commands
    elif 'close browser' in command or 'close chrome' in command or 'close youtube' in command or 'close google' in command:
        close_app("chrome.exe", "Browser")

    elif 'close edge' in command:
        close_app("msedge.exe", "Microsoft Edge")

    elif 'close notepad' in command:
        close_app("notepad.exe", "Notepad")

    elif 'close calculator' in command:
        close_app("CalculatorApp.exe", "Calculator")

    elif 'close command prompt' in command or 'close cmd' in command:
        close_app("cmd.exe", "Command Prompt")

    elif 'close code' in command or 'close vs code' in command:
        close_app("Code.exe", "Visual Studio Code")

    # Web Searches & Media
    elif command.startswith('play '):
        song = command.replace('play ', '')
        speak(f"Playing {song} on YouTube.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    elif command.startswith('search for ') or command.startswith('google '):
        search_query = command.replace('search for ', '').replace('google ', '')
        speak(f"Searching Google for {search_query}.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    # EVERY OTHER QUERY GOES TO GEMINI AI
    else:
        response = ask_gemini(command)
        speak(response)

    return True

# ---------------------------------------------------------------------------
# 5. MAIN LOOP
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    speak("Systems online. How may I assist you today?")
    
    running = True
    while running:
        user_input = listen()
        if user_input:
            running = process_command(user_input)