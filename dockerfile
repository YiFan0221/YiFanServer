FROM python:3.8-slim as build 

COPY . /
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "./server_app.py" ]

#ping
EXPOSE 22
EXPOSE 5000
 
