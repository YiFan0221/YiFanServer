
YiFanServer
===================
作為分散式架構架構中的副服務,

主要展現backend, 爬蟲 crawler build and delivery Docker container

主服務git link: [TeaOrFish](https://github.com/YiFan0221/TeaOrFish)

# 大綱 <a name="top"></a>
### 1. Architecture 1 						[go](#architecture-1)
### 1.1 ---contriner env para 1.1 				[go](#contriner-env-para-11)
### 2. Docker 2 							[go](#docker-2)
### 2.1 ---Docker build and launch 2.1 			[go](#docker-build-and-launch-21)
### 2.2 ---Docker container operation 2.2 		[go](#docker-container-operation-22)
### 2.3 ---Push Docker Image to Docker Hub 2.3 	[go](#push-docker-image-to-docker-hub-23)
### 2.4 ---Docker-compose 2.4 					[go](#docker-compose-24)
### 2.5 ---docker-compose secretes 2.5 			[go](#docker-compose-secretes-25)
### 2.6 ---觀看Logs資訊 2.6 					[go](#觀看logs資訊-26)
### 3.  Daemon 3 								[go](#daemon-3)
### 3.1 ---systemctl 日誌 3.1 					[go](#systemctl-日誌-31)
### 3.2 ---daemon重起手順 3.2 					[go](#daemon重起手順-32)
### 3.3 ---轉發port 3.3 						[go](#轉發port-33)
<br><br />

## Architecture 1
![](/ReadmePic/pic0.jpg)
<br><br />
[Back Top](#top)
<br><br />


## contriner env para 1.1
[Environment]
```
LINEBOT_POST_TOKEN = {from post token}
LINEBOT_RECV_TOKEN = {from post token}
CONNECTSTRING = {mongodb connection string}
TARGET_SERVER_URL = {http://IP or domain :5000}
SSL_PEM = {SSL憑證相對路徑}
SSL_KEY = {SSL私鑰相對路徑}
TEAORFISH_SERVER_PORT = {4000}
YIFANSERV_SERVER_PORT = {5000}
```
<br><br />
[Back Top](#top)
<br><br />

## docker 2
部分基礎操作
若要觀看如何撰寫dockerfile請參考主服務的readme 2.4 2.5 [link](https://github.com/YiFan0221/TeaOrFish?tab=readme-ov-file#write-dockerfilse-24)
<br><br />
[Back Top](#top)
<br><br />

## Docker build and launch 2.1

-t 要建立出的image名稱  
--no-cache 不產生cache
```
sudo docker build --no-cache -t gary80221/yifanserver .
```

標記版本號
```
sudo docker tag <ContainerID> gary80221/yifanserver:\<version>
```

啟動container
```
sudo docker run -e \ 
LINEBOT_POST_TOKEN={} \
LINEBOT_RECV_TOKEN = {} \ 
CONNECTSTRING = {} \
retryWrites=true&w=majority \
--rm --name yifanserver \
-p 4000:4000 \
-p 4000:4000/udp \ 
-i -t gary80221/yifanserver:\<version>
```

<br><br />
[Back Top](#top)
<br><br />

## Docker container operation 2.2
 啟用容器
```
sudo docker start yifanserver
```
進入容器
```
sudo docker attach yifanserver
```
在容器外對容器下命令 示範從外部執行 bash
```
sudo docker exec -it yifanserver /bin/bash
```
停止容器
```
sudo docker stop yifanserver
```
移除容器
```
sudo docker rm yifanserver
```
移除IMAGE
```
sudo docker rmi gary80221/yifanserver:\<version>
or
sudo docker rmi <Image ID>
```
<br><br />
[Back Top](#top)
<br><br />

## Push Docker Image to Docker Hub 2.3
[參考ref] https://ithelp.ithome.com.tw/articles/10192824

Log in
```
sudo docker login
```

push to docker imagehub
```
sudo docker push gary80221/yifanserver:\<version>
```

pull 
```
sudo docker pull gary80221/yifanserver:\<version>
```
<br><br />
[Back Top](#top)
<br><br />


## Docker-compose 2.4

建立網路nat
```
docker network create nat
```

啟用
```
docker-compose up -d
```
or scale up
```
docker-compose up -d --scale yifanserver=3
```


停止
```
docker-compose stop <Service Name>
```
開始
```
docker-compose start <Service Name>
```

移除 將較於up down則是關閉並移除
```
docker-compose down
```

若要開啟3個容器則要再輸入一次
```
docker-compose up -d --scale yifanserver=3
```

<br><br />
[Back Top](#top)
<br><br />

## docker-compose secretes 2.5
在最上層宣告並引入檔案到secretes
```
secrets: 
    SSL_PEM:
        file: {FilePath}
```

在服務內宣告要使用的secretes 並且在環境參數中將對應檔案宣告在環境參數中
```
   environment:      
      LINEBOT_POST_TOKEN: ${LINEBOT_POST_TOKEN}
      LINEBOT_RECV_TOKEN: ${LINEBOT_RECV_TOKEN}     
      TARGET_SERVER_URL : ${TARGET_SERVER_URL}
      SSL_PEM : /run/secrets/SSL_PEM
      SSL_KEY : /run/secrets/SSL_KEY
   secrets:
      - SSL_PEM
      - SSL_KEY
```
<br><br />
[Back Top](#top)
<br><br />

## 觀看Logs資訊 2.6
```
docker-compose logs -f 
```

<br><br />
[Back Top](#top)
<br><br />

## daemon 3
若不使用docker時可使用 systemd來進行服務部屬


<br><br />
[Back Top](#top)
<br><br />

## systemctl 日誌 3.1

journalctl : 調閱systemd日誌
```
journalctl -u YiFanServer.service
```

僅保留過去兩小時資料
```
sudo journalctl --vacuum-time=600s
```

清除日誌資料
```
sudo rm -rf /var/log/journal/*
journalctl -u YiFanServer.service
```

<br><br />
[Back Top](#top)
<br><br />

## daemon重起手順 3.2
如果使用daemon進行部屬的方式
```
sudo rm /etc/systemd/system/YiFanServer.service
sudo cp /home/yifan/文件/YiFanServer/YiFanServer.service /etc/systemd/system/
sudo systemctl stop YiFanServer.service
sudo systemctl daemon-reload
sudo systemctl start YiFanServer.service
sudo systemctl status YiFanServer.service
sudo iptables -t nat -A PREROUTING -p tcp 
--dport 80 -j REDIRECT --to-ports 5000
```

<br><br />
[Back Top](#top)
<br><br />

## 轉發port 3.3
```
 sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 5000
```
<br><br />
[Back Top](#top)
<br><br />


# note
Install [Doc](https://www.mongodb.com/docs/drivers/pymongo/#connect-to-mongodb-atlas)
```
python3 -m pip install "pymongo[srv]"
```
Connect:
```
mongodb+srv://user0:<password>@apilog0.amcx94o.mongodb.net/test
```
[Cloud MongoDB](https://cloud.mongodb.com/v2/632d1df8af84ef7bf676ba5d#clusters/connect?clusterId=APILOG0)

<br><br />
[Back Top](#top)
<br><br />




