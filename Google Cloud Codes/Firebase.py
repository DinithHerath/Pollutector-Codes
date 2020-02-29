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

#set GOOGLE_APPLICATION_CREDENTIALS="C:\Users\dinit\Downloads\pollutector-pub-5222d506a61d.json"

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()
doc_ref = db.collection(u'Pollutector Data').document()
doc_ref.set({
    u'Time': datetime.datetime.now(),
    u'Temperature': 28.1,
    u'Humidity': 78.59,
    u'Gas Value': 135.4
}) 