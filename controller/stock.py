from . import stock_controller as controller
from typing import Any
from flask import request
import json , logging , string
from backend_models.stocksearch import *
from backend_models.PTT_top_post import *
from backend_models.LinebotPusher import *
from app_utils.app_result import result_json
#-------------共用函式-------------
from enum import Enum, unique

from MongoDB.FuncMongodb import *
    
@unique
class BodyType(Enum):
    applicationjson = 'multipart/form-data'
    multipartformdata = 'application/json'
    
#region -------------共用函式-------------    
def FuncGetFormValue(DataType:type , EventName,):
    #TODO def FuncGetFormValue(DataType:type,EventName,)
    #根據傳入種類找尋網頁中屬於{EventName}的值
    #並嘗試轉換成所需的型態{DataType}並回傳

    #從Body取值
    getData:Any = None
    if request.content_type!= None:
      if request.content_type.startswith('application/json'):         
          data = json.loads(request.data)
          getData = data[EventName]   
          
      elif request.content_type.startswith('multipart/form-data'):
          getData=request.form.get(EventName) 
    
    else:
          return None

    #將值依照所需轉型並回傳
    if DataType==int:
        return int(getData)
    elif DataType==string:
        return str(getData)
    else:
        return None

def FuncEventLog(EventName,GETPOST):
    #TODO def FuncEventLog(EventName,GETPOST):
    #使用傳入的Post/Get種類{GETPOST}，與事件名稱{EventName}
    #ex : 'a [GET] [camera device list] event'
    st = 'a '+GETPOST+' ['+EventName+'] event'
    logging.info(st)    
    return st
    
def FuncEventLog(EventName,GETPOST,Para,Value):
    #TODO def FuncEventLog(EventName,GETPOST):
    #使用傳入的Post/Get種類{GETPOST}，與事件名稱{EventName}
    #ex : 'a [GET] [camera device list] event'
    st = 'a '+GETPOST+' ['+EventName+'] event >>{'+ Para + ":" + str(Value) +"}"
    logging.info(st)    
    return st

def FuncEventExecSDK(EventSDKAPI,*args):
    #TODO def FuncEventExecSDK(EventSDKAPI,*args):
    #執行所登入的SDK(或其他)函式
    TestMode = False
    if(TestMode==True): #測試用尚未實裝
        return #這編寫回傳200
    if args==():#沒帶參數值時直接執行函式
        return EventSDKAPI() 
    else:#有帶參數值時將參數帶入函式執行
        return EventSDKAPI(*args)
#endregion  -------------共用函式-------------        
    
#region -------------API 框架範例-------------
# <{}為說明Hint {}內為前者說明>
#TODO#207{API No.}-set sharpness value{API名稱} #0-100{數值合法範圍}
# @controller.route('sharpness_color'{URL}, methods=["POST"]{GET/POST})
# def set_image_sharpness():{函式名稱}
#     #-------------------新增API所需登記項目--------------------------
#     eventName:str        = 'sharpness_color'{API名稱/Body名稱}
#     eventSDKAPI:function = camera.set_image_sharpness{要執行的函式(SDK Function)}
#     
#     min:int              = 0{收到數值的合法範圍最小值}
#     max:int              = 100{收到數值的合法範圍最大值}
#     expectType:type      = int{收到數值期望後送的型態}    
#     returnStr_200        = "Success"  {回應訊息:成功200}
#     returnStr_400        = "Please check paras or query valid."  {回應訊息:成功400}
#     #-------------------此處以下不需更動直接套用即可-------------------
#     FuncEventLog(eventName,request.method){將收到的事件存成訊息}
#     status=FuncGetFormValue(expectType,eventName) {嘗試從Body取出資訊並轉型}
#     if min<= status <= max:{部分邏輯判斷}
#       FuncEventExecSDK(eventSDKAPI,status){執行預先登記好的函式}
#       return result_json(200, returnStr_200)
#     else:
#       return result_json(400, returnStr_400)
#endregion -------------API 框架範例-------------

#region ------ Get_TOP_N_Report ------
 # GET Get_TOP_N_Report:#Get top post of ptt stock. Range:[ 0 - 40 ]
@controller.route('/Get_TOP_N_Report', methods=["GET"])
def api_get_get_top_n_report():  
    eventName:str    = 'text'    
    eventSDKAPI:function =Func_Stock_PTT_TopN  
    expectType:type      = int#int or bool
    
    status=FuncGetFormValue(expectType,eventName)
    Logst = FuncEventLog(eventName,request.method,eventName,status)    
    print(Logst)
    returnStr = FuncEventExecSDK(eventSDKAPI,status)
    return result_json(200, returnStr)

#endregion ------ Get_TOP_N_Report ------

