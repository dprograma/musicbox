from rest_framework.serializers import ModelSerializer
from .models import Album, Song


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class SongSerializer(ModelSerializer):

    tracks = AlbumSerializer(many=True)
    class Meta:
        model= Song
        fields = ('id','artist','title','image','mp3','oga','created_at','tracks')

