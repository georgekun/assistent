import os
import time

import classes


def main():
    player = classes.Player()
    player.play("sound/run")

    vosk = classes.Vosk()
    porcupine= classes.Porcupine()
    micro = classes.Record()
    executer = classes.Executer()

    micro.start()
    player.play("sound/ready",micro)
    
    while True:
        # bufer = micro.read()
        if(porcupine.detect_word(micro.read())):
            player.play("sound/yesSir",micro)
            end = time.time() + 15
        
            while end - time.time()>0:
                text = vosk.speech_to_text(micro.read())
                if text:
                    executer.execute(text,micro,player)
                
            print("\nsleep")

if __name__ == "__main__":
    main()