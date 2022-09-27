from flask import Flask, request
from main import Main

app = Flask(__name__)
main_obj = Main()

@app.route('/transcribe')
def transcribe():
    url = request.json['url']
    audio = main_obj.get_mp3_from_yt(url)
    transcription = main_obj.get_transcription(audio)
    return transcription
