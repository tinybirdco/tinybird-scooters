import json
import ndjson
import os
from uuid import uuid4
from datetime import datetime, timedelta
import random
import requests
from random import choices
import math
from time import sleep
from confluent_kafka import Producer

CONFLUENT_SERVER = 'your_bootstrap_server'
CONFLUENT_KEY = 'your_confluent_access_key'
CONFLUENT_SECRET = 'your_confluent_secret'
TOPIC_NAME = 'scooter_telemetry'

def generate_data(uuids, state):
    data_list = []
    for scooter_id in uuids:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_changed_time = state.get(scooter_id, {}).get(
            'status_changed_time', timestamp)
        journey_id = 'none'

        # Check if there is state for the scooter
        if scooter_id in state:
            scooter_state = state[scooter_id]
            status = scooter_state['status']
            latitude = scooter_state['latitude']
            longitude = scooter_state['longitude']
            battery_percent = scooter_state['battery_percent']
            journey_duration = scooter_state['journey_duration']
            last_battery_decrement_time = scooter_state['last_battery_decrement_time']
            journey_id = scooter_state['journey_id']

            # Update status if necessary
            if status == 'in_use':
                time_diff = datetime.now() - datetime.strptime(status_changed_time, "%Y-%m-%d %H:%M:%S")

                if time_diff.total_seconds() >= journey_duration:
                    status = 'available'
                    journey_id = 'none'
                    status_changed_time = timestamp
                else:
                    status = 'in_use'

                if battery_percent < 5:
                    status = 'available'
            elif status == 'available':
                if battery_percent < 25:  # bikes under 25% battery should never be used
                    status = 'available'
                else:
                    status = choices(['available', 'in_use', 'fault'], weights=[
                                     90, 9.5, 0.5], k=1)[0]
                status_changed_time = timestamp
                if status == 'in_use':  # if we have changed to in_use
                    journey_duration = random.randint(60, 300)
                    journey_id = str(uuid4())
            elif status == 'fault':
                time_diff = datetime.now() - datetime.strptime(status_changed_time, "%Y-%m-%d %H:%M:%S")
                if time_diff.total_seconds() >= 30:
                    status = 'available'
                    status_changed_time = timestamp

            if status == 'in_use':
                # Update latitude and longitude
                latitude += random.uniform(-0.00002, 0.00002)
                longitude += random.uniform(-0.00002, 0.00002)
                # Update battery percent
                time_diff = datetime.now() - datetime.strptime(last_battery_decrement_time,
                                                               "%Y-%m-%d %H:%M:%S")
                if time_diff.total_seconds() >= 25:
                    last_battery_decrement_time = timestamp
                    battery_percent -= 1

        else:
            # Generate random data
            status = choices(['in_use', 'available', 'fault'],
                             weights=[35, 60, 5], k=1)[0]
            journey_duration = 0
            if status == 'in_use':  # if we have changed to in_use, we need to set a journey duration
                journey_duration = random.randint(60, 300)
            latitude = random.uniform(36.08144597233949, 36.27704846619167)
            longitude = random.uniform(-115.31338500392567, -
                                       115.06091073530962)
            battery_percent = max(
                0, min(100, math.floor(random.normalvariate(60, 20))))
            last_battery_decrement_time = timestamp
            journey_id = str(uuid4()) if status == 'in_use' else 'none'

        data = {
            'scooter_id': scooter_id,
            'timestamp': timestamp,
            'status': status,
            'fault_severity': 'NONE' if status != 'fault' else random.choice(['INFO', 'WARNING', 'CRITICAL']),
            'latitude': latitude,
            'longitude': longitude,
            'battery_percent': battery_percent,
            'journey_id': journey_id
        }

        data_list.append(data)

        # Store new state
        state[scooter_id] = {
            'status': status,
            'status_changed_time': status_changed_time,
            'latitude': latitude,
            'longitude': longitude,
            'battery_percent': battery_percent,
            'journey_duration': journey_duration,
            'last_battery_decrement_time': last_battery_decrement_time,
            'journey_id': journey_id
        }

    return data_list


def send_to_kafka(producer, data):
    for row in data:
        producer.produce(TOPIC_NAME, value=json.dumps(row))
    producer.flush()


def create_kafka_producer():
    # Required connection configs for Kafka producer, consumer, and admin
    config = {
        'bootstrap.servers': CONFLUENT_SERVER,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': CONFLUENT_KEY,
        'sasl.password': CONFLUENT_SECRET
    }

    return Producer(config)


def send_to_tinybird(data):
    r = requests.post(f'{os.environ("TB_HOST")}/v0/events',
                      params={
                          'name': 'scooter_telem_events',
                          'token': os.environ('TB_TOKEN')
                      },
                      data=ndjson.dumps(data))

    print(r.status_code)
    print(r.text)


def generate():
    with open('./uuids.txt', 'r') as file:
        uuids = file.read().splitlines()
        state = {}  # Initialize state
        producer = create_kafka_producer()
        while True:
            print('generating')
            data = generate_data(uuids, state)
            sleep(3)
            send_to_kafka(producer, data)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(data)


# Example usage
generate()
