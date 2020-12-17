import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

from sentimentclassifier import classifier
from sentimentclassifier import remove_noise
from nltk.tokenize import word_tokenize




client = discord.Client()

sad_words=["sad","depressed","unhappy","angry","miserable","despressing"]

starter_negative_responds = [
  "Don't be an asshole",
  "Now this is rude",
  "I don't think that we can go anywhere with that attitude",
   "I don't agree with you",
   "Don't be that guy",
   "Tough day, huh?",
   "I mean is this how you treat your friends",
   "I thought we were friends",
   "I find this approach quite useless"
]

starter_positive_responds = [
  "Oh, this is very kind of you.",
  "Thanks!",
  "Thank you very much!",
   "Actually, I think you are the best.",
   "Be that guy :).",
   "Have an awesome day :).",
   "I guess we will make good friends.",
   "Ohh, that's so sweeeeeet.",
   "Nice approach, well done mate."
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  return json_data[0]["q"]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
     encouragements = db["encouragements"]
     encouragements.append(encouraging_message)
     db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if(len(encouragements)>index):
    del encouragements[index]
    db["encouragements"]: encouragements
  

@client.event
async def on_ready():
  print("We've logged in as {0.user}".format(client))

@client.event
async def on_message(message):

  msg = message.content

  custom_tokens = remove_noise(word_tokenize(msg))
  is_negative = classifier.classify(dict([token, True] for token in custom_tokens))

  if message.author == client.user: 
    return
  
  if message.content.startswith("$hello"):
    await message.channel.send("Hello!")
  
  if message.content.startswith("$inspire"):
    quote =  get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_negative_responds
    
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if is_negative == "Negative":
      await message.channel.send(random.choice(options))
    
    if is_negative == "Positive":
      await message.channel.send(random.choice(starter_positive_responds))

      


  if message.content.startswith("$new"):
    new_message = msg.split("$new ", 1)[1]
    update_encouragements(new_message)

  if message.content.startswith("$del"):
    encouragements = []
    if ("encouragements" in db.keys()):
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if message.content.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]

    await message.channel.send(encouragements)

  if message.content.startswith("$responding"):  
    value = msg.split("$responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Respoding is on...")
    else:
      db["responding"] = False
      await message.channel.send("Respoding is off...")

keep_alive()
client.run(os.getenv("TOKEN"))

