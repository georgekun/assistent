from classes import Porcupine, Vosk, Player,Record
from classes import ChatCompletion, CommandExecute 
import time

# доброе утро
Player.play("run")
# vosk = Vosk.Vosk()
porcupine= Porcupine.Porcupine()
micro = Record.Record()
micro.start()
Player.play("ready",micro)

while True:
    if(porcupine.detectWord(micro.read())):
        Player.play("yesSir",micro)
        end = time.time() + 15
        
        # while end - time.time()>0:
            # text = vosk.speechToText(micro.read())
            # if text != None:
            #     if text.startswith("скажи"):
            #         micro.stop()
            #         Player.play("request")
            #         ChatCompletion.openaiResponse(text)
            #         micro.start()
            #     else:
            #         startExe = time.time()
            #         if not CommandExecute.execute(text,micro):
            #             break
            #         endExe = time.time()
            #         print(f"Время = {endExe-startExe}") 
   