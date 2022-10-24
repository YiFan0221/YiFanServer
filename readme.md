
# 專案說明
===================
## 此服務用來被LineBot所呼叫。

LineBot : heroku
<br><br />
YiFanServer : Local Server

# 環境參數
## [Environment]
### LINEBOT_POST_TOKEN = {from post token}
### LINEBOT_RECV_TOKEN = {from post token}
### CONNECTSTRING = {mongodb connection string}

<br><br />
# systemctl 日誌

### journalctl : 調閱systemd日誌
> journalctl -u YiFanServer.service

### 僅保留過去兩小時資料
> sudo journalctl --vacuum-time=600s

### 清除日誌資料
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
# Git remote repository fetch:
http登入改為使用token 登入

> $ git clone https://github.com/username/repo.git
### Username: your_username
### Password: your_token

<br><br />
# Cloud MongoDB
> https://cloud.mongodb.com/v2/632d1df8af84ef7bf676ba5d#clusters/connect?clusterId=APILOG0

安裝套件
> python3 -m pip install "pymongo[srv]"

> https://www.mongodb.com/docs/drivers/pymongo/#connect-to-mongodb-atlas

> Connect:
mongodb+srv://user0:<password>@apilog0.amcx94o.mongodb.net/test
