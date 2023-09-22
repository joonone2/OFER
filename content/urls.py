from django.urls import path
from .views import Profile, Main

urlpatterns = [
    path('profile', Profile.as_view()),
    path('main', Main.as_view())
]