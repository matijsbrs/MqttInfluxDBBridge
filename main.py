#!/usr/bin/env python3
#
# auther: Matijs Behrens
# Date: 12-10-2021
#
# This script pushes values from mqtt to a given influxdb
# It's a quick and dirty solution to a problem I ran in to, and perhaps usefull for others out there ;-) 
#   
# the topic format is as follows:
# [location]/[(sub)devicename]/[identifier]/[valuename] 
# The payload will be pushed if numerical.
#
# The name of the measurement in the influxdb will be [identifier].[valuename] value will always be parsed as float
# The devicename will be used as hostname.
# 
# The Server locations, credentials and topic are configured through Environment variables 
# this makes it very simpel to implament multiple bridges on a single computer. Or when 
# one is working with Docker.
#
# Feel free to use the code.


import os
import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
#from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL =  os.environ.get("INFLUX_URL")
INFLUX_TOKEN =  os.environ.get("INFLUX_TOKEN")
INFLUX_BUCKET =  os.environ.get("INFLUX_BUCKET")
INFLUX_ORG =  os.environ.get("INFLUX_ORG")

influxdb_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN)
influxdb_write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
#end of influx

MQTT_ADDRESS = os.environ.get("MQTT_ADDRESS")
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC").split(",")
# automation/climatronic/relais/vac24

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    for topic in MQTT_TOPIC:
        client.subscribe(topic)



def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    _parse_mqtt_message(msg.topic.split("/"), msg.payload.decode('utf-8'))

def _parse_mqtt_message(topic, payload):
    location = topic[1]
    if ( location != 'set' ):
        try:
            measurement = "{}.{}".format(topic[2],topic[3])
            data = "mem,host={} {}={}".format(location, measurement,float(payload))
            print ("data: {}".format(data))
            influxdb_write_api.write(INFLUX_BUCKET, INFLUX_ORG, data)
        except:
            print("ignore non numeric value.")
    else:
        print("set command ignore.")


def main():
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    print("Hello, I am {}".format(MQTT_CLIENT_ID))
    if ( len(MQTT_USERNAME) > 0 ):
        mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
