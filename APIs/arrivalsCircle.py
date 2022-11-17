import requests
import json

url = "https://api.tfl.gov.uk/Line/circle/Arrivals"

payload={}
headers = {
  'Authorization': 'Basic CjBkM2NhOTkyY2YwMjRhMWI5MzNhZDM2ZTQyY2E0MmQ5OjdjYjQ3ODUzNzlkZTQxZTVhNjUzZTk4NDk5MGJiODYx'
}

response = requests.request("GET", url, headers=headers, data=payload)




data = json.loads(response.text)

print(json.dumps(data, indent=2))

