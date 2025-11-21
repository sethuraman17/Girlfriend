import streamlit as st
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import time

# Initialize speech recognition and TTS engines
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to recognize speech with retries
def recognize_speech_with_retry(retry_count=3):
    for _ in range(retry_count):
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                st.write(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                st.write("Sorry, I did not get that. Please try again.")
                speak_text("Sorry, I did not get that. Please try again.")
                time.sleep(2)
    return None

# Function to speak a text in English
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to generate and play Tamil text using gTTS
def generate_and_play_tamil(text):
    tts = gTTS(text=text, lang='ta')
    tts.save("response.mp3")
    st.audio("response.mp3")

# Function to prompt user repeatedly until a valid response is obtained
def prompt_user_until_valid_response(prompt_text, tamil_text=None, language="en"):
    while True:
        if language == "en":
            speak_text(prompt_text)
        elif language == "ta" and tamil_text:
            generate_and_play_tamil(tamil_text)
        time.sleep(2)  # Wait for 2 seconds before listening

        command = recognize_speech_with_retry()
        if command:
            return command

# Function to clean up generated Tamil audio files
def cleanup_audio_file(file_path="response.mp3"):
    if os.path.exists(file_path):
        os.remove(file_path)

# Streamlit App Layout
st.title("Accessible ATM Interface")

# Language Selection with repetition until a valid response is obtained
language = prompt_user_until_valid_response(
    "Select your language. Say 1 for English or say 2 for Tamil.",
    "உங்கள் மொழியைத் தேர்வு செய்யவும். 1 ஐ சொன்னால் ஆங்கிலம், 2 ஐ சொன்னால் தமிழ்.",
)

if language == "one" or language == "1":
    speak_text("You have selected English!")
    # English Menu with repetition until a valid response is obtained
    command = prompt_user_until_valid_response(
        "Say 1 to check balance. Say 2 to withdraw money. Say 3 for transaction. Say 4 to change password."
    )
    
    if command == "one" or command == "1":
        pin = prompt_user_until_valid_response("Please say your 4-digit PIN.")
        # Assuming PIN is verified
        if pin:
            speak_text("Your account balance is 5000 rupees.")
        
    elif command == "two" or command == "2":
        pin = prompt_user_until_valid_response("Please say your 4-digit PIN.")
        if pin:
            speak_text("You have successfully withdrawn 1000 rupees.")

    elif command == "three" or command == "3":
        pin = prompt_user_until_valid_response("Please say your 4-digit PIN.")
        if pin:
            speak_text("Transaction completed successfully.")
        
    elif command == "four" or command == "4":
        new_pin = prompt_user_until_valid_response("Please say your new 4-digit PIN.")
        if new_pin:
            speak_text("Your PIN has been changed successfully.")

elif language == "two" or language == "2":
    generate_and_play_tamil("நீங்கள் தமிழ் தேர்வு செய்துள்ளீர்கள்!")
    # Tamil Menu with repetition until a valid response is obtained
    command = prompt_user_until_valid_response(
        "Say 1 to check balance. Say 2 to withdraw money. Say 3 for transaction. Say 4 to change password.",
        "நீங்கள் 1 ஐ சொன்னால்  உங்கள் இருப்பை சரிபார்க்கலாம். 2 ஐ சொன்னால் பணம் எடுக்கலாம். 3 ஐ சொன்னால் பரிவர்த்தனை செய்யலாம். 4 ஐ சொன்னால் கடவுச்சொல்லை மாற்றலாம்.",
        language="ta"
    )
    
    if command == "one" or command == "1":
        pin = prompt_user_until_valid_response(
            "Please say your 4-digit PIN.",
            "உங்கள் 4-இலக்க ரகசிய எண்ணைச் சொல்லவும்.",
            language="ta"
        )
        # Assuming PIN is verified
        if pin:
            generate_and_play_tamil("உங்கள் கணக்கு இருப்பு 5000 ரூபாய்.")
        
    elif command == "two" or command == "2":
        pin = prompt_user_until_valid_response(
            "Please say your 4-digit PIN.",
            "உங்கள் 4-இலக்க ரகசிய எண்ணைச் சொல்லவும்.",
            language="ta"
        )
        if pin:
            generate_and_play_tamil("நீங்கள் 1000 ரூபாய் பணத்தை எடுத்துள்ளீர்கள்.")
        
    elif command == "three" or command == "3":
        pin = prompt_user_until_valid_response(
            "Please say your 4-digit PIN.",
            "உங்கள் 4-இலக்க ரகசிய எண்ணைச் சொல்லவும்.",
            language="ta"
        )
        if pin:
            generate_and_play_tamil("பரிவர்த்தனை வெற்றிகரமாக முடிந்தது.")
        
    elif command == "four" or command == "4":
        new_pin = prompt_user_until_valid_response(
            "Please say your new 4-digit PIN.",
            "உங்கள் புதிய 4-இலக்க ரகசிய எண்ணைச் சொல்லவும்.",
            language="ta"
        )
        if new_pin:
            generate_and_play_tamil("உங்கள் ரகசிய எண் வெற்றிகரமாக மாற்றப்பட்டுள்ளது.")

# Cleanup any generated audio files
cleanup_audio_file()
