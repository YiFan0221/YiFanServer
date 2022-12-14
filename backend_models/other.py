import time
import requests
rs = requests.session()
from backend_models.PTT_top_post import Get_TOP_N_Report


def Func_Gossiping_PTT_TopN(num):
    PTT_URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
    return Get_TOP_N_Report(PTT_URL,num,"Gossiping")
    
