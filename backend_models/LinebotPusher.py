import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * #MessageEvent,TextMessage,ImageSendMessage
import requests
import os

LINEBOT_POST_TOKEN = os.environ.get('LINEBOT_POST_TOKEN')
LINEBOT_POST_LINEID= os.environ.get('LINEBOT_POST_LINEID')

def LinePost(strInfo):  
    userId = LINEBOT_POST_LINEID   
    headers = {'Authorization':'Bearer '+LINEBOT_POST_TOKEN,'Content-Type':'application/json'}
    body = {
    'to':userId,
    'messages':[{
            'type': 'text',
            'text': strInfo
        }]
    }
    # 向指定網址發送 request
    
    #先關閉 否則會超過每月限制 <但此行可用>
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))
    print(req.text)
    return 200