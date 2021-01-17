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
<<<<<<< HEAD
    print(os.environ['DBNAME'],os.environ['POSTGRES_USER'], os.environ['POSTGRES_PASSWORD'], os.environ['URL_DB'])
    conn = psycopg2.connect(dbname=os.environ['DBNAME'], user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'], host=os.environ['URL_DB'], port=os.environ['DBPORT'])
=======
    conn = psycopg2.connect(dbname="info_capteur", user="surveillancedevieux",
                            password="surveillancedevieux", host="surveillancedevieux-postgresql-db.apps.asidiras.dev", port="5432")
>>>>>>> 7cae60869519630cc7c69e74ee9ac1cdea5af1da
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
    cur.execute("CREATE TABLE User (id serial PRIMARY KEY, first_name varchar(50), last_name varchar(50), email varchar(50), phone_number varchar(50));")
    cur.execute("CREATE TABLE Pathology (id serial PRIMARY KEY, name varchar(50), description varchar(50), FOREIGN KEY id_user REFERENCES User(id));")
    cur.execute("CREATE TABLE Contact (id serial PRIMARY KEY, first_name varchar(50), last_name varchar(50), email varchar(50), phone_number varchar(50), relationship varchar(50), FOREIGN KEY id_user REFERENCES User(id));")
    cur.execute("CREATE TABLE House (id serial PRIMARY KEY, adresse varchar(100), city varchar(50), zip_code varchar(5), FOREIGN KEY id_user REFERENCES User(id));")
    cur.execute("CREATE TABLE Gateway (id serial PRIMARY KEY, FOREIGN KEY id_house REFERENCES House(id));")
    cur.execute("CREATE TABLE Sensor (id serial PRIMARY KEY, type varchar(50), FOREIGN KEY id_gateway REFERENCES Gateway(id));")
    cur.execute("CREATE TABLE Measure (id int PRIMARY KEY, data varchar(50), date varchar(20), FOREIGN KEY id_sensor REFERENCES Sensor(id));")

    cur.execute("INSERT INTO User (first_name, last_name, email, phone_number) VALUES (%s,%s,%s,%s)", ("Gautier", "Bonnemaison", "gautier.bonnemaison@gmail.com", "1111111111"))
    cur.execute("INSERT INTO Pathology (name, description, id_user) VALUES (%s,%s,%d)", ("Anomalie cardiaque", "Bonjour", 1))
    cur.execute("INSERT INTO Contact (first_name, last_name, email, phone_number, relationship, id_user) VALUES (%s,%s,%s,%s,%d)", ("François", "Rault", "francois.rlt@orange.fr", "0000000000", 1))
    cur.execute("INSERT INTO House (adresse, city, zip_code, id_user) VALUES (%s,%s,%s,%d)", ("Champ de Mars, 5 Avenue Anatole France", "Paris", "75007", 1))
    cur.execute("INSERT INTO Gateway (id_house) VALUES (%d)", (1))
    cur.execute("INSERT INTO Sensor (type, id_gateway) VALUES (%s, %d)", ("cardiaque", 1))

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

client.connect(os.environ['URL_MQTT'], int(os.environ['PORT_MQTT']), 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
cur.close()
conn.close()

print("connection closed")
