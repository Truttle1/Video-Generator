import os
import openai
import json

openai.api_key = "API KEY HERE"

count = 0

while count < 1000:
    
    video = open("scripts/"+str(count)+".txt","r")
    content = video.read()
    video.close()
    
    mimic = open("dinoworld_mimic.txt","r")
    intro = mimic.read()
    mimic.close()
    
    response = openai.Completion.create(
      engine="curie",
      prompt=intro+content+"\nVIDEO TITLE:",
      temperature=0.4,
      max_tokens=64,
      top_p=1,
      frequency_penalty=0.4,
      presence_penalty=0.25,
      stop="###"
    )


    txt = response["choices"][0]["text"]
    print(txt)
    f = open("titles/"+str(count)+".txt", "a")
    f.write(txt)
    print("DONE")
    f.close()
    count += 1