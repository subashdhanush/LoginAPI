from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from rest_framework import serializers  

# Create your views here.

def index(request):
    return render(request,'index.html')

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import FavouriteSongsNewSerializer,CategorySerializer,TagSerializer,SignupSerializer, SigninSerializer,SongListSerializer,FavouritelistSerializer

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
        
         
class FavouriteSongViewSet(viewsets.ViewSet):
    """
    ViewSet for managing favourite songs and playlists.
    """

    def list(self, request):
        """GET /api/favourites/ — List all favourites of current user"""
        user = request.user.username
        favourites = Favouritesongsnew.objects.filter(user=user).order_by("playlistname")
        serializer = FavouriteSongsNewSerializer(favourites, many=True)
        return Response(serializer.data)

    def create(self, request):
        """POST /api/favourites/ — Add a song to playlist"""
        user = request.user.username
        song_id = request.data.get("song_id")
        new_list_name = request.data.get("new_list_name", "").strip()
        new_list_name2 = request.data.get("new_list_name2", "").strip()

        playlist_name = new_list_name2 or new_list_name
        if not playlist_name:
            return Response({"status": "error", "message": "Playlist name is required"}, status=status.HTTP_400_BAD_REQUEST)

        song_obj = get_object_or_404(SongList, id=song_id)

        # Limit to 10 songs per playlist
        song_count = Favouritesongsnew.objects.filter(user=user, playlistname=playlist_name).count()
        if song_count >= 10:
            return Response({"status": "warning", "message": f"You can only add up to 10 songs in '{playlist_name}' playlist."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicates
        if Favouritesongsnew.objects.filter(user=user, playlistname=playlist_name, fav_id=song_id).exists():
            return Response({"status": "warning", "message": f"'{song_obj.article_title}' already exists in '{playlist_name}' playlist."},
                            status=status.HTTP_200_OK)

        # Create record
        Favouritesongsnew.objects.create(
            user=user,
            song=song_obj.article_title,
            playlistname=playlist_name,
            fav_id=song_id
        )

        return Response({"status": "success", "message": f"Song '{song_obj.article_title}' added to playlist '{playlist_name}' successfully!"},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def by_playlist(self, request):
        """GET /api/favourites/by_playlist/?name=MyPlaylist"""
        user = request.user.username
        playlist_name = request.query_params.get("name")

        if not playlist_name:
            return Response({"status": "error", "message": "Playlist name required"}, status=status.HTTP_400_BAD_REQUEST)

        favourites = Favouritesongsnew.objects.filter(user=user, playlistname=playlist_name)
        serializer = FavouriteSongsNewSerializer(favourites, many=True)
        return Response(serializer.data)
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

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    