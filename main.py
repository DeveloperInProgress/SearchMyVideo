from urllib.parse import urlparse, parse_qs
from pytube import YouTube
import os 
import whisper 

class Main:
    def __init__(self):
        pass

    def video_id(self, url):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # fail?
        return None

    def get_mp3_from_yt(self, url):
        destination = self.video_id(url)
        if(os.path.exists(destination+'.mp3')):
            return destination+'.mp3'
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        out_file = audio.download(output_path=destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file

    def get_transcription(self, audio):
        model = whisper.load_model("base")
        result = model.transcribe(audio)
        return result 
