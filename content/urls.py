from django.urls import path
from .views import Profile, Main, Upload, UploadFeed, StyleView, UploadReply, ToggleLike, ToggleBookmark


urlpatterns = [
    path('profile', Profile.as_view()),
    path('main', Main.as_view()),
    path('upload', UploadFeed.as_view()),
    path('reply', UploadReply.as_view()),
    path('like', ToggleLike.as_view()),
    path('bookmark', ToggleBookmark.as_view()),
    path('styleview', StyleView.as_view())
]