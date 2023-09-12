# V3
import os
import time
import torch
from pydub import AudioSegment
from pydub.playback import play


language = 'ru'
sample_rate = 48000
speaker = 'baya'
device = torch.device('cpu')

model = torch.package.PackageImporter("models/silero/model.pt").load_pickle("tts_models", "model")
model.to(device)


def textToSpeech(text,i=0,speaker = "random"):
    audio_paths = model.save_wav(text=text,
                      speaker=speaker,
                      sample_rate=sample_rate,)
    print(audio_paths)
    os.rename(audio_paths,f"{speaker}{i}.wav")

  # for playing wav file
#   song = AudioSegment.from_wav(audio_paths)
#   play(song)
#   time.sleep(1)
  
#   os.remove(audio_paths)





def main():
    speakers = ['xenia' , 'aidar','random','eugene']#baya, eugene,'kseniya'

    for i in speakers:
       textToSpeech("доброе утро",speaker=i)

if __name__ == "__main__":
   main()