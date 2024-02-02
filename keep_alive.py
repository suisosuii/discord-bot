from flask import Flask
from threading import Thread
import logging

app = Flask('')

@app.route('/')
def home():
    app.logger.info("I'm alive")
    return "I'm alive"

def run():
    logging.basicConfig(filename='server.log', level=logging.INFO)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()