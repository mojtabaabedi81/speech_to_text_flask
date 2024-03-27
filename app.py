from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Initialize the SpeechRecognition recognizer
    recognizer = sr.Recognizer()

    try:
        # Use recognizer to convert speech to text
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            # Recognize speech with Persian language
            text = recognizer.recognize_google(audio_data, language="fa-IR")
            # Translate the text to English for the response
            translated_text = translator.translate(text, src="fa", dest="en").text
            return jsonify({'text': translated_text}), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech not recognized'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results; {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
