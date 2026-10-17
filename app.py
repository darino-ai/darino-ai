from flask import Flask, request
import requests, os
app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN","darino123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route('/')
def home(): return 'DARINO OK'

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.verify_token")==VERIFY_TOKEN:
        return request.args.get("hub.challenge"),200
    return "Forbidden",403

@app.route('/webhook', methods=['POST'])
def webhook():
    data=request.get_json()
    try:
        value=data['entry'][0]['changes'][0]['value']
        if 'messages' in value:
            msg=value['messages'][0]
            frm=msg['from']
            txt=msg.get('text',{}).get('body','')
            url=f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
            headers={"Authorization":f"Bearer {WHATSAPP_TOKEN}","Content-Type":"application/json"}
            payload={"messaging_product":"whatsapp","to":frm,"type":"text","text":{"body":f"Salut ! Tu as dit: {txt} ✅ DARINO marche !"}}
            r=requests.post(url,json=payload,headers=headers)
            print(f"Status {r.status_code} - {r.text}")
    except Exception as e: print(e)
    return "OK",200
