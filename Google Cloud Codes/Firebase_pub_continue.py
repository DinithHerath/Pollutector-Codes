import datetime
import pytz
import os
import time
import json
import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt
import ast
from google.cloud import firestore

def on_connect(client, userdata, flags, rc):  # on connect interrupt
    print("Connected With Result Code", (rc))


def on_disconnect(client, userdata, rc):  # on disconnect interrupt
    print("Client Got Disconnected")


def on_message(client, userdata, message):  # on message interrupt
    collect_data(message.payload)


def collect_data(data):
    try:
        decode = ast.literal_eval(data.decode("utf-8"))
        print(decode)
        doc_ref = db.collection(u'Pollutector - 04/Continuous Mode/Continuous Data').document()
        doc_ref_temp = db.collection(u'Pollutector - 04').document(u'Continuous Mode')
        # timenow = datetime.now(pytz.timezone("Asia/Colombo")).strftime("%d/%m/%Y %H:%M:%S")
        timenow = datetime.datetime.now()
        doc_ref.set({
            u'Time': timenow,
            u'Temperature': float(decode['Temperature']),
            u'Humidity': float(decode['Humidity']),
            u'Gas Value': float(decode['GasSensorValue']),
            u'PM2.5': float(decode['PM2.5']),
            u'AQI': int(decode['AQI'])
        })
        doc_ref_temp.set({
            u'Time': timenow,
            u'Temperature': float(decode['Temperature']),
            u'Humidity': float(decode['Humidity']),
            u'Gas Value': float(decode['GasSensorValue']),
            u'PM2.5': float(decode['PM2.5']),
            u'AQI': int(decode['AQI'])
        }) 
    except Exception as ex:
        print(ex)

# Global variables
broker_url = "broker.hivemq.com"  # mqtt broker URI
broker_port = 1883  # broker port
db = firestore.Client()

print("Welcome to pollutector firebase script for google cloud......")
client = mqtt.Client()  # defining client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(broker_url, broker_port)  # connect using this port
client.subscribe("pollutector/outgoing/continuous", qos=1)
client.loop_forever()


