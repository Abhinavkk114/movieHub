from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.models import Movies,Genres,Reviews

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class Genreserializer(serializers.ModelSerializer):
    class Meta:
        model=Genres
        fields=["id","genre"]    


class Reviewserilizer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        exclude=("movie",)
    

class Movieserializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    genres=serializers.SlugRelatedField(many=True,read_only=True,slug_field="genre")


    review=Reviewserilizer(many=True,read_only=True)


    # genre_names=Genreserializer(read_only=True,many=True)
    class Meta:
        model=Movies
        # exclude=("genres",)
        fields="__all__"