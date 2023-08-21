import yaml
from rapidfuzz import fuzz
import os
from functools import cache
from . import Player
import eel


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
