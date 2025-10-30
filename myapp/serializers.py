from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


# Signin Serializer
class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data

class SongListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongList
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class FavouritelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favouritelist
        fields = '__all__'

class FavouriteSongsNewSerializer(serializers.ModelSerializer):
    song_detail = SongListSerializer(source='fav_id', read_only=True)

    class Meta:
        model = Favouritesongsnew
        fields = ['id', 'user', 'playlistname', 'fav_id', 'song', 'song_detail']
        read_only_fields = ['user', 'song']        