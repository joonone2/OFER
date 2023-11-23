import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import django.contrib.auth.hashers
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse
from OFER.settings import MEDIA_ROOT



# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        email = request.data.get('email', None)
        name = request.data.get('name', None)
        nickname = request.data.get('nickname', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")
        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다.1"))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=500, data=dict(message="회원정보가 잘못되었습니다.2"))






class Mypage(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        return render(request, 'user/mypage.html', context=dict(user=user))

class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name
        email = request.data.get('email')

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)


class DeleteProfile(APIView):
    def post(self, request):
        email = request.data.get('email')


        user = User.objects.filter(email=email).first()

       # user.profile_image = /media/default_profile.jpg
        user.save()

        return Response(status=200)


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")

class ChangeName(APIView):
    def post(self, request):

        # 일단 파일 불러와

        name = request.data.get('name')
        email = request.data.get('email')


        user = User.objects.filter(email=email).first()

        user.name = name
        user.save()

        return Response(status=200)

