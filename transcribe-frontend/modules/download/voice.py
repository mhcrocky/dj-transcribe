import sys
import time
import requests
import json
import pytube
import boto3
from django.conf import settings

AWS_ACCESS_KEY_ID = 'AKIASOJFJ5RPYZJMYOOY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'transcribe-now'

def download(link):
    """download youtube video for further processing
    """
    yt = pytube.YouTube(link)

    # print('video description: ', yt.description)
    # print('rating', yt.rating)
    # print('length', yt.length)
    # print('views', yt.views)

    stream = yt.streams.get_audio_only()
    stream.download(filename="output")


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


class AssemblyAi(object):

    def __init__(self, key):
        if key:
            self.key = key
        else:
            self.key = '1fc3ded0edaa4851b288051bff6e56d5'


    def upload(self, file_name):
        """upload file to assembly-ai servers
        """
        headers = {'authorization': self.key}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                headers=headers,
                                data=read_file(file_name))
        
        # https://cdn.assemblyai.com/upload/0e30a085-30eb-4b77-9911-133b538a35e6
        return response.json()["upload_url"]

    def transcribe(self, audio_url):
        """trigger transcription
        """
        endpoint = "https://api.assemblyai.com/v2/transcript"

        json = {
            "audio_url": audio_url,
            "speaker_labels": True
        }

        headers = {
            "authorization": self.key,
            "content-type": "application/json"
        }

        response = requests.post(endpoint, json=json, headers=headers)
        return response.json()["id"]


    def poll(self, tag):
        """get results from queue
        """
        endpoint = f"https://api.assemblyai.com/v2/transcript/{tag}" # xb78gr3723-9705-4a54-aaf6-1557147d4253
        headers = {
            "authorization": self.key,
        }
        response = requests.get(endpoint, headers=headers)
        print(response.json())

        try:
            response = response.text

            s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
            bucket.put_object(Key=f'uploads/json/{tag}.json', Body=response)
            print('okay')
            return 'okay'
            
        except:
            print('error')
            return 'error'
            


if __name__ == "__main__":
    # download test
    link = "https://www.youtube.com/watch?v=uRYcospQzzw"
    download(link)

    # assembly-ai tests
    key = "1fc3ded0edaa4851b288051bff6e56d5"
    ai = AssemblyAi(key)

    # upload
    file_name = "output.mp4"
    audio_url = ai.upload(file_name)

    # trigger transcription
    # audio_url = "https://cdn.assemblyai.com/upload/c4fb70f1-4c12-4f35-8a11-01f35d9a11e9"
    tag = ai.transcribe(audio_url)

    # poll transcription results
    # tag = "b788hwbst-4c1c-4f5a-9e2b-c39072475fca"
    response = ai.poll(tag)

    print(response)
    print(response["status"])
