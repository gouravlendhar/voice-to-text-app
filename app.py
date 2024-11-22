from flask import Flask, render_template, request
import speech_recognition as sr

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html', title="Voice to Text Transcript")

# Transcription route
@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return "No audio file uploaded", 400

    # Process the uploaded audio file
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            # Use Google Web Speech API to transcribe
            text = recognizer.recognize_google(audio_data)
            return render_template('result.html', title="Transcription Result", transcription=text)
    except sr.UnknownValueError:
        return "Could not understand the audio", 400
    except sr.RequestError:
        return "Speech recognition service is unavailable", 503

# Run the app
if __name__ == '__main__':
    app.run(debug=True)