@controller.route('/LINEPost', methods=["POST"])
def Post_LINE():  
  """
    主動推送資訊到LINEBOT
    ---
    tags:
    - Common API
    summary: 主動推送資訊到LINEBOT
    description: 主動推送資訊到LINEBOT
    requestBody:
      description: 要推送的資料
      content:
        application/json:
          schema:
            type: object
            properties:
              text:
                type: string
                example: Hi~this from YiFanServer.swagger
      required: true
    responses:
      200:
        description: Success
        content: {}
      400:
        description: Please check paras or query valid.
        content: {}
    x-codegen-request-body-name: body
  """
  
  
  # """
  #   推送資訊到LINEBOT (Swagger 2.0)
  #   ---
  #   tags:
  #   -   Common API
  #   description: 
  #   -   主動推送資訊到LINEBOT

  #   consumes:
  #   -   application/json
  #   parameters:
  #   -   name: EchoInfo
  #       description: 要推送的資料
  #       required: true
  #       in: body        
  #       schema:
  #       properties:
  #           text:                
  #               type: string                
  #               example: Hi~this from YiFanServer.swagger
  #       required:
  #           - text            

  #   responses:
  #     200:
  #       description: Success   
  #     400:
  #       description: Please check paras or query valid.
  # """     
  eventName:str    = 'text'
  eventSDKAPI:function =LinePost
  expectType:type      = string#int or bool
  returnStr            = ""
  returnStr_200        = "Success"
  returnStr_400        = "Please check paras or query valid."
  status=FuncGetFormValue(expectType,eventName)
  Logst = FuncEventLog(eventName,request.method,eventName,status)
  print(Logst)
  Insert_APILog_Linebot(Logst)
  returnStr = FuncEventExecSDK(eventSDKAPI,status)
  return result_json(200, returnStr)
    
@controller.route('/Echo', methods=["POST"])
def set_Echo():  
  
  """
    回應與傳入資訊相同的資料 (open api)
    ---
    tags:
    - Common API
    summary: 回應與傳入資訊相同的資料
    description: 回應與傳入資訊相同的資料，通常用在LINEBOT測試
    requestBody:
      description: 回應與傳入資訊相同的資料，通常用在LINEBOT測試
      content:
        application/json:
          schema:
            type: object
            properties:
              text:
                type: string
                example: Hi~YiFanServer
      required: true
    responses:
      200:
        description: Success
        content: {}
      400:
        description: Please check paras or query valid.
        content: {}
    x-codegen-request-body-name: body
  """
  
  # """
  #   回應與傳入資訊相同的資料 (Swagger 2.0)
  #   ---
  #   tags:
  #   -   Common API
  #   description: 
  #   -   回應與傳入資訊相同的資料，通常用在LINEBOT測試

  #   consumes:
  #   -   application/json
  #   parameters:
  #   -   name: EchoInfo
  #       description: 輸入需要被回傳的資訊
  #       required: true
  #       in: body        
  #       schema:
  #       properties:
  #           text:                                
  #               type: json
  #               example: Hi~YiFanServer
  #       required:
  #           - text            

  #   responses:
  #     200:
  #       description: Success   
  #     400:
  #       description: Please check paras or query valid.
  # """     
  eventName:str    = 'text'  
  eventSDKAPI:function =Func_Echo
  expectType:type      = string#int or bool
  returnStr            = ""
  returnStr_200        = "Success"
  returnStr_400        = "Please check paras or query valid."
  status=FuncGetFormValue(expectType,eventName)
  Logst = FuncEventLog(eventName,request.method,eventName,status)
  print(Logst)  
  Insert_APILog_Linebot(Logst)
  returnStr = FuncEventExecSDK(eventSDKAPI,status)
  return result_json(200, returnStr)
  
@controller.route("/SearchStock",methods=['POST']) 
def Get_SearchStock():
      #關於在GET請求中使用body【不建議在GET請求中使用body】
      #https://www.796t.com/content/1564528803.html
      
  """
    搜尋對應的股票資訊(爬蟲)
    ---
    tags:
    - Stock
    summary: 搜尋對應的股票資訊(爬蟲)
    description: 搜尋對應的股票資訊(爬蟲)
    requestBody:
        description: 要查詢的股票代號
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                  example: 2330
        required: true
    responses:
      200:
        description: Success
        content: {}
      400:
        description: Please check paras or query valid.
        content: {}
    x-codegen-request-body-name: body
  """     
      
  # """
  #   搜尋對應的股票資訊(爬蟲) (Swagger 2.0)
  #   ---
  #   tags:
  #     - Stock
  #   description:
  #     搜尋股票資訊(爬蟲版)    
  #   consumes:
  #   -   application/json
  #   parameters:
  #   -   name: EchoInfo
  #       description: 需要搜尋的股票代號
  #       required: true
  #       in: body        
  #       schema:
  #       properties:
  #           text:                                
  #               type: json
  #               example: 2330
  #       required:
  #           - text           
  
  #   responses:
  #     400:
  #       description: InvalidSignatureError
  #     200:
  #       description: Receive Line request.
  # """
  eventName:str    = 'text'  
  eventSDKAPI:function =Func_SearchStock_cnyes
  expectType:type      = string#int or bool
  returnStr            = ""
  returnStr_200        = "Success"
  returnStr_400        = "Please check paras or query valid."
  status=FuncGetFormValue(expectType,eventName)
  Logst = FuncEventLog(eventName,request.method,eventName,status)
  Insert_APILog_StockSearchlog(Logst)
  print(Logst)
  returnStr = FuncEventExecSDK(eventSDKAPI,status)
  
  m_data =returnStr
  if(type(m_data)== str):
      rtn_text =m_data
  else:
      st=(
      '股票名稱:'+m_data.get('股票名稱')+' ('+m_data.get('股票編號')+')\n'+
      '股票現價:'+m_data.get('股票現價')+'\n'+                         
      '漲跌:'+m_data.get('漲跌')+' ('+m_data.get('漲跌幅')+')\n'     
      # '昨收:'+m_data.get('昨收')+' 開盤:'+m_data.get('開盤')+' 收盤:'+m_data.get('收盤')+'\n'
      
      # '本益比:'+m_data.get('本益比')+'\n'+     
      # '本淨比:'+m_data.get('本淨比')+'\n'+     
      )
      rtn_text=st    
  return result_json(200, rtn_text)

