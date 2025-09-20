from .import views
from django.urls import path,include
from django.urls import path
from .views import SignupView, SigninView,SongListViewSet,SongViewSet,FavouritelistViewSet,TagViewSet,CategoryViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'songlist', SongListViewSet, basename='songlist')
router.register(r'songlist/<int:id>', SongViewSet, basename='songview')
router.register(r'favouritelist/(?P<username>[^/.]+)', FavouritelistViewSet, basename='favouritelist')
router.register(r'taglist', TagViewSet, basename='taglist')
router.register(r'categorylist', CategoryViewSet, basename='categorylist')


urlpatterns = [

path('',views.index,name='home'),
path("signup/", SignupView.as_view(), name="signup"),
path("signin/", SigninView.as_view(), name="signin"),
path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
path("", include(router.urls)),

]