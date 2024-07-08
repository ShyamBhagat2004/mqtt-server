import json
import paho.mqtt.client as mqtt
import math
from pymongo import MongoClient
from datetime import datetime

# MongoDB settings
MONGO_URI = "mongodb+srv://shyambhagat:mypassword@cluster0.ltngatr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MQTT settings
MQTT_BROKER = "broker.mqtt.cool"
MQTT_PORT = 1883
MQTT_TOPIC = "NMEA_Lightning"

client = MongoClient(MONGO_URI)
db = client['lightning_data_db']
collection = db['lightning_strikes']

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(mqtt_client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received MQTT message: {message}")
    if message.startswith("$WIMLI,"):
        data = parse_lightning_message(message)
        if data:
            print(f"Formatted data: {data}")
            # Insert data into MongoDB with timestamp
            document = {
                'latitude': data[0],
                'longitude': data[1],
                'timestamp': datetime.now()  # Record the current time and date
            }
            collection.insert_one(document)

def parse_lightning_message(message):
    parts = message.split(',')
    distance_miles = float(parts[1])
    bearing_degrees = float(parts[2].split('*')[0])
    return convert_to_coordinates(38.002729, 23.675644, distance_miles, bearing_degrees)

def convert_to_coordinates(lat, lon, distance, bearing):
    distance_km = distance * 1.60934
    bearing_rad = math.radians(bearing)
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance_km / 6371.0) + math.cos(lat_rad) * math.sin(distance_km / 6371.0) * math.cos(bearing_rad))
    new_lon_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance_km / 6371.0) * math.cos(lat_rad), math.cos(distance_km / 6371.0) - math.sin(lat_rad) * math.sin(new_lat_rad))
    return math.degrees(new_lat_rad), math.degrees(new_lon_rad)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
