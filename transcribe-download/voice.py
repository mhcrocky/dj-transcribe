import sys
import time
import requests
import json
import pytube


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
        self.key = key

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
        response = response.json()

        # with open("result.json", "w") as outfile:
        #     json.dump(response, outfile)

        return response


if __name__ == "__main__":
    # download test
    # link = "https://www.youtube.com/watch?v=uRYcospQzzw"
    # download(link)

    # assembly-ai tests
    key = "977c87bf52e14cdd911f3bdc2cb1bc84"
    ai = AssemblyAi(key)

    # upload
    # file_name = "output.mp4"
    # audio_url = ai.upload(file_name)

    # trigger transcription
    audio_url = "https://s3-us-west-2.amazonaws.com/blog.assemblyai.com/audio/8-7-2018-post/7510.mp3"
    tag = ai.transcribe(audio_url)

    # poll transcription results
    # tag = "b788hwbst-4c1c-4f5a-9e2b-c39072475fca"
    response = ai.poll('lssb2qa1g-c299-4aa2-a147-9e130d5bf2ce')

    print(response)
    print(response["status"])
