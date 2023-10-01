
import time
import classes


def main():
    player = classes.Player()
    player.play("sound/run.wav")

    vosk = classes.Vosk()
    porcupine= classes.Porcupine()
    micro = classes.Record()
    executer = classes.Executer(vosk=vosk,micro=micro, player = player)

    micro.start()
    player.play("sound/ready.wav",micro)
    
    while True:
        # bufer = micro.read()
        if(porcupine.detect_word(micro.read())):
            player.play("sound/yesSir.wav",micro)
            end = time.time() + 5
            
            while end - time.time()>0:
                print(f"{end-time.time()}")
                text = vosk.speech_to_text(micro.read())
                if text:
                    if not executer.execute(text):
                        break
            

if __name__ == "__main__":
    main()