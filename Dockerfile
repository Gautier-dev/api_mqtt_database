FROM ubuntu
RUN apt-get install python3
RUN apt-get install python3-pip
RUN pip3 install paho-mqtt
RUN pip3 install psycopg2-binary
ADD . /api/
WORKDIR /api
RUN python3 mqtt_to_DB.py


