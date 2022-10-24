import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * #MessageEvent,TextMessage,ImageSendMessage
import requests
import os

LINEBOT_POST_TOKEN = os.environ.get('LINEBOT_POST_TOKEN')

def LinePost(strInfo):  
    userId = "U28f735e0a0bff2a9e5c6d75bbb4e1411"    
    headers = {'Authorization':'Bearer '+LINEBOT_POST_TOKEN,'Content-Type':'application/json'}
    body = {
    'to':userId,
    'messages':[{
            'type': 'text',
            'text': strInfo
        }]
    }
    # 向指定網址發送 request
    
    #先關閉 否則會爆掉 <但此行可用>
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)
    return 200