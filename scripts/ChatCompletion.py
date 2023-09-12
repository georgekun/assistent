import openai
# from classes.TTS import textToSpeech
from ..classes import config
openai.api_key = config.gpt_key

def openaiResponse(request):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content":f"{request}"}
    ],
    temperature=0.7,
  )
  response = completion.choices[0].message.content 
  if(response != None):
    pass
    # textToSpeech(response,"baya")

  


