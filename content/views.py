import os
from uuid import uuid4

from django.conf.global_settings import MEDIA_ROOT
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed


# Create your views here.
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all()   #select * from content_feed;
        print(feed_list)

        for feed in feed_list:
            print(feed.content)
        return render(request, 'OFER/main.html', context=dict(feeds=feed_list))


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        return render(request, 'content/profile.html', context=dict(user=user))

class UploadProfile(APIView):
    def post(self, request):

        file = request.FILES['file']
        email = request.data.get('email')
        # 이미지 파일의 확장자 추출
        extension = file.name.split('.')[-1].lower()
        uuid_name = uuid4().hex + extension
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        profile_image = uuid_name

        user = User.objects.filter(email=email).first()
        user.profile_image = profile_image
        user.save()

        return Response(status=200)

class Upload(APIView):
    def get(self, request):

        return render(request, 'OFER/main.html')