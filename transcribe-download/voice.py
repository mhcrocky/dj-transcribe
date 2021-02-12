import sys
import time
import requests
import json

import pytube


def download(link):
    """download youtube video for further processing
    """
    yt = pytube.YouTube(link)

    print('video description: ', yt.description)
    print('rating', yt.rating)
    print('length', yt.length)
    print('views', yt.views)

    stream = yt.streams.get_audio_only()
    stream.download(filename="output")



def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
 
# TODO: clean-up to class hierarchy
def upload(key, file_name):
    """upload file to assembly-ai servers
    """
    headers = {'authorization': key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    print(response.json())
    # https://cdn.assemblyai.com/upload/0e30a085-30eb-4b77-9911-133b538a35e6


def transcribe(key, audio_url)
    """trigger transcription
    """
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
        "audio_url": audio_url,
        "speaker_labels": True
    }

    headers = {
        "authorization": "cba052e3be71481183e9c2455cc6b7d3",
        "content-type": "application/json"
    }

    response = requests.post(endpoint, json=json, headers=headers)
    print(response.json())


def result(key, tag):
    """get results from queue
    """
    endpoint = f"https://api.assemblyai.com/v2/transcript/{}" # xb78gr3723-9705-4a54-aaf6-1557147d4253

    headers = {
        "authorization": "cba052e3be71481183e9c2455cc6b7d3",
    }

    response = requests.get(endpoint, headers=headers)
    response = response.json()

    with open("result.json", "w") as outfile:
        json.dump(response, outfile)
    print(response)



if __name__ == "__main__":
    # download test
    link = "https://www.youtube.com/watch?v=uRYcospQzzw"
    download(link)

    # assembly-ai tests
    key = "cba052e3be71481183e9c2455cc6b7d3"
    file_name = "output.mp4"
    upload(key, file_name)

    audio_url = "https://cdn.assemblyai.com/upload/c4fb70f1-4c12-4f35-8a11-01f35d9a11e9"
    transcribe(key, audio_url)

    tag = "b788hwbst-4c1c-4f5a-9e2b-c39072475fca"
    result(key, tag)