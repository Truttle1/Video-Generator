import os
import openai
import json

openai.api_key = "API KEY HERE"

count = 38

while count < 42:
    
    intro = "This is a video script. Now on with the video."
    response = openai.Completion.create(
      engine="davinci",
      prompt=intro,
      temperature=0.4,
      max_tokens=900,
      top_p=1,
      frequency_penalty=.8,
      presence_penalty=0.25
    )


    txt = intro + response["choices"][0]["text"]
    print(txt)
    f = open("scripts/"+str(count)+".txt", "a")
    f.write(txt)
    print("DONE")
    f.close()
    count += 1