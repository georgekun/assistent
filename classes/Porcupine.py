import pvporcupine
from . import config


class Porcupine:
    
    def __init__(self):
      self.porcupine = pvporcupine.create(
            access_key= config.porcupine_access,
            keyword_paths=["./models/porcupine/friday.ppn"],
            model_path='./models/porcupine/porcupine_params_ru.pv',
            sensitivities=[config.sensitiviti])
      print("Поркупине готов.")
  
    def detectWord(self,pcm):
        index = self.porcupine.process(pcm)
        if(index>=0):
          return True
        else: 
          return False
