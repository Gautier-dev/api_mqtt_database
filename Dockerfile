FROM ubuntu
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install paho-mqtt
RUN pip3 install psycopg2-binary
COPY . /api/
WORKDIR /api
RUN python3 mqtt_to_DB.py


