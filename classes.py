"""Базовые классы для работы syrinx"""

import os
import struct
import json
import yaml
import random
import subprocess

# from pydub import playback, AudioSegment
from rapidfuzz import fuzz
from dotenv import load_dotenv

import pvporcupine
import pvrecorder
import vosk
from pygame import mixer, time
from pygame import init as pyInit
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
            access_key= os.getenv("porcupine_key"),
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



class Player:
     #воспроизводит звук
    def __init__(self) -> None:
        pyInit()
        print("[info] Player готов.")
   
    def play(self,path,micro = None):
        if micro:
            micro.stop()
        sound = mixer.Sound(f'{path}.wav')
        sound.play()
        length = sound.get_length() * 1000
        time.wait(int(length))  # в миллисекундах
        if micro:
            micro.start()





class Executer:
    def __init__(self) -> None:
        """при инициализации будем брать все команды из yaml файлов и помещать их 
        в словари, так будет быстрее, поскольку каждый раз не надо будет обращаться 
        yaml и все читать еще раз
        """
        self.__bin_dict = dict()
        self.__cmd_dict = dict()

        try:
            filename = "yaml/bin_apps.yaml"
            with open(filename) as yf1:
                data = yaml.safe_load(yf1)
                for key, value in data.items():
                    self.__bin_dict[key]=value
        except FileNotFoundError:
            print(f"файл {filename} не найден")

    #основный метод 
    def execute(self,text:str, micro:Record, player:Player):
        name_dict, cur_dict = self.__controller(text)
        value_in_dict = self.__best_match(text,cur_dict)
        sounds = ["sound/ok", "sound/yesSir","sound/loading"]
        cur_sound = random.choice(sounds)

        if name_dict == "bin":
            player.play(cur_sound,micro)
            try:
                os.open("/home/jordan/Telegram")
            except:
                print("\n[error] не удалось открыть программу")
        if name_dict == "cmd":
            pass

    #определяет тип команды в самом начале (bin, cmd, None)
    def __controller(self,text:str)->tuple[str,dict]:
        list_word  = text.split()
        words_open_apps = ["открой", "запусти" , "открыть" , "запустить"]
        
        for word in list_word:
            if word in words_open_apps:
                return "bin" , self.__bin_dict
            
        return "cmd", self.__cmd_dict
    

    def __best_match(self,text:str,current_dict:dict)->str:
        if not current_dict:
            current_dict = self.__bin_dict
        # проходим по словарю и получаем наилучшее совпадение
        best_result = ""
        percent_match = 70

        for keyword in current_dict:
            new_percent = fuzz.partial_ratio(text,keyword)
            if new_percent>percent_match:
                percent_match = new_percent
                best_result = keyword
            if new_percent >=90: # чтоб по всем не проходил каждый раз
                break

        if best_result:
            return current_dict[best_result]
        
        return "Not Found"
    
    