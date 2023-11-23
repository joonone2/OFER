import os
from uuid import uuid4

from django.views import View

from OFER.settings import MEDIA_ROOT
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed


# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None) #현재 접속중인 사용자의 이메일 받아오기

        #로그인 안되어있을시 login 화면으로 보내는 코드
        if email is None:
            return render(request,"user/login.html")
        user = User.objects.filter(email=email).first() #DB에 있는 이메일과 비교
        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.all()   #select * from content_feed;
        print(feed_list)

        for feed in feed_list:
            print(feed.content)
        return render(request, 'OFER/main.html', context=dict(feeds=feed_list,
                                                                profile_image=user.profile_image,
                                                                nickname=user.nickname))



class UploadFeed(APIView):

    def get(self, request):

        return render(request, 'user/upload.html')
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        print(save_path)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        asdf = uuid_name
        content123 = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image=asdf, content=content123, email=email)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email)

        return render(request, 'content/profile.html', context=dict(feed_list=feed_list, user=user))

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

        return render(request, 'user/upload.html')


class StyleView(APIView):
    def get(self, request):
        email = request.GET.get('email', None)  # 현재 접속중인 사용자의 이메일 받아오기
        id = request.GET.get('id', None) # 사용자가 누른 feed의 고유번호 받아오기
        print('아이디')
        print(id)
        print('이메일')
        print(email)
        # 추가적으로 선택된 피드 번호도 받아야한다. (밑의 코드와 같은 방식으로 하면 될듯)

        user = User.objects.filter(email=email).first()  # DB에 있는 이메일과 비교
        if user is None:
            return render(request, "user/login.html")

        feed = Feed.objects.filter(id=id).first()

        # 해당 피드가 없으면 메인페이지로 돌아가기
        return render(request, 'content/style_view.html', context=dict(
                                                              user=user, feed=feed))

