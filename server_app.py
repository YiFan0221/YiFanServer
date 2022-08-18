from flask import Flask, request, render_template ,abort
from flask_cors import CORS
from linebot import  WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * #MessageEvent,TextMessage,ImageSendMessage

import tempfile
from controller import stock_controller, modbus_controller,ssh_controller,tickerOrder_controller

from flasgger import Swagger
from requests import *

#其他後端function
from backend_models.stocksearch import *
from backend_models.picIV       import Pic_Auth
from controller.stock           import *
from controller.tickerOrder     import *
from app_utils.app_result       import requests_api

handler = WebhookHandler('976067291be71b6c3e6a3d5c161db416')

 
Mode = 'setting'

app = Flask(__name__)
app.config['SWAGGER'] = {
    "title": "TeaOrFish",
    "description": "Flasgger by TeaOrFish,stockSearch in Linebot",
    "version": "1.0.2",
    "termsOfService": "",
    "hide_top_bar": True
}
CORS(app)
Swagger(app)

#registering blueprints
#註冊其他藍圖中的controllers
app.register_blueprint(modbus_controller       , url_prefix='/Modbus')
app.register_blueprint(ssh_controller          , url_prefix='/SSH')
app.register_blueprint(stock_controller        , url_prefix='/Stock')
app.register_blueprint(tickerOrder_controller  , url_prefix='/Ticker')
                            

print("..........Flask start!")

@app.route("/")
def home():
  return render_template("home.html")

# @app.route("/callback",methods=['POST'])
# def callback():
#   """
#     接收到LINE發過來的資訊
#     ---
#     tags:
#       - Linebot
#     description:
#       接收到LINE發過來的資訊,並藉此放到@handle中做處理
#     produces: application/json,
#     parameters:
#     - name: name
#       in: path
#       required: true
#       type: string    
#     responses:
#       400:
#         description: InvalidSignatureError
#       200:
#         description: Receive Line request.
#   """
#   signature = request.headers['X-Line-Signature']
#   body = request.get_data(as_text=True)
#   try:
#       handler.handle(body,signature)
#   except InvalidSignatureError:
#       abort(400)
#   return 'OK'

      
def SwitchSettingMode():
  global Mode
  if(Mode == 'setting'):
    Mode = 'normal'
  else :
    Mode = 'setting'
  return '更換為'+Mode
    
def CheckSettingMode():
  global Mode
  if(Mode == 'setting'):
    return True
  else :
    return False
def ShowMode():
  global Mode
  return '現在模式為: '+Mode

      
if __name__ == '__main__':
  #app.run(ssl_context=('/SSL/YiFanServer.crt', '/SSL/YiFanServer.key'),host="0.0.0.0", port=4000 , threaded=True)
  app.run(host="0.0.0.0", port=4000 , threaded=True)
#添加SSL
#https://medium.com/@charming_rust_oyster_221/flask-%E9%85%8D%E7%BD%AE-https-%E7%B6%B2%E7%AB%99-ssl-%E5%AE%89%E5%85%A8%E8%AA%8D%E8%AD%89-36dfeb609fa8
#產生KEY
#https://blog.miniasp.com/post/2019/02/25/Creating-Self-signed-Certificate-using-OpenSSL
#取得授承認的SSL
#https://certbot.eff.org/instructions?ws=other&os=ubuntufocal
#如何在 VSCode 設定完整的 .NET Core 建置、發行與部署工作 看第四點
#https://blog.miniasp.com/post/2019/01/22/Configure-Tasks-and-Launch-in-VSCode-for-NET-Core