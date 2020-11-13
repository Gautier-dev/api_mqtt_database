FROM debian AS builder
ARG DBNAME=${DBNAME}
ARG POSTGRES_USER=${POSTGRES_USER}
ARG POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ARG URL_DB=${URL_DB}
ARG URL_MQTT=${URL_MQTT}
ARG PORT_MQTT=${PORT_MQTT}
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip3 install paho-mqtt
RUN pip3 install psycopg2-binary
RUN pip3 install pyping
COPY . /api/

FROM debian
WORKDIR /api
COPY --from=builder /api ./
CMD ["python3", "mqtt_to_DB.py"]


