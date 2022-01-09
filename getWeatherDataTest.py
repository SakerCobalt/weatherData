import requests
from credentials import coordinates,apikey #apikey is a string for you unique key, coordinates=[lat,long]

weatherUrl = "https://api.tomorrow.io/v4/timelines"

querystring = {"apikey":apikey}
location = {
  "type": "Point",
  "coordinates": coordinates
  }
fields = ["windSpeed","windDirection","temperature","cloudCover","humidity","dewPoint","precipitationIntensity"]
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

response = requests.request(
  "POST", 
  weatherUrl, 
  json=payload, 
  headers=headers, 
  params=querystring
)

data = response.json()["data"]["timelines"][0]["intervals"][0]
print(data)
print("Time",data["startTime"])
print("Wind Speed",data["values"]["windSpeed"],"")
print("Wind Direction",data["values"]["windDirection"])
temp = data["values"]["temperature"]
print(f"Temperature {temp}C")
cloudCover = data["values"]["cloudCover"]
print(f"Cloud Cover {cloudCover}%")
humidity = data["values"]["humidity"]
print(f"Humidity {humidity}%")
dewPoint = data["values"]["dewPoint"]
print(f"Dewpoint {dewPoint}C")
precipitation = data["values"]["precipitationIntensity"]
print(f"{precipitation} mm/hr of precipitation")