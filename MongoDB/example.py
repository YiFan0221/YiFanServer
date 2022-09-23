import collections
import pprint
import pymongo
username = "user0"
password = "gary80221"
conn_str = "mongodb+srv://"+username+":"+password+"@apilog0.amcx94o.mongodb.net/test?retryWrites=true&w=majority"
import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

client =None
db     =None

#region ------ Common ------
def Clientinit():
    global client
    global db
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
#endregion ------ Common ------

#region ------ Insert ------
def Insert_one():
    db = getDataBase()
    post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
    collection = "apilog_fromLinebot"
    if(db==None):
        return False
    else:
        apilog = db[collection]
        post_id = apilog.insert_one(post).inserted_id
        print("post_id:"+str(post_id))
        return post_id

#endregion ------ Insert ------

#region ------ Find ------
def Find_one(post_id):
    db = getDataBase()
    if(db==None):
        return print("Find nothing.")
    else:
        apilog = db.apilog_fromLinebot    
        pprint.pprint(apilog.find_one({"_id": post_id}))
        
def Find(author):
    db = getDataBase()
    if(db==None):
        return print("Find nothing.")
    else:
        apilog = db.apilog_fromLinebot    
        for post in apilog.find({"author": author}):
            pprint.pprint(post)      
        
#endregion ------ Find ------        

#region ------ Delete ------
def delete(author):
    db = getDataBase()
    if(db==None):
        return print("Find nothing.")
    else:
        col=db["apilog_fromLinebot"]
        query = {"author": author}
        d = col.delete_many(query)
        print(d.deleted_count, " documents deleted !!")
        
#endregion ------ Delete ------
Clientinit()
id=Insert_one()
Find_one(id)
Find("Mike")
delete("Mike")