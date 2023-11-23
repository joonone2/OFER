from django.urls import path
from .views import Join, Login, UploadProfile, Mypage, LogOut, DeleteProfile, ChangeName

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
    path('profile/upload', UploadProfile.as_view()),
    path('mypage', Mypage.as_view()),
    path('logout', LogOut.as_view()),
    path('profile/delete', DeleteProfile.as_view()),
    path('profile/changename', ChangeName.as_view())
]