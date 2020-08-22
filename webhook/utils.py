import base64
import hashlib
import hmac
import os
import requests

from linetoken.utils import get_token

def verify_line_signature(request):
    channel_secret = os.getenv('LINE_BOT_CHANNEL_SECRET')
    body = request.body.decode('utf-8')
    hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    if 'X-Line-Signature' in request.headers:
        return signature.decode('utf-8') == request.headers['X-Line-Signature']

    return False


def send_reply(message, reply_token):
    r = requests.post('https://api.line.me/v2/bot/message/reply', headers={
        'Content-Type' : 'application/json',
        'Authorization' : f"Bearer {get_token()}"
    }, json={
        'replyToken' : reply_token,
        'messages' : [
            {
                "type" : "text",
                "text" : message
            }
        ]
    })

def get_group_display_name(groupId, userId):
    r = requests.get(f"https://api.line.me/v2/bot/group/{groupId}/member/{userId}", headers={
        'Authorization' : f"Bearer {get_token()}"
    })

    res = r.json()
    return res['displayName']

def get_room_display_name(roomId, userId):
    r = requests.get(f"https://api.line.me/v2/bot/room/{roomId}/member/{userId}", headers={
        'Authorization' : f"Bearer {get_token()}"
    })

    res = r.json()
    return res['displayName']