"""Базовые классы для работы syrinx"""

import os
import struct
import json
import yaml
from random import choice
from subprocess import run as process

from rapidfuzz import fuzz
from dotenv import load_dotenv

import pvporcupine
import pvrecorder
import vosk
from pygame import mixer, time
from pygame import init as pyInit
import pyautogui

import config



load_dotenv()

class Record:
  
  def __init__(self):
    self.record = pvrecorder.PvRecorder(device_index=-1,frame_length=512)
    # print("[info] Микрофон подключён.")
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
        # print("[info] VOSK готов.")
    
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

    #   print("[info] Поркупине готов.")
  
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
        # print("[info] Player готов.")
   
    def play(self,path,micro = None):
        if micro:
            micro.stop()
        try:    
            sound = mixer.Sound(path)
            sound.play()
            length = sound.get_length() * 1000
            time.wait(int(length))  # в миллисекундах
        except FileNotFoundError:
            print("[error] Файл музыки не найден")
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
            print(f"[error] Файл {filename} не найден")

        try:
            filename = "yaml/commands.yaml"
            with open(filename) as yf2:
                data = yaml.safe_load(yf2)
                for key, value in data.items():
                    self.__cmd_dict[key]=value

        except FileNotFoundError:
            print(f"[error] Файл {filename} не найден")

    #основный метод 
    def execute(self,text:str, micro:Record, player:Player):
        name_dict, cur_dict = self.__controller(text)
        value_in_dict = self.__best_match(text,cur_dict)

        if not value_in_dict:
            player.play("sound/not_found.wav",micro)
            return True
        
        sounds = ["sound/ok.wav", "sound/yesSir.wav","sound/loading.wav"]
        cur_sound = choice(sounds)

        if name_dict == "bin":
           return self.__process_bin(
               value_in_dict=value_in_dict,
                player=player,
                micro=micro,
                cur_sound=cur_sound
           )
        
        if name_dict == "cmd":
            return self.__process_cmd(
                value_in_dict=value_in_dict,
                player=player,
                micro=micro
                )
    
            
    #определяет тип команды в самом начале (bin, cmd, None)
    def __controller(self,text:str)->tuple[str,dict]:
        list_word  = text.split()
        words_open_apps = ["открой", "запусти" , "открыть" , "запустить"]
        
        for word in list_word:
            if word in words_open_apps:
                return "bin" , self.__bin_dict
            
        return "cmd", self.__cmd_dict
    

    #находит наилучшее совпадение в словаре
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
        return 


      # выполняет команды из файла bin_apps.yaml          
    def __process_bin(self,value_in_dict,player:Player,micro:Record, cur_sound:str):
        player.play(cur_sound,micro)
        try:
            process(["flatpak","run", value_in_dict]) # запуск приложения
            return True
        except FileNotFoundError:
            print("\n[error] Не удалось найти программу")
            return True
        except PermissionError:
            print("\n[error] Отказано в доступе. Запустите с правами администратора.")   
            return
    

    # выполняет команды из файла commands.yaml
    def __process_cmd(self,value_in_dict,player:Player,micro:Record):
          match value_in_dict:
                case "break":
                    player.play("sound/ok.wav",micro)
                    return 
                case "sleep":
                    return
                case "thanks":
                    player.play("sound/thanks.wav",micro)
                    return
                case "write":
                    pass
                case "exit":
                    os._exit(0)
                case "space": 
                    # эти кнопки нажимаются по одному разу
                    self.keymouse_remote(name_key=value_in_dict)
                    return True


    #Эта функция будет писать вместо меня
    #но сначала хорошо бы остановить предыдущий микрофоно чтобы не смешивалось
     
        
    def keymouse_remote(self,name_key="",
                        count:int=None, 
                        c_x:int = None,
                        c_y:int = None, 
                        ):
        gui = pyautogui
        if name_key:
            if count:
                gui.press(name_key,presses=count)
                return 
            else:
                gui.press(name_key)
                return
        
        