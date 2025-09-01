from .import views
from django.urls import path,include
from django.urls import path
from .views import SignupView, SigninView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

path('',views.index,name='home'),
path("signup/", SignupView.as_view(), name="signup"),
path("signin/", SigninView.as_view(), name="signin"),
path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]