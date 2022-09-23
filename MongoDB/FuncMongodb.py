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


def Clientinit():
    global client
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server.")
        
    db = client['APILOG']

def Insert_one():
    db = client['APILOG']
    post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
    if(db==None):
        return False
    else:
        posts = db.posts
        post_id = posts.insert_one(post).inserted_id
        print("post_id:"+str(post_id))
        return post_id
        
        
    