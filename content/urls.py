from django.urls import path
from .views import Profile, Main, Upload, UploadFeed


urlpatterns = [
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    path('upload', UploadFeed.as_view())
]