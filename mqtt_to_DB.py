import paho.mqtt.client as mqtt
import psycopg2
import os
import datetime
import yagmail
"""
yag = yagmail.SMTP('gautierbonneappartement@gmail.com', 'prjiot2020')

yag.send(
    to="bonnegaut@gmail.com",
    subject="test",
    contents="bonjour"
)
"""

# Connect to our postgre database
try:
    conn = psycopg2.connect(dbname="info_capteur", user="surveillancedevieux",
                            password="surveillancedevieux", host="surveillancedevieux-postgresql-db.apps.asidiras.dev", port="5432")
except psycopg2.OperationalError as e:
    print("Unable to connect")
    print(e)

# Cursor used to perform database operation
cur = conn.cursor()
cur.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")   
# Take every rows in the cursor and put them into an array

tables = cur.fetchall()
if (tables == []):
    # Create the table used to store the data
    cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, first_name varchar(50), last_name varchar(50), email varchar(50), phone_number varchar(50));")
    cur.execute("CREATE TABLE pathology (id SERIAL PRIMARY KEY, name varchar(50), description varchar(50), id_user INT, FOREIGN KEY(id_user) REFERENCES users(id));")
    cur.execute("CREATE TABLE contact (id SERIAL PRIMARY KEY, first_name varchar(50), last_name varchar(50), email varchar(50), phone_number varchar(50), relationship varchar(50), id_user INT, FOREIGN KEY(id_user) REFERENCES users(id));")
    cur.execute("CREATE TABLE house (id SERIAL PRIMARY KEY, adresse varchar(100), city varchar(50), zip_code varchar(5), id_user INT, FOREIGN KEY(id_user) REFERENCES users(id));")
    cur.execute("CREATE TABLE gateway (id SERIAL PRIMARY KEY, id_house INT, FOREIGN KEY(id_house) REFERENCES house(id));")
    cur.execute("CREATE TABLE sensor (id SERIAL PRIMARY KEY, type varchar(50), id_gateway INT, FOREIGN KEY(id_gateway) REFERENCES gateway(id));")
    cur.execute("CREATE TABLE measure (id SERIAL PRIMARY KEY, data varchar(50), date varchar(20), id_sensor INT, FOREIGN KEY(id_sensor) REFERENCES sensor(id));")

    cur.execute("INSERT INTO users (first_name, last_name, email, phone_number) VALUES (%s,%s,%s,%s)", ("Gautier", "Bonnemaison", "gautier.bonnemaison@gmail.com", "1111111111"))
    cur.execute("INSERT INTO pathology (name, description, id_user) VALUES (%s,%s,%s)", ("Anomalie cardiaque", "Bonjour", 1))
    cur.execute("INSERT INTO contact (first_name, last_name, email, phone_number, relationship, id_user) VALUES (%s,%s,%s,%s,%s,%s)", ("François", "Rault", "francois.rlt@orange.fr", "0000000000", "Friend", 1))
    cur.execute("INSERT INTO house (adresse, city, zip_code, id_user) VALUES (%s,%s,%s,%s)", ("Champ de Mars, 5 Avenue Anatole France", "Paris", "75007", 1))
    cur.execute("INSERT INTO gateway (id_house) VALUES (%s)", (1,))
    cur.execute("INSERT INTO sensor (type, id_gateway) VALUES (%s, %s)", ("cardiaque", 1))
    conn.commit()
    print("Table created")
else:
    print(tables)


        
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("1")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print("Inserted the following data, "+str(msg.payload)+" from "+msg.topic+" into the DB")
    # Add a value into the database
    cur.execute("INSERT INTO Measure (data, date, id_sendor) VALUES (%s,%s,%d)", (str(msg.payload), str(datetime.datetime.now()), 1))
    # Make it persistent
    conn.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("srv-captain--surveillancedevieux-mqtt2", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
cur.close()
conn.close()

print("connection closed")
