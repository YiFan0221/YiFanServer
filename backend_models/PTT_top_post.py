import time
import requests
from bs4 import BeautifulSoup
rs = requests.session()
#Cookie
cookie='''XSRF-TOKEN=eyJpdiI6ImQ4S2pidDVIY3prbWdPRHVvY01RQmc9PSIsInZhbHVlIjoiR1ROckx2bnNmbEJwanNWQ1FKQldEXC8ydU5NQ2tCa25lWW1cL1RTMzBtVERmcUl2bERiaFRrZFNDbTNNK1A0UWN5IiwibWFjIjoiMTVhNDI2MTRmNTc4ZGM5MWZlZDAzODI3OGQyZDAzZTAzNGE2YTYwYjQ1OTI4Yjk0NTM1NGEzM2U5ODNkZGY0OSJ9; jvid_prod_session=gXIHtW1oTiDEuq0iX4RxmoFiheKqoD3TU8WBFw3F; __auc=1a77c905179cd8c88d30046a28a; _ga=GA1.2.1615784831.1622651210; _gid=GA1.2.1126861238.1622651210; _ga_Q4XDSLQE2E=GS1.1.1622651209.1.0.1622651212.0'''    
PTTHeader = {
    'over18':'1;',
    'method':'GET',
    'scheme':'https',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36','Cookie': cookie}

def over18(URL:str,header):
    res = rs.get(URL,headers=header, timeout = 10,verify=False)
    # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if 'over18' in res.url:
        print("18禁網頁")
        strURL= URL[18:len(URL)]
        
        load = {
            'from': strURL,
            'yes': 'yes'
        }
        res = rs.post('https://www.ptt.cc/ask/over18', timeout = 10, verify=False, data=load)
    return res

def Get_TOP_N_Report(PTT_URL,num,boardname):  
    if(num>20 or num<=0):
        return "超出上限(20筆)囉"
    st='TOP前'+str(num)+'\n'        
    m_data =Func_PTT_TopN(PTT_URL,boardname) 
    
    if type(m_data)==str:
        return m_data
    else:
        for i in range(0,num+3,1):
            data=m_data.pop()
            #濾掉置頂文章,將列表加入列表
            if i>=3:
                st += str(i-2)+':['+data['rate']+'] '+data['title']+' '+data['url']+'\n'            
    print(st)    
    return st
    
def Func_PTT_TopN(PTT_URL,boardname):
    res_Page =over18(PTT_URL,PTTHeader)  
    soup = BeautifulSoup(res_Page.text, 'html.parser')  
    
    #print(soup) 
    #例外情形 返回無資料
    m_error = [tag.text for tag in soup.find_all("div", class_="jsx-3008000365")]
    # R18     = [tag.text for tag in soup.find_all("div", class_="over18-notice")]
    if(soup.title.string== '404' or str(m_error)!='[]'):
        rtn = '找不到相關資訊歐~'
        print(rtn)
        return rtn  
    # elif(str(R18)!='[]'):
    #     rtn = '偵測到R18檢核 開發中'
    #     print(rtn)
    #     return rtn 
    
    URL_List = []
    
    article_list = []
    
    all_page_url = soup.select('.btn.wide')[1]['href']
    End_page = TopN_get_pagenumber(all_page_url)
    #print(End_page)  
    #取預計找尋的頁數
    for page in range(End_page-1, End_page+1, 1):        
        page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(boardname, page)
        #print('URL:'+page_url)
        URL_List.append(page_url)        

    # 抓取 文章標題 網址 推文數
    while URL_List:
        URL = URL_List.pop(0)        
        res =over18(URL ,PTTHeader)   
        soup = BeautifulSoup(res.text, 'html.parser')  
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            #塞回去再來一次
            URL_List.append(URL)
            time.sleep(1)
        else:
            article_list.extend(TopN_GrabPageInfo(res))#往後加入列表
        time.sleep(0.05)

    total = len(article_list)

    print("其他資訊:"+str(article_list))   
    return article_list

#取得當前所有頁數
def TopN_get_pagenumber(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1
#傳入資料網址 取出標題與連結
def TopN_GrabPageInfo(res):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            #print('1') 
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                #print('2') 
                rate = r_ent.find(class_="nrec").text
                title = r_ent.find(class_="title").text.strip()                
                url = 'https://www.ptt.cc' + link
                #print('3') 
                print(rate+title)
                article_seq.append({
                    'title': title,
                    'url': url,
                    'rate': rate,
                })
                #print('4') 
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print(e)        
    return article_seq