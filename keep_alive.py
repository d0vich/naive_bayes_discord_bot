from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "This Webserver is running to keep a naive bayes agent alive, agent feeds discord bot"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()