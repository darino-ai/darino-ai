from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "darino123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route('/')
def home():
    return 'DARINO OK'

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"DATA: {data}", flush=True)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_number = msg['from']
            text = msg.get('text', {}).get('body', '')
            print(f"Message de {from_number}: {text}", flush=True)

            url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp","to": from_number,"type": "text","text": {"body": f"Salut ! Tu as dit: {text} ✅"}}

            r = requests.post(url, json=payload, headers=headers)
            print(f"=== REPONSE META ===", flush=True)
            print(f"Status: {r.status_code}", flush=True)
            print(f"Body: {r.text}", flush=True)
            print(f"=====================", flush=True)
    except Exception as e:
        print(f"ERREUR PYTHON: {e}", flush=True)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=10000)
