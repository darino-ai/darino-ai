from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
PHONE_ID = "1359401900590472"
VERIFY_TOKEN = "darino123"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Erreur", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = msg['from']
        text = msg['text']['body']
        reponse = f"Salut! C'est DARINO AI 🤖 de Kinshasa!\n\nTu as dit: '{text}'\n\nJe suis prêt! Dis-moi ton business?"
        url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        payload = {"messaging_product": "whatsapp","to": from_number,"text": {"body": reponse}}
        requests.post(url, headers=headers, json=payload)
    except: pass
    return "OK", 200

@app.route('/')
def home():
    return "DARINO AI en ligne!"

if __name__ == '__main__':
    app.run(port=10000)
