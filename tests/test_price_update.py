import requests

url = 'http://localhost:5000/price_update'
payload = {'price': 27040}

r = requests.post(url, json=payload)
print(r.status_code)
print(r.text)
