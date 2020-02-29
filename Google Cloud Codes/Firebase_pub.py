import datetime
from datetime import datetime
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
    collect_data(message.payload, message_count)


def collect_data(data, message_count):
    try:
        decode = ast.literal_eval(data.decode("utf-8"))
        # print(decode)
        if (len(temperature_data) < 20):
            temperature_data.append(float(decode['Temperature']))
            humidity_data.append(float(decode['Humidity']))
            gas_sensor.append(float(decode['GasSensorValue']))
            dust.append(float(decode['PM2.5']))
            aqi_index.append
        else:
            temperature = filterdata(temperature_data, 3, 4)
            humidity = filterdata(humidity_data, 3, 4)
            gas_value= filterdata(gas_sensor, 3, 4)
            dust_value = filterdata(gas_sensor, 3, 4)
            aqi_value = filterdata(aqi_index, 3, 4)
            # timenow = datetime.now(pytz.timezone("Asia/Colombo")).strftime("%d/%m/%Y %H:%M:%S")
            timenow = datetime.datetime.now(pytz.timezone("Asia/Colombo"))
            doc_ref.set({
                u'Time': timenow,
                u'Temperature': temperature,
                u'Humidity': humidity,
                u'Gas Value': gas_value,
                u'PM2.5': dust_value,
                u'AQI': aqi_value
            })
            payload = {"timestamp": str(timenow), "temperature": temperature, "humidity": humidity, "gas_sensor": gas_value}
            jsonpayload = json.dumps(payload, indent=4)
            print("Published data: ", jsonpayload)
            temperature_data.clear()
            humidity_data.clear()
            gas_sensor.clear()
            time.sleep(5)
        # print(len(temperature_data))
    except Exception as ex:
        print(ex)


def filterdata(data, threshold, window_size):
    # importing dataset
    dataset = pd.Series(data)
    P = dataset.rolling(window=window_size).median().fillna(method='bfill').fillna(method='ffill')
    difference = np.abs(dataset - P)
    outlier_idx = difference > threshold
    filteredset = filterset(dataset, outlier_idx, P)
    return np.mean(filteredset)

def filterset(dataset, outlier_idx, rolling_ds):
    filteredset = [0 for i in range(0,len(dataset))]
    for i in range(0,len(dataset)):
        if outlier_idx[i]==True:
            filteredset[i] = rolling_ds[i]
        else:
            filteredset[i] = dataset[i]
    return filteredset

# Global variables
broker_url = "broker.hivemq.com"  # mqtt broker URI
broker_port = 1883  # broker port
message_count = 0  # count for setting data to firestore
temperature_data = []
humidity_data = []
aqi_index = []
dust = []
gas_sensor = []
db = firestore.Client()
doc_ref = db.collection(u'Pollutector - 04').document(u'Discrete Mode')


print("Welcome to pollutector firebase script for google cloud......")
client = mqtt.Client()  # defining client
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(broker_url, broker_port)  # connect using this port
client.subscribe("pollutector/outgoing/discrete", qos=1)
client.loop_forever()


