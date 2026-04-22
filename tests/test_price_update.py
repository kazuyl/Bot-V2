import requests

url = "https://bot-v2-production.up.railway.app/price_update"

payload = {
    "price": 27040
}

r = requests.post(url, json=payload)

print(r.status_code)
print(r.text)
