# gps-block
Easily add gps functionality to your project. 

## Overview

The [GPS NEO-6M](https://www.amazon.com/gp/product/B07P8YMVNT/ref=ppx_yo_dt_b_asin_title_o01_s01?ie=UTF8&psc=1) is a decent and very inexpensive GPS module. This project creates a container you can add to your project to retrieve data from the GPS module via HTTP or MQTT. (If you aren't using containers, you can still run or modify the gps.py example)

This gps-block is intended to be used via the USB (not serial) connection and has been tested on a Raspberry Pi 4.

## Installation

Use the docker-compose.yml file as an example of how to add this to your project.

## Usage

By default, the project will run an HTTP server on port 7575 and listen for external connections. You can poll the data using: (replace your device's IP address)

- `curl 192.168.1.100:7575`

- `http://192.168.1.100:7575`

- An HTTP library in your favorite programming languge (Node, Python, etc...) such as [Requests](https://docs.python-requests.org/en/latest/) for Python.


To use internally only among your other containers, change:

```
ports:
      - "7575:7575"
```

to:

```
expose:
      - "7575"
```

You could then refer to the HTTP server by container name from another container, such as `curl gps:7575`

To use MQTT instead, add a device variable `MQTT_ADDRESS` with the IP of your MQTT broker and it will publish to that instead of running an HTTP server.

When using MQTT, the default topic will be `gps` but you can change that using the `MQTT_TOPIC` device variable. By default, it will publish every five cycles of TPV data from the GPS module (approximately every five seconds.) This value can be changed by setting `SKIP_CYCLES` to an integer value.

## Data

The gps-block will return data in json format. Here is an example:

```
{
    "alt": 119.0859,
    "altHAE": 85.3359,
    "altMSL": 119.0859,
    "class": "TPV",
    "climb": 0.034,
    "device": "/dev/ttyACM0",
    "ecefpAcc": 9.49,
    "ecefvAcc": 0.55,
    "ecefvx": -0.02,
    "ecefvy": 0.04,
    "ecefvz": -0.02,
    "ecefx": 1242787.92,
    "ecefy": -4731867.26,
    "ecefz": 4078541.55,
    "epc": 17.95,
    "eph": 5.183,
    "eps": 7.03,
    "ept": 0.005,
    "epv": 8.974,
    "epx": 2.097,
    "epy": 3.517,
    "geoidSep": -33.75,
    "lat": 46.215901065,
    "leapseconds": 18,
    "lon": -77.744076823,
    "magtrack": 62.1747,
    "magvar": -12.0,
    "mode": 3,
    "sep": 9.045,
    "speed": 0.038,
    "status": 2,
    "time": "2022-02-09 05:07:58",
    "track": 74.1991,
    "velD": -0.034,
    "velE": 0.036,
    "velN": 0.01
}
```

### Thanks
Resources used to create this block:

- https://github.com/tfeldmann/gpsdclient

- https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842

