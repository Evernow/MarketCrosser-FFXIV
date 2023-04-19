import requests
import json

url = "https://www.garlandtools.org/api/get.php"
params = {"id":"35812", "type":"item", "lang":"en","version":"3"}

response = requests.get(url, params=params)

data = response.text

print(data)