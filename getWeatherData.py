#!/usr/bin/python3

#Request Weather data from Tomorrow.io every 2 minutes (to fall below the 1000 requests per day allowed by the free account)
#(month,day,hr,minute)
#Requests windSpeed,windDirection,temperature,cloudCover,dewPoint,precipitationIntensity
#Each of these data published under: WeatherStation/

import time

from requests import api
import paho.mqtt.client as mqtt
import traceback
import requests
#credentials is a file with only the below values.  This is separate to protect your sensitive/unique information
from credentials import apikey,coordinates #apikey is a string for you unique key, coordinates=[lat,long]

i = 0
day = 0
energy = 0.0
powerMax = 0

broker_address="192.168.50.201"
#broker_address="iot.eclipse.org" #to use external broker
client = mqtt.Client("WeatherStation")
client.connect(broker_address)
client.loop_start() #handles reconnecting.  Runs in separate thread to let main thread run
#client.loop_forever() #Stops main thread for mqtt loop
#client.reinitialise()

weatherUrl = "https://api.tomorrow.io/v4/timelines"

#Get weather data as JSON from Tomorrow.io
def getWeatherData():
  querystring = {"apikey":apikey}
  location = {
  "type": "Point",
  "coordinates": coordinates
  }
  fields = ["windSpeed","windDirection","temperature","cloudCover","dewPoint","precipitationIntensity"]
  payload = {
    "units": "metric", #metric or imperial
    "timesteps": ["current"],
    "location":location,
    "fields":fields,
    "timezone":"America/New_York"
  }
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  try:
    response = requests.request(
    "POST", 
    weatherUrl, 
    json=payload, 
    headers=headers, 
    params=querystring
    )
    data = response.json()["data"]["timelines"][0]["intervals"][0]
    Toutside=data["values"]["temperature"]
    Houtside=data["values"]["humidity"]
    cloudCover = data["values"]["cloudCover"]
    dewPoint = data["values"]["dewPoint"]
    windSpeed = data["values"]["windSpeed"]
    windDirection = data["values"]["windDirection"]
    precipIntensity = data["values"]["precipitationIntensity"]
  except:
    print("Data Retrieval from Tomorrow.io failed.")
    Toutside=25
    Houtside=50
    cloudCover=0
    dewPoint=50
    windSpeed=0
    windDirection=0
    precipIntensity=0

  print("Wind Speed",data["values"]["windSpeed"],"")
  print("Wind Direction",data["values"]["windDirection"])
  print(f"Temperature {Toutside}C")
  print(f"Cloud Cover {cloudCover}%")
  return [Toutside,Houtside,cloudCover,dewPoint,windSpeed,windDirection,precipIntensity]

def msgWeatherData():
  [Toutside,Houtside,cloudCover,dewPoint,windSpeed,windDirection,precipIntensity] = getWeatherData()
  messageWeatherData = f",{Toutside},{Houtside},{cloudCover},{dewPoint},{windSpeed},{windDirection},{precipIntensity},"
  try:
      client.publish("WeatherStation/WeatherData",messageWeatherData)
      print(messageWeatherData)
  except:
      print("MQTT error: ", messageWeatherData)
        
def getCurrentTime():
  #timeNow = time.localtime()
  #year = time.localtime().tm_year
  #month = time.localtime().tm_mon
  day = time.localtime().tm_mday
  hour = time.localtime().tm_hour
  minute = time.localtime().tm_min
  second = time.localtime().tm_sec
  return day,hour,minute,second

def Average(l):
  avg = sum(l)/len(l)
  return avg

try:
  while True:
    day,hour,minute,second = getCurrentTime()
    
    if minute%2==0:
      msgWeatherData()
      time.sleep(70) #will pause until well into the next minute so that there are not more than 1 request for every even minute.

    time.sleep(1)
except:
  client.loop_stop()
  print("MQTT loop closed")
  traceback.print_exc()