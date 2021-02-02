import sys
import time
import requests

filename = "output.mp4"
 
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
 
headers = {'authorization': "cba052e3be71481183e9c2455cc6b7d3"}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

print(response.json())

# https://cdn.assemblyai.com/upload/0e30a085-30eb-4b77-9911-133b538a35e6