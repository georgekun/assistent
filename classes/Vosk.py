import vosk
import struct
import json
import eel

class Vosk:
    def __init__(self):
        model = vosk.Model("./models/vosk-model-small-ru-0.22")
        self.kaldi = vosk.KaldiRecognizer(model,16000)
        print("VOSK готов.")
    
    def speechToText(self,pcm):
        struct_pcm = struct.pack("h" * len(pcm), *pcm)
        if(self.kaldi.AcceptWaveform(struct_pcm)):
          letter = json.loads(self.kaldi.Result())["text"]
          if(len(letter)>3):
              print("\nРаспознано: " + letter)
            #   eel.js_view_info(str(letter))
              return letter

