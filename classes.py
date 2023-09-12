"""Базовые классы для работы syrinx"""

import os
import struct
import json
import yaml


# from pydub import playback, AudioSegment
from rapidfuzz import fuzz
from dotenv import load_dotenv

import pvporcupine
import pvrecorder
import vosk
import pygame
import config

load_dotenv()


class Record:
  
  def __init__(self):
    self.record = pvrecorder.PvRecorder(device_index=-1,frame_length=512)
    print("[info] Микрофон подключён.")

  def start(self):
    self.record.start()

  def stop(self):
    self.record.stop()

  def read(self):
    return self.record.read()


class Vosk:

    def __init__(self):
        model = vosk.Model(config.vosk_model_path)
        self.kaldi = vosk.KaldiRecognizer(model,16000)
        print("[info] VOSK готов.")
    
    def speech_to_text(self,pcm):
        struct_pcm = struct.pack("h" * len(pcm), *pcm)  
        if self.kaldi.AcceptWaveform(struct_pcm):
            letter = json.loads(self.kaldi.Result())["text"]

            if(len(letter)>3):
                print(f"\rРаспознано:{letter}", end="")
                return letter



class Porcupine:

    def __init__(self):
      self.porcupine = pvporcupine.create(
            access_key= os.getenv("porcupine_access"),
            keyword_paths=["./models/porcupine/syrinx_en_linux_v2_2_0.ppn"],
            # keywords=["jarvis"],
            # model_path='./models/porcupine/porcupine_params_ru.pv',
            sensitivities=[config.sensitiviti_porcupine])

      print("[info] Поркупине готов.")
  
    def detect_word(self,pcm):
        index = self.porcupine.process(pcm)
        if(index>=0):
          return True
        else: 
          return False



class Player():
    def __init__(self) -> None:
        pass
    #воспроизводит звук

    def play(self,path,micro = None):
        if micro:
            micro.stop()

        # path = f"{path}.wav"
        # song = AudioSegment.from_wav(path)
        # playback.play(song)
        pygame.init()
        # Создайте объект звука, загрузив WAV-файл
        sound = pygame.mixer.Sound(f'{path}.wav')
        # Воспроизведите звук
        sound.play()
        # Подождите, пока звук не закончится (если нужно)
        length = sound.get_length() * 1000
        print(length)
        pygame.time.wait(length)  # в миллисекундах
        # Завершите Pygame (необязательно)
        pygame.quit()
        if micro:
            micro.start()

def getNameScriptFromYaml(text):
    with open("./yaml/commands.yaml",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    maxScore = 0
    for key,value  in data.items():
        for k,p in value.items():
            if k == "keyword":
                for word in p:
                    newScore = fuzz.partial_ratio(text,word)
                    if newScore > maxScore and newScore>80:
                        maxScore= newScore
                        ahk = value["ahkFile"]
                        sound = value["sound"]
                        action = value["action"]
                        path = value["path"]
                        
    if maxScore<70:
        return False
    return ahk,sound,action,path

def execute(text,micro):#,micro
    if(getNameScriptFromYaml(text)):
        ahk,sound,action,path = getNameScriptFromYaml(text) 
        # print(f"куда попал: {ahk}, {sound}, {action}, {path}\n")
        if ahk != False:
            path = os.path.abspath(f"./ahk/{ahk}")
            os.startfile(path)
        if sound != False:
            Player.play(f"{sound}",micro)   
        if action != False:
            if action == "exit":
                os._exit(0)
            elif action == "break":
                return False 
            elif action == "start":
                os.startfile(path)
    else:
        Player.play("not_found",micro)
    return True
