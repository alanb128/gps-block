from gps import *
import time
import json
import paho.mqtt.client as mqtt
import os
import threading
import socket

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

use_httpserver = 0

try:
    mqtt_interval = int(os.getenv('MQTT_INTERVAL', '5'))
except:
    mqtt_interval = 5
mqtt_address = os.getenv('MQTT_ADDRESS', '0')
if mqtt_address == '0':
    use_httpserver = 1
mqtt_topic = os.getenv('MQTT_TOPIC', 'gps')

def getPositionData(gps):
    gps_data = {"mode": 0}
    nx = gpsd.next()
    i = 0
    while nx['class'] != 'TPV':
        i = i + 1
        print("Got class {}; waiting for class TPV. Retries: {}".format(nx['class'], i))
        if i > 4:
            break
        nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    # nx is a pita "dictwrapper"
    for d in nx:
        gps_value = getattr(nx, d, "Unknown")
        gps_data[d] = gps_value

    return json.dumps(gps_data) #, indent=4, sort_keys=True, default=str)

# Simple webserver
# see https://gist.github.com/joaoventura/824cbb501b8585f7c61bd54fec42f08f
def background_web(server_socket):

    global gps_data

    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        print("HTTP request from {}".format(client_address))
        

        # Send HTTP response
        response = 'HTTP/1.0 200 OK\n\n'+ getPositionData(gps)
        client_connection.sendall(response.encode())
        client_connection.close()


if use_httpserver == 1:
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 7575

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print("HTTP server listening on port {0}...".format(SERVER_PORT))

    t = threading.Thread(target=background_web, args=(server_socket,))
    t.start()
else:
    mqtt_client = mqtt.Client()
    print("Starting mqtt client, publishing to {0}:1883".format(mqtt_address))
    try:
        mqtt_client.connect(mqtt_address, 1883, 60)
    except Exception as e:
        print("Error connecting to mqtt. ({0})".format(str(e)))
    else:
        mqtt_client.loop_start()

while True:
    if use_httpserver == 0:
        print("Publishing MQTT data on topic {}.".format(mqtt_topic))
        mqtt_client.publish(mqtt_topic, getPositionData(gps))
    time.sleep(mqtt_interval)
