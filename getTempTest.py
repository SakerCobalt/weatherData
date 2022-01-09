import requests #python -m pip install requests

url = "https://api.tomorrow.io/v4/timelines"

querystring = {"units":"metric","timesteps":"1h"}

headers = {"Accept": "application/json"}

{
  "type": "Point",
  "coordinates": [
    -81.423,
    40.271
  ]
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)