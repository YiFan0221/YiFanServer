import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * #MessageEvent,TextMessage,ImageSendMessage
import requests

line_bot_api = LineBotApi('QcRH4+cmpgKeP24rDsHblYBgd0qkifKrgJem7GxmHyXCYLvOdZqsUkLFASyAYhjRAiFkeiY8AYd+aF2fW9Zn1FcUc9QBB4AK7AATm1MVc47orHkod3ZAm8hAOsGOLcoSy1XeyZuk+2fN8Afccu97EwdB04t89/1O/w1cDnyilFU=')

def LinePost(strInfo):  
    CHANNEL_ACCESS_TOKEN = 'QcRH4+cmpgKeP24rDsHblYBgd0qkifKrgJem7GxmHyXCYLvOdZqsUkLFASyAYhjRAiFkeiY8AYd+aF2fW9Zn1FcUc9QBB4AK7AATm1MVc47orHkod3ZAm8hAOsGOLcoSy1XeyZuk+2fN8Afccu97EwdB04t89/1O/w1cDnyilFU='
    userId = "U28f735e0a0bff2a9e5c6d75bbb4e1411"    
    headers = {'Authorization':'Bearer '+CHANNEL_ACCESS_TOKEN,'Content-Type':'application/json'}
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