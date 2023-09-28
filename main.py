
import time
import classes


def main():
    player = classes.Player()
    player.play("sound/run.wav")

    vosk = classes.Vosk()
    porcupine= classes.Porcupine()
    micro = classes.Record()
    executer = classes.Executer()

    micro.start()
    player.play("sound/ready.wav",micro)
    
    while True:
        # bufer = micro.read()
        if(porcupine.detect_word(micro.read())):
            player.play("sound/yesSir.wav",micro)
            end = time.time() + 15
        
            while end - time.time()>0:
                text = vosk.speech_to_text(micro.read())
                if text:
                    if not executer.execute(text,micro,player):
                        break

            print("\nsleep")

if __name__ == "__main__":
    main()