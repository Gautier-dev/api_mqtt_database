import paho.mqtt.client as mqtt
import psycopg2
import os




# Connect to our postgre database
try:
    conn = psycopg2.connect(dbname=os.environ['DBNAME'], user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'], host=os.environ['URL_DB'], port="5432")
    print("Connected")
    cur = conn.cursor()
    cur.execute("show tables;")
    tables = cur.fetchall()
    if (tables == []):
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, topic varchar(100), data varchar(100));")
        print("Table created")
    else:
        print(tables)
except:
    print("Unable to connect")


# Cursor used to perform database operation


# Create the table used to store the data


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    cur.execute("INSERT INTO test (topic, data) VALUES (%s,%s)",
                (str(rc), str(rc)))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # Add a value into the database
    cur.execute("INSERT INTO test (topic, data) VALUES (%s,%s)",
                (msg.topic, str(msg.payload)))
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
print("connection close")
