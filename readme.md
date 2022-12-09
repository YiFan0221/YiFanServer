
# 專案說明
===================
## 此服務用來被LineBot所呼叫背後主要爬蟲等核心服務。

![](/ReadmePic/pic0.jpg)
### LineBot : AWS/LocalServer

### YiFanServer : AWS/LocalServer


# 所需環境參數
## [Environment]
* LINEBOT_POST_TOKEN = {from post token}
* LINEBOT_RECV_TOKEN = {from post token}
* CONNECTSTRING = {mongodb connection string}
* TARGET_SERVER_URL = {http://IP or domain :5000}
* SSL_PEM = {SSL憑證相對路徑}
* SSL_KEY = {SSL私鑰相對路徑}
* TEAORFISH_SERVER_PORT = {4000}
* YIFANSERV_SERVER_PORT = {5000}

<br><br />
# systemctl 日誌

* journalctl : 調閱systemd日誌
> journalctl -u YiFanServer.service

* 僅保留過去兩小時資料
> sudo journalctl --vacuum-time=600s

* 清除日誌資料
> sudo rm -rf /var/log/journal/*
> journalctl -u YiFanServer.service

<br><br />
# Server 重起手順

> sudo rm /etc/systemd/system/YiFanServer.service

> sudo cp /home/yifan/文件/YiFanServer/YiFanServer.service /etc/systemd/system/

> sudo systemctl stop YiFanServer.service

> sudo systemctl daemon-reload

> sudo systemctl start YiFanServer.service

> sudo systemctl status YiFanServer.service

> sudo iptables -t nat -A PREROUTING -p tcp 
--dport 80 -j REDIRECT --to-ports 5000

<br><br />
# 轉發port
> sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 5000

<br><br />
Docker 相關說明
=============

指令說明
-------------


* Docker build  -t 要建立出的image名稱  --no-cache 從頭執行
> sudo docker build --no-cache -t gary80221/yifanserver .

* 添加版本號
> sudo docker tag <ContainerID> gary80221/yifanserver:\<version>

* 將Image 作為容器

> sudo docker run -e LINEBOT_POST_TOKEN={} LINEBOT_RECV_TOKEN = {} CONNECTSTRING = {}
retryWrites=true&w=majority --rm --name yifanserver -p 4000:4000 -p 4000:4000/udp -i -t gary80221/yifanserver:\<version>

* 啟用容器
> sudo docker start yifanserver

* 進入容器
> sudo docker attach yifanserver

* 在容器外對容器下命令 示範從外部執行 bash
> sudo docker exec -it yifanserver /bin/bash

<br><br />

## 移除容器與IMAGE
* 停止容器
> sudo docker stop yifanserver
* 移除容器
> sudo docker rm yifanserver
* 移除IMAGE
> sudo docker rmi gary80221/yifanserver:\<version>

<br><br />
上傳 Docker Image 到 Docker Hub
=============================

1. 先登入
> sudo docker login

2. 推送到docker imagehub
> sudo docker push gary80221/yifanserver:\<version>

3. 到別台電腦在拉下來
> sudo docker pull gary80221/yifanserver:\<version>

<br><br />
Docker compose
=============================
* 建立網路nat
> docker network create nat

* 安裝swarm
> docker swarm init

* 建立 並使用三個容器分攤 (類似docker的run)
> docker-compose up -d --scale yifanserver=3

* 停止
> docker-compose stop {name}

* 開始
> docker-compose start {name}

* 移除 將較於up是建立 down則是移除 
> docker-compose down
* 若要開啟3個容器則要再輸入一次 --scale > 
> docker-compose up -d --scale yifanserver=3

<br><br />
Docker compose env傳遞
=============================

* 直接讀取 .env檔案
>    environment:

>      CONNECTSTRING: ${CONNECTSTRING}
>      LINEBOT_POST_TOKEN: ${LINEBOT_POST_TOKEN}
>      LINEBOT_RECV_TOKEN: ${LINEBOT_RECV_TOKEN}   
  
<br></br>
### 使用secretes 存取機密檔案
* 在最上層宣告並引入檔案到secretes
> secrets:
> 
> {縮排*1} SSL_PEM:
>
> {縮排*2} file: {當前要存取檔案的路徑}
>
* 在服務內宣告要使用的secretes 並且在環境參數中將對應檔案宣告在環境參數中
>   environment:      

>      LINEBOT_POST_TOKEN: ${LINEBOT_POST_TOKEN}
>      LINEBOT_RECV_TOKEN: ${LINEBOT_RECV_TOKEN}     
>      TARGET_SERVER_URL : ${TARGET_SERVER_URL}
>      SSL_PEM : /run/secrets/SSL_PEM
>      SSL_KEY : /run/secrets/SSL_KEY

>    secrets:

>      - SSL_PEM
>      - SSL_KEY

* 觀看Logs資訊
> docker-compose logs -f 



<br><br />
# Git remote repository fetch:
http登入改為使用token 登入

> $ git clone https://github.com/username/repo.git
* Username: your_username
* Password: your_token

<br><br />
# Cloud MongoDB
> https://cloud.mongodb.com/v2/632d1df8af84ef7bf676ba5d#clusters/connect?clusterId=APILOG0

安裝套件
> python3 -m pip install "pymongo[srv]"

> https://www.mongodb.com/docs/drivers/pymongo/#connect-to-mongodb-atlas

> Connect:
mongodb+srv://user0:<password>@apilog0.amcx94o.mongodb.net/test
