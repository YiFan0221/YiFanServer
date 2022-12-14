from . import stock_controller as controller
from typing import Any
from flask import request
import json , logging , string
from backend_models.PTT_top_post import *
from backend_models.other import *

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
#endregion -------------共用函式-------------    

#region -----------API 框架範例-------------
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
#endregion -----------API 框架範例-------------

#region ------ Get_TOP_N_Report ------
 # GET Get_TOP_N_Report:#Get top post of ptt stock. Range:[ 0 - 40 ]
@controller.route('/Get_TOP_N_Report', methods=["GET"])
def api_get_Gossiping_top_n_report():  
    eventName:str    = 'text'    
    eventSDKAPI:function =Func_Gossiping_PTT_TopN  
    expectType:type      = int#int or bool
    
    status=FuncGetFormValue(expectType,eventName)
    Logst = FuncEventLog(eventName,request.method,eventName,status)    
    print(Logst)
    returnStr = FuncEventExecSDK(eventSDKAPI,status)
    return result_json(200, returnStr)

#endregion ------ Get_TOP_N_Report ------
  