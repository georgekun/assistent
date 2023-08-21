import pvrecorder
class Record:
  def __init__(self):
    self.record = pvrecorder.PvRecorder(device_index=-1,frame_length=512)
    print("Микрофон подключён.")


  def start(self):
    self.record.start()

  def stop(self):
    self.record.stop()

  def read(self):
    return self.record.read()

