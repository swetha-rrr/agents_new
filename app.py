import os
from flask import Flask, request, jsonify
from langchain_groq import GroqModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Groq Setup (Assuming Groq integration is setup using LangChain)
groq_model = GroqModel.from_pretrained("llama3-8b-8192")  # Specify your Groq model name

# Predefined safety-related keywords or phrases
safety_keywords = ['harassment', 'threat', 'afraid', 'scared', 'unsafe', 'help', 'danger']

# Function to detect if any of the keywords are in the question
def check_safety_concerns(question):
    for keyword in safety_keywords:
        if keyword.lower() in question.lower():
            return True
    return False

# Route for voice assistant functionality (question answering)
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Get the question from the POST request
        data = request.get_json()
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Check if the question contains safety-related keywords
        if check_safety_concerns(question):
            # You can customize this response as per your requirements
            response = "It sounds like you're in a potentially unsafe situation. Please take immediate action and contact authorities if needed."
        else:
            # Get a general response from Groq model
            response = groq_model.predict(question)

        return jsonify({'answer': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for speech-to-text functionality (convert voice to text)
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        # Get audio file from the POST request
        audio_file = request.files['audio']

        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Convert speech to text using SpeechRecognition
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        # Recognize speech
        text = recognizer.recognize_google(audio)
        return jsonify({'text': text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to provide instructions (welcome message)
@app.route('/instructions', methods=['GET'])
def get_instructions():
    instructions = """
    Welcome to the Women Safety Assistant Bot. 
    This bot is designed to help you with any safety concerns you might have. 
    If you are feeling unsafe or threatened, feel free to ask for help.
    Here are some keywords to get started:
    - "harassment" - If you feel you are being harassed.
    - "afraid" or "scared" - If you are feeling fearful.
    - "help" or "danger" - If you feel you are in immediate danger.
    If you need immediate assistance, contact local authorities.
    """
    return jsonify({'instructions': instructions}), 200

if __name__ == '__main__':
    app.run(debug=True)
