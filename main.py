import os
import time

from classes import Porcupine, Vosk, Player,Record



def main():
    # доброе утро
    print(f"папка - {os.getcwd()}")
    player = Player()
    player.play("sound/run")

    vosk = Vosk()
    porcupine= Porcupine()
    micro = Record()
    
    micro.start()
    player.play("sound/ready",micro)
    
    while True:
        # bufer = micro.read()
        if(porcupine.detect_word(micro.read())):
            player.play("sound/yesSir",micro)
            end = time.time() + 15
        
            while end - time.time()>0:
                text = vosk.speech_to_text(micro.read())
                # if not CommandExecute.execute(text,micro):
                #     break
            print("\nsleep")

if __name__ == "__main__":
    main()