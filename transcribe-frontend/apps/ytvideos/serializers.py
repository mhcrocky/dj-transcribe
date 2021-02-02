# backend/server/apps/ytvideos/serializers.py

from rest_framework import serializers
from pytube import YouTube

from apps.ytvideos.models import Ytvideo

class YtvideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ytvideo
        read_only_fields = (
            "id",
            "created_at",
        )
        fields = (
            "id",
            "created_at",
            "url",
            "title",
            "length",
            "price",
        )
    def create(self, validated_data):
        # Need to validate url
        yt = YouTube(validated_data['url'])
        length = int(yt.length)
        title = yt.title # publish_date, rating, title, description, keywords, author
        return Ytvideo.objects.create(
            url=validated_data['url'],
            title=title,
            length=length,
        )
