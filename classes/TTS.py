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


def textToSpeech(text,speaker = speaker ):
  audio_paths = model.save_wav(text=text,
                      speaker=speaker,
                      sample_rate=sample_rate)

  # for playing wav file
  song = AudioSegment.from_wav(audio_paths)
  play(song)
  time.sleep(1)
  os.remove(audio_paths)
