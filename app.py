from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "darino123"
TOKEN = os.environ.get("TOKEN")
PHONE_ID = "1359401900590472"

@app.route('/')
def home():
    return "DARINO AI en ligne!"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erreur", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = msg['from']
        text = msg['text']['body']
        print(f"Message de {from_number}: {text}")
    except:
        pass
    return "ok", 200
