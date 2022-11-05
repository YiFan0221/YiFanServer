import time
import requests
from bs4 import BeautifulSoup
rs = requests.session()

from copyheaders import headers_raw_to_dict
from backend_models.PTT_top_post import Get_TOP_N_Report
#抓header教學  https://blog.v123582.tw/2019/12/17/%E5%88%A9%E7%94%A8-Chrome-%E9%96%8B%E7%99%BC%E8%80%85%E5%B7%A5%E5%85%B7%E8%A7%80%E5%AF%9F-HTTP-Headers/
r_h = b'''
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-TW,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5
cache-control: max-age=0
cookie: __gads=ID=47e0715c10ead12f:T=1633485450:S=ALNI_MYh2jMq9I3khZT5fTlQSvP1sAHE_g; _gid=GA1.2.1537933614.1666283312; consentCookie=1666283909608; _ga_Q14GZ4B1PW=GS1.1.1666283312.9.1.1666285071.0.0.0; _ga=GA1.1.253690574.1625671363
dnt: 1
if-none-match: W/"2c4ac-OE3j6txsNxMXIBgc21JSgt8a1yU"
sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
'''
cookie='__gads=ID=47e0715c10ead12f:T=1633485450:S=ALNI_MYh2jMq9I3khZT5fTlQSvP1sAHE_g; _gid=GA1.2.1537933614.1666283312; consentCookie=1666283909608; _gat_UA-145056278-11=1; _gat=1; _gat_proj=1; _gat_cross=1; _gat_global=1; _gat_twstock=1; _ga_Q14GZ4B1PW=GS1.1.1666283312.9.1.1666285065.0.0.0; _ga=GA1.1.253690574.1625671363'
StockHeader =headers_raw_to_dict(r_h)
StockHeader["cookie"] = cookie

def Func_Echo(mtext):
    return mtext

def Func_Stock_PTT_TopN(num):
    print('進入函式:Func_PTTStock_TopN') 
    PTT_URL = "https://www.ptt.cc/bbs/Stock/index.html"
    return Get_TOP_N_Report(PTT_URL,num)
    
def Func_SearchStock_cnyes(StockNum):
    print('進入函式:Func_SearchStock') 
    numstring = str(StockNum)
    link = "https://invest.cnyes.com/twstock/TWS/"+numstring+"/" 
    res_Page = rs.get(link,headers=StockHeader, timeout = 10,verify=False)  
    #PS.例外資訊： socket.timeout: The read operation timed out                  
    soup = BeautifulSoup(res_Page.text, 'html.parser')
    
    #例外情形 返回無資料
    # m_error = [tag.text for tag in soup.find_all("div", class_="jsx-3008000365")]
    m_error = [tag.text for tag in soup.find_all("div", {"class": "jsx-3008000365"})]
    
    m_Name  = [tag.text for tag in soup.find_all("div", {"class": "jsx-652552899 main_subTitle"})]
    belemtchange = len(m_Name)==0
    if(belemtchange==True): #try another
        m_Name  = [tag.text for tag in soup.find_all("div", {"class": "jsx-2625558795 header_second"})]
    belemtchange = len(m_Name)==0
    b404 = soup.title.string== '404'
    bError =  str(m_error)!='[]'
    
    if(b404 or bError or belemtchange):
        rtn=""
        if belemtchange == True:
            rtn += '來源改變，請通知回報錯誤;'
        if b404 == True:
            rtn += '找不到相關資訊;'
        if bError == True:
            rtn += '來源回報錯誤;'
        print(rtn)        
        return rtn

    m_key=[]
    m_Value=[]
    
    #股票編號 
    m_ID = StockNum   
    m_key.append('股票編號')
    m_Value.append(m_ID)
    print("股票編號:"+str(m_ID[0]) )

    #名稱 #jsx-37573986 header_second 也可以
    # m_Name = [tag.text for tag in soup.find_all("div", {"class": "jsx-652552899 main_subTitle"})]   
    
        
    m_key.append('股票名稱')
    m_Value.append(m_Name[0])
    print("股票名稱:"+m_Name[0])     
    
    #現價
    m_Price = [tag.text for tag in soup.find_all("div", {"class": "jsx-2214436525 info-lp"})]
    m_key.append('股票現價')
    m_Value.append(m_Price[0])
    print("股票現價:"+str(m_Price[0]))       

    #漲跌
    m_UpDown = [tag.text for tag in soup.find_all("div", {"class": "jsx-2214436525 change-net"})]
    m_key.append('漲跌')
    m_Value.append(m_UpDown[0])
    print("漲跌:"+str(m_UpDown[0]))  
    
    #漲跌幅
    m_UpDownPercent = [tag.text for tag in soup.find_all("div", {"class": "jsx-2214436525 change-percent"})]
    m_key.append('漲跌幅')
    m_Value.append(m_UpDownPercent[0])
    print("漲跌幅:"+str(m_UpDownPercent[0]))  
            
    #尋訪各項目的元素
    for tag in soup.find_all("div", {"class": "jsx-3874884103 jsx-1763002358 data-block"}):
        Name = [val.text for val in tag.find_all("div", {"class": "jsx-3874884103 jsx-1763002358 block-title"})]
        m_key.append(Name[0])                                       
        value = [val.text for val in tag.find_all("div", {"class": "jsx-3874884103 jsx-1763002358 block-value block-value--"})]
        if len(value) == 0:                              
            value2 = [val.text for val in tag.find_all("div", {"class": "jsx-3874884103 jsx-1763002358 block-value block-value-- block-value--small"})]
            m_Value.append(value2[0])        
        else:
            m_Value.append(value[0])  
    #轉換看這篇:
    #https://blog.csdn.net/loner_fang/article/details/80940600    
    m_data_zip=[]
    m_data_zip = zip(m_key,m_Value)
    m_data_dict = dict(m_data_zip)
    print("其他資訊:"+str(m_data_dict))
    print('離開函式:Func_SearchStock')   
    return m_data_dict
   
   