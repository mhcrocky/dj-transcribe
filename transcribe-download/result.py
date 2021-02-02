import requests
import json

endpoint = "https://api.assemblyai.com/v2/transcript/b788hwbst-4c1c-4f5a-9e2b-c39072475fca" # xb78gr3723-9705-4a54-aaf6-1557147d4253

headers = {
    "authorization": "cba052e3be71481183e9c2455cc6b7d3",
}

response = requests.get(endpoint, headers=headers)
response = response.json()

with open("result.json", "w") as outfile:
    json.dump(response, outfile)

print(response)
