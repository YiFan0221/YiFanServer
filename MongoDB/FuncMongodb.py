###
# 撰寫來存取MongoDB的函式庫
###


import collections
import os
from enum import Enum, unique
import pprint
import pymongo
username = None
password = None
conn_str = None
import datetime

client =None
db     =None

@unique
class InfoType(Enum):
    APILog_Trade = 'apilog_Trade'
    APILog_Line = 'apilog_Line'
    APILog_Stock = 'apilog_Stock'

#region ------ Common Function------
def ImportUserInfoByENV():
    global conn_str
    conn_str = os.environ.get('CONNECTSTRING')
    return conn_str

def Clientinit():
    global username
    global password
    global client
    global db    
    ImportUserInfoByENV()
    if(conn_str==None):
        return "-1"
    else:
        print("Mongodb connection string : "+conn_str )
    
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
        
    db = client['APILOG']
    
def getDataBase():
    global db
    if(db==None):
        db = client['APILOG']
    else:
        return db
    
def getConnectInfo(Collections:InfoType):
    #DataBase
    global db    
    db = getDataBase()
    #Collections
    collections = db[Collections.value]    
    return collections
    
    
#endregion ------ Common ------

#region ------ Insert ------
   
def Insert_APILog_Trade(text:str):
    return Insert_unit_nonTags(InfoType.APILog_Trade,text)
    
def Insert_APILog_Line(text:str):
    return Insert_unit_nonTags(InfoType.APILog_Line,text)    

def Insert_APILog_Stock(text:str):
    return Insert_unit_nonTags(InfoType.APILog_Stock,text)    
    
def Insert_unit(Collections:InfoType,text:str,Tags:tuple):
    #插入資料庫的根本函式
    
    #connect     
    collections = getConnectInfo(Collections)

    post = {
    "TypeName":Collections.value,
    "text": text,
    "tags": [Collections.value, text],
    "date": datetime.datetime.utcnow(),
    }
    
    post_id = collections.insert_one(post).inserted_id
    # print("post_id:"+str(post_id))
    return post_id

def Insert_unit_nonTags(Collections:InfoType,text:str):
    return Insert_unit(Collections,text,None)

#endregion ------ Insert ------

#region ------ Find ------
def Find_one_byid(Collections:InfoType,post_id):
    #connect     
    collections = getConnectInfo(Collections)
    pprint.pprint(collections.find_one({"_id": post_id}))
        
def Find(Collections:InfoType,SelectItemName:str,SelectItem:str):
    #connect     
    collections = getConnectInfo(Collections)
    for post in collections.find({SelectItemName: SelectItem}):
        pprint.pprint(post)      
        
#endregion ------ Find ------        

#region ------ Delete ------
def delete(Collections:InfoType,SelectItemName:str,SelectItem:str):
    #connect     
    collections = getConnectInfo(Collections)
    query = {SelectItemName: SelectItem}
    d = collections.delete_many(query)
    print(d.deleted_count, " documents deleted !!")
    
    
        
#endregion ------ Delete ------

Clientinit()
id=Insert_unit_nonTags(InfoType.APILog_Line,"TEST message.")
Find(InfoType.APILog_Line,"_id",id)
# delete(InfoType.APILog_Line,"TypeName",InfoType.APILog_Line.value)