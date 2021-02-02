import pytube

link = "https://www.youtube.com/watch?v=uRYcospQzzw"
yt = pytube.YouTube(link)

print('video description: ', yt.description)
print('rating', yt.rating)
print('length', yt.length)
print('views', yt.views)

stream = yt.streams.get_audio_only()
stream.download(filename="output")
