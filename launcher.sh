#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# To start at boot add cronjob:
# @reboot sh /home/pi/sensor/launcher.sh >/home/pi/logs/cronlog 2>&1

cd /
cd /home/pi/sensor
python3 post_data.py
cd /
