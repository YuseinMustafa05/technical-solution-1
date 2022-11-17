import json 
import requests

import requests

url = "https://api.tfl.gov.uk/Line/victoria/Arrivals/940GZZLUWWL"

payload={}
headers = {
  'Authorization': 'Basic CjBkM2NhOTkyY2YwMjRhMWI5MzNhZDM2ZTQyY2E0MmQ5OjdjYjQ3ODUzNzlkZTQxZTVhNjUzZTk4NDk5MGJiODYx'
}

response = requests.request("GET", url, headers=headers, data=payload)



data = json.loads(response.text)

#How to extract what you want from the api call
#print(json.dumps(data[0]["naptanId"], indent=2))


print(json.dumps(data, indent=2))

