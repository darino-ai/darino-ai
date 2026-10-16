import os
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "darino123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/")
def home():
    return "DARINO AI est en ligne 🚀"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erreur verification", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            msg = entry["messages"][0]
            from_number = msg["from"]
            text = msg["text"]["body"]
            reponse = f"Salut ! Ici DARINO AI 🚀 Tu as dit : {text}"
            url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp","to": from_number,"text": {"body": reponse}}
            requests.post(url, headers=headers, json=payload)
    except Exception as e:
        print(e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
