from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from rest_framework import serializers  

# Create your views here.

def index(request):
    return render(request,'index.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, SigninSerializer,SongListSerializer,FavouritelistSerializer

# Signup API
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Signin API
class SigninView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SongListViewSet(viewsets.ModelViewSet):
    queryset = SongList.objects.all()
    serializer_class = SongListSerializer



class SongViewSet(viewsets.ModelViewSet):
    queryset = SongList.objects.all()
    serializer_class = SongListSerializer

    def get_queryset(self):
        queryset = SongList.objects.all()
        song_id = self.request.query_params.get("id")
        if song_id:
            queryset = queryset.filter(id=song_id)
        return queryset    

# class FavouritelistViewSet(viewsets.ModelViewSet):
#     queryset = Favouritelist.objects.all()
#     serializer_class = FavouritelistSerializer

#     def get_queryset(self):
#         queryset = Favouritelist.objects.all()
#         username= self.request.query_params.get("username")
#         if song_id:
#             queryset = queryset.filter(username=username)
#         return queryset    


# class FavouritelistViewSet(viewsets.ModelViewSet):
#     serializer_class = FavouritelistSerializer
#     queryset = Favouritelist.objects.all()

#     def get_queryset(self):
#         username = self.kwargs.get("username")   # comes from URL path
#         if username:
#             return Favouritelist.objects.filter(username=username)
#         return super().get_queryset()

#     def perform_create(self, serializer):
#         """When a user adds a favourite, save username + song"""
#         username = self.request.data.get("username")
#         song_id = self.request.data.get("song")

#         if not username or not song_id:
#             raise serializers.ValidationError("Username and song are required")

#         serializer.save(username=username, song_id=song_id)


class FavouritelistViewSet(viewsets.ModelViewSet):
    serializer_class = FavouritelistSerializer
    queryset = Favouritelist.objects.all()

    def get_queryset(self):
        username = self.kwargs.get("username")   # from URL
        if username:
            return Favouritelist.objects.filter(username=username)
        return super().get_queryset()

    def perform_create(self, serializer):
        username = self.kwargs.get("username")   # username comes from URL
        article_title = self.request.data.get("article_title")  # song_name comes from POST body

        if not article_title:
            raise serializers.ValidationError("Song name is required")

        serializer.save(username=username, article_title=article_title)