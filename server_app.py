from flask import Flask, request, render_template ,abort
from flask_cors import CORS
from linebot import  WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import * #MessageEvent,TextMessage,ImageSendMessage
import tempfile
from controller import stock_controller, modbus_controller,other_controller,tickerOrder_controller
from flasgger import Swagger
from requests import *

#其他後端function
from backend_models.stocksearch import *
#from backend_models.picIV       import Pic_Auth
from controller.stock           import *
from controller.other           import *
#from controller.tickerOrder     import *
from app_utils.app_result       import requests_api
from MongoDB.FuncMongodb        import *

print("[Inital][ENV]")
LINEBOT_POST_TOKEN  = os.environ.get('LINEBOT_POST_TOKEN')
LINEBOT_RECV_TOKEN  = os.environ.get('LINEBOT_RECV_TOKEN')
CONNECTSTRING       = os.environ.get('CONNECTSTRING')
SSL_PEM             = os.environ.get('SSL_PEM')
SSL_KEY             = os.environ.get('SSL_KEY')
SERVER_PORT         = os.environ.get('YIFANSERV_SERVER_PORT')

# print("ENV:Mongodb_ConnString : "+CONNECTSTRING )
print("ENV:LINEBOT_RECV_TOKEN : "+LINEBOT_RECV_TOKEN )
print("ENV:SERVER_PORT        : "+str(SERVER_PORT) )
print("ENV:SECRETS_SSL_PEM    : "+str( os.path.exists("/run/secrets/SSL_PEM") ))
print("ENV:SECRETS_SSL_KEY    : "+str( os.path.exists("/run/secrets/SSL_KEY") ))
print("ENV:SSL_PEM            : "+str( SSL_PEM))
print("ENV:SSL_KEY            : "+str( SSL_KEY))

handler = WebhookHandler(LINEBOT_RECV_TOKEN)

Mode = 'setting'

print("[Inital][Swagger]")
app = Flask(__name__)
#(OpenAPI 3.0) 擇一
app.config['SWAGGER'] = {
    "title": "YiFanServer",
    "description": "Backend server of get linebot request.",
    "version": "1.0.0",
    'openapi': '3.0.1',
    "termsOfService": "",
    "hide_top_bar": False
}
CORS(app)
Swagger(app)

print("[Inital][blueprints]")
#registering blueprints  #註冊其他藍圖中的controllers
app.register_blueprint(modbus_controller       , url_prefix='/Modbus')
app.register_blueprint(stock_controller        , url_prefix='/Stock')
app.register_blueprint(other_controller        , url_prefix='/Other')
app.register_blueprint(tickerOrder_controller  , url_prefix='/Ticker')
                            
print("[Inital][MongoDB]")
Clientinit()

@app.route("/")
def home():
  return render_template("home.html")
            
import ssl

print("[Finnish].......... Backend service start!")      
if __name__ == '__main__':
  context = ssl.SSLContext()
  if(SSL_PEM!=None and SSL_KEY!=None):
    print("[Inital][SSL]")                 
    context.load_cert_chain(SSL_PEM,SSL_KEY)    
    app.run(ssl_context=context,host="0.0.0.0" ,port=int(SERVER_PORT), threaded=True)  
  else:    
    app.run(host="0.0.0.0" ,port=int(SERVER_PORT), threaded=True)  
  