from django.urls import path
from .views import Join, Login, UploadProfile, Mypage

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('profile/upload', UploadProfile.as_view()),
    path('mypage', Mypage.as_view())
]