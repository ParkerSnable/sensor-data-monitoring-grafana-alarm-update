# Grafana Temperature and Humidity Monitoring with Smartphone Alarm

## Introduction

This project is a modified version of the Grafana Lab Temperature and Humidity monitoring setup. 
It is orignally based on the DHT22 sensor. The purpose of this project is to monitor temperature and send an alarm
to my smartphone with components already at reach before implementing a full smart home later on.
It monitors metrics using a Raspberry Pi connected to a DHT11 sensor with a Flask Server, Prometheus and Grafana.
To implement alarm and notification the project uses tailscale VPN and Tasker.

### Resources

- Original Blog: [Monitor Temperature and Humidity with Grafana and Raspberry Pi](https://grafana.com/blog/2023/10/23/monitor-temperature-and-humidity-with-grafana-and-raspberry-pi/)
- Original Code: [Sensor Data Monitoring with Grafana](https://github.com/tonypowa/sensor-data-monitoring-grafana)

## Base Architecture

The core architecture involves a Raspberry Pi interfacing with a DHT11 Temperature sensor. 
This Pi runs a Flask server to communicate with Prometheus and display data on a Grafana dashboard accessible 
from every tailscale node. Modifications to the original repository include the addition of service and script files,
a switch to the DHT11 sensor, and the integration of alarm and notification features for smartphones. 

The decision to switch to the DHT11 sensor was to reduce cost by using already available components because of the 
project's temporary nature as it will be obsolete for me shortly after implementation. 
The DHT11 sensors precision is not as good as the precision of the original equipment used in the Grafana Lab tutorial,
but it is fine for my current needs.

## Installation

1. Begin by installing the dependencies as shown in the original blog and code readme.
2. Proceed to install Tailscale on your Raspberry Pi and Smartphone. Add them to the same network.
3. Install Tasker on your Smartphone.
4. Clone the repository into the home directory of your Raspberry Pi user.
5. Customize the paths in the service files to suit your specific use case, then move them into the systemd service directory.
6. Enable the services and reboot your Raspberry Pi.

7. **Current Step for Dashboard and Tasks:**
   - Develop an HTTP Request Profile for Tasker that triggers an alarm.
   - Write the alarm URL into config.py as "alarm_url".
   - Create a Dashboard in Grafana for visualizing the metrics.

#### Todo:
- Include Tasker XML files in the repository for easy importation by users.
- Add the Dashboard to the repository so users can easily import it for their own use.
- Update step 7.

## Notification and Alarm Functionality

I had no static IP address provisioned by my ISP so the creation of a Tailscale VPN enabled communication between my
devices regardless of location without any extra cost. Through this VPN the web servers running on Pi, Smartphone and 
any of my other devices can communicate without the need for additional vServer or similar solutions.

### Implementation Steps

1. **Install Tailscale to Host Device**: Tailscale must be installed and configured on both the Raspberry Pi and the \
smartphone. Refer to this guide [here](https://pimylifeup.com/raspberry-pi-tailscale/) and install the APK on the \
smartphone.

2. **Configure Tasker on Smartphone**: The Tasker App is used on the smartphone to automate alarm and notification \
actions triggered by the script running on the Raspberry Pi. XML tasks need to be imported into Tasker to replicate \
my exact solution.