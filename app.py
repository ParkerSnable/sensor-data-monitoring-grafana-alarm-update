import time

import Adafruit_DHT as dht_sensor
import requests
from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
from requests import ReadTimeout
from config import alarm_url

alarm_temp = 32  # temp at which the alarm should be set
last_notification_time = 0
notification_interval = 5 * 60  # only notify every 5min
content_type = str('text/plain; version=0.0.4; charset=utf-8')


def get_temperature_readings():
    max_retries = 2
    for _ in range(max_retries):
        humidity, temperature = dht_sensor.read_retry(dht_sensor.DHT11, 4)
        if all(v is not None for v in [humidity, temperature]):
            humidity = format(humidity, ".2f")
            temperature = format(temperature, ".2f")
            return {"temperature": temperature, "humidity": humidity}
        time.sleep(0.2)
    return None


def set_smartphone_alarm():
    global last_notification_time
    current_time = time.time()
    if current_time - last_notification_time >= notification_interval:
        try:
            requests.get(alarm_url, timeout=2)
            last_notification_time = current_time
        except ReadTimeout as rt:
            # Todo:
            #  do something more meaningful here
            #  implement fallback notification method
            #  if VPN or Tasker is broken
            #  for example: send_telegram_message()
            print(rt)
            pass
        except Exception as e:
            # Todo: exclude blanket except
            print(e)
            pass


app = Flask(__name__)

current_humidity = Gauge(
    'current_humidity',
    'the current humidity percentage, this is a gauge as the value can increase or decrease',
    ['room']
)

current_temperature = Gauge(
    'current_temperature',
    'the current temperature in celsius, this is a gauge as the value can increase or decrease',
    ['room']
)


@app.route('/metrics')
def metrics():
    metric_data = get_temperature_readings()
    print(float(metric_data['temperature']))
    if float(metric_data['temperature']) > alarm_temp:
        set_smartphone_alarm()
    current_humidity.labels('grow').set(metric_data['humidity'])
    current_temperature.labels('grow').set(metric_data['temperature'])
    print(generate_latest())
    return Response(generate_latest(), mimetype=content_type)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
