import requests

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": "https://cdn.assemblyai.com/upload/c4fb70f1-4c12-4f35-8a11-01f35d9a11e9",
  "speaker_labels": True
}

headers = {
    "authorization": "cba052e3be71481183e9c2455cc6b7d3",
    "content-type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

print(response.json())
