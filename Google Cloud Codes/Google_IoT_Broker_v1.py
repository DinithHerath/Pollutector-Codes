import argparse
import datetime
import os
import time
import json
import numpy as np
import pandas as pd
import jwt
import paho.mqtt.client as mqtt

# Global variables
broker_url = "broker.hivemq.com"  # mqtt broker URI
broker_port = 1883  # broker port
sub_topic = ''
mqtt_topic = ''  # publishing google cloud mqtt topic
message_count = 0  # count for setting data to firestore
temperature_data = []
humidity_data = []
# aqi_index = []
gas_sensor = []


def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # The time the token expires.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', error_str(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(client, userdata, message):
    print("Message Recieved from pollutector: "+str(message.payload.decode()))
    publish_google(args, message.payload.decode(), clientgoogle, message_count)


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
        'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
        '--project_id',
        default=os.environ.get('GOOGLE_CLOUD_PROJECT'),
        help='GCP cloud project name')
    parser.add_argument(
        '--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument(
        '--device_id', required=True, help='Cloud IoT Core device id')
    parser.add_argument(
        '--private_key_file',
        required=True, help='Path to private key file.')
    parser.add_argument(
        '--algorithm',
        choices=('RS256', 'ES256'),
        required=True,
        help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
        '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
        '--ca_certs',
        default='roots.pem',
        help=('CA root from https://pki.google.com/roots.pem'))
    parser.add_argument(
        '--num_messages',
        type=int,
        default=100,
        help='Number of messages to publish.')
    parser.add_argument(
        '--message_type',
        choices=('event', 'state'),
        default='event',
        required=True,
        help=('Indicates whether the message to be published is a '
              'telemetry event or a device state message.'))
    parser.add_argument(
        '--mqtt_bridge_hostname',
        default='mqtt.googleapis.com',
        help='MQTT bridge hostname.')
    parser.add_argument(
        '--mqtt_bridge_port',
        default=8883,
        type=int,
        help='MQTT bridge port.')

    return parser.parse_args()


def config_google(args):
    client = mqtt.Client(
        client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                   .format(
                       args.project_id,
                       args.cloud_region,
                       args.registry_id,
                       args.device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username='unused',
        password=create_jwt(
            args.project_id, args.private_key_file, args.algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=args.ca_certs)
    return client


def publish_google(args, data, client, message_count):
    client.loop_start()
    # Publish to the events or state topic based on the flag.
    sub_topic = 'events' if args.message_type == 'event' else 'state'
    mqtt_topic = '/devices/{}/{}'.format(args.device_id, sub_topic)
    if (message_count <= 20):
        decode = json.load(data)
        temperature_data.append(float(decode['Temperature']))
        humidity_data.append(float(decode['Humidity']))
        gas_sensor.append(float(decode['GasSensorValue']))
        message_count += 1
    else:
        temperature = filterdata(temperature_data, 3, 4)
        humidity = filterdata(humidity_data, 3, 4)
        gas_value= filterdata(gas_sensor, 3, 4)
        print("Published data: " + str(temperature) + " " + str(humidity) + " " + str(gas_value))
        message_count = 0
        temperature_data.clear()
        humidity_data.clear()
        gas_sensor.clear()
        time.sleep(5)
    print("Publishing message: {}".format(data))
#     jsonpayload = json.dumps(data, indent=4)
    client.publish(mqtt_topic, data, qos=1)
#     time.sleep(1 if args.message_type == 'event' else 5)
    print("Published message successfully.")
    client.loop_stop()


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

if __name__ == '__main__':
    print("Welcome to pollutector broker script for google cloud......")
    args = parse_command_line_args()
    clientgoogle = config_google(args)
    clientgoogle.on_connect = on_connect
    clientgoogle.on_publish = on_publish
    clientgoogle.on_disconnect = on_disconnect
    clientgoogle.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)
    print("Connected with google cloud successfully.")
    clientmqtt = mqtt.Client()
    clientmqtt.on_connect = on_connect
    clientmqtt.on_disconnect = on_disconnect
    clientmqtt.on_message = on_message
    clientmqtt.connect(broker_url, broker_port)
    clientmqtt.subscribe("pollutector/outgoing", qos=1)
    clientmqtt.loop_forever()
