import requests
import Adafruit_DHT as dht
import time
import paho.mqtt.client as mqttClient

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")

        global Connected                #Use global variable
        Connected = True                #Signal connection 

    else:

        print("Connection failed")

Connected = False
broker_address= "192.168.2.21"
user = "<USER>"
password = "<PWD>"

port = 1883
sensor_name = "RPiB"

client = mqttClient.Client("Werkkamer")
client.username_pw_set(user, password=password)
client.on_connect= on_connect
client.connect(broker_address, port=port)
client.loop_start()
while Connected != True:    #Wait for connection
    time.sleep(0.1)

url = "<POST_URL>"

def measure():
  
  data = {}
  try:
    humidity, temperature = dht.read_retry(dht.DHT22, 4)
    humidity = round(humidity, 2)
    temperature = round(temperature, 2)

#    print 'Temperatuur: {0:0.1f}*C'.format(temperature)
#    print 'Luchtvochtigheid: {0:0.1f}%'.format(humidity)

    data["temperature"] = '{0:0.1f}'.format(temperature)
    data["humidity"] = '{0:0.1f}'.format(humidity)
  except:
    data["temperature"] = 21
    data["humidity"] = 21

    print('Failed to measure data')
  finally:
    return data

def upload_data(data):
  global sensor_name, url
  client.publish("home-assistant/ale/werkkamerTemp",data["temperature"])
  client.publish("home-assistant/ale/werkkamerHum",data["humidity"])

  post_data = {}
  post_data["Temperature"] = data["temperature"]
  post_data["Humidity"] = data["humidity"]
  post_data["SensorId"] = sensor_name
  headers = {}
  headers['Authorization'] = '<AUTH_TOKEN>'
  headers['Content-Type'] = 'application/json'

  try:
    response = requests.post(url, json=post_data, headers=headers, verify=False)
    
    print("Response code: " + str(response.status_code))
  except:
    print('Failed to upload da')

while True:
  upload_data(measure())
  time.sleep(10)
