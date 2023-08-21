import playsound

def play(name,micro = None):
  if micro != None:
    micro.stop()
  path = f"./sound/{name}.wav"
  playsound.playsound(path)
  if micro != None:
    micro.start()
  