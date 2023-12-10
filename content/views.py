import os
from django.http import JsonResponse
from uuid import uuid4

from django.views import View

from OFER.settings import MEDIA_ROOT
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from .models import Feed, Reply, Like, Bookmark


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

        user_connect = User.objects.filter(email=email).first()

        feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))
        pop_feed_list = sorted(feed_list, key=lambda x: x['like_count'], reverse=True)

        return render(request, "OFER/main.html", context=dict(feeds=feed_list, user=user,
                                                              user_connect=user_connect, pop_feeds = pop_feed_list))


class CategoryView(APIView):
    def get(self, request):
        email = request.session.get('email', None) #현재 접속중인 사용자의 이메일 받아오기
        category = request.GET.get('category')

        #로그인 안되어있을시 login 화면으로 보내는 코드
        if email is None:
            return render(request,"user/login.html")
        user = User.objects.filter(email=email).first() #DB에 있는 이메일과 비교
        if user is None:
            return render(request, "user/login.html")

        user_connect = User.objects.filter(email=email).first()

        feed_object_list = Feed.objects.all().order_by('-id')  # select  * from content_feed;
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked,
                                  category=feed.category
                                  ))
        pop_feed_list = sorted(feed_list, key=lambda x: x['like_count'], reverse=True)

        return render(request, "content/category_view.html", context=dict(feeds=feed_list, user=user,
                                                              user_connect=user_connect, pop_feeds = pop_feed_list, category=category))


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
        category = request.data.get('category')
        print("카테고리")
        print(category)

        Feed.objects.create(image=asdf, content=content123, email=email, category=category)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email).order_by('-id')
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)

        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                            like_feed_list=like_feed_list,
                                                                        bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))



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

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None) #댓글 쓴 사람의 이메일

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        #print('무야호')
        #print(feed_id)
        bookmark_text = request.data.get('bookmark_text', True)
        #print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None) #접속해있는 사람 email


        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)

class DeleteFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        delete_text = request.data.get('delete_text', None)
        #print('무야호')
        #print(feed_id)
        de = request.data.get('bookmark_text', True)
        #print(bookmark_text)
        # if delete_text == 'bookmark_border':
        #     is_marked = True
        # else:
        #     is_marked = False
        email = request.session.get('email', None) #접속해있는 사람 email


       # bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        try:
            feed = Feed.objects.get(id=feed_id)
            feed.delete()
            return JsonResponse({'message': '피드가 삭제되었습니다.'}, status=200)
        except Feed.DoesNotExist:
            return JsonResponse({'message': '해당 피드를 찾을 수 없습니다.'}, status=404)




class DeleteReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)

        delete_id = request.data.get('delete_id', None)
        print("삭제피드")
        print(feed_id)
        print("삭제댓글")
        print(delete_id)

        email = request.session.get('email', None) #접속해있는 사람 email


       # bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        try:

            reply = Reply.objects.get(id=delete_id)
            reply.delete()
            return JsonResponse({'message': '피드가 삭제되었습니다.'}, status=200)
        except Feed.DoesNotExist:
            return JsonResponse({'message': '해당 피드를 찾을 수 없습니다.'}, status=404)



class StyleView(APIView):
    def get(self, request):

        email = request.session.get('email', None) # 현재 접속중인 사용자의 이메일 받아오기
        id = request.GET.get('id', None) # 사용자가 누른 feed의 고유번호 받아오기
        print('아이디')
        print(id)
        print('이메일')
        print(email)
        # 추가적으로 선택된 피드 번호도 받아야한다. (밑의 코드와 같은 방식으로 하면 될듯)



        feed_object = Feed.objects.filter(id=id).first() # 해당하는 피드 찾고
        email_feed = feed_object.email #글쓴이의 이메일
        print('ggg')
        print(email_feed)
        user_content = User.objects.filter(email=feed_object.email).first()  # 게시물 쓴 유저의 정보
        reply_object_list = Reply.objects.filter(feed_id=feed_object.id)
        reply_list = []

        for reply in reply_object_list:
            user = User.objects.filter(email=reply.email).first()
            print(reply.email)
            print(user)
            reply_list.append(dict(reply_content=reply.reply_content,
                                   nickname=user.nickname, user_image = user.profile_image, email = user.email, id = reply.id))
        like_count = Like.objects.filter(feed_id=feed_object.id, is_like=True).count()
        is_liked = Like.objects.filter(feed_id=feed_object.id, email=email, is_like=True).exists()
        is_marked = Bookmark.objects.filter(feed_id=feed_object.id, email=email, is_marked=True).exists()

        feed = {
            'id': feed_object.id,
            'image': feed_object.image,
            'content': feed_object.content,
            'like_count': like_count,
            'profile_image': user_content.profile_image,
            'nickname': user_content.nickname,
            'reply_list': reply_list,
            'is_liked': is_liked,
            'is_marked': is_marked,
            'date_time' : feed_object.date_time,
            'email' : feed_object.email,
            'category' : feed_object.category

        }

        #user = User.objects.filter(email=email).first()  # 로그인 한 사용자의 정보(이게 굳이 필요가 있는지는 모르겠다.)
        # 탬플릿에서 그냥 세션값으로 처리 할 수 있으면 굳이 필요 없을듯
        if user_content is None:
            return render(request, "user/login.html")

        # 해당 피드가 없으면 메인페이지로 돌아가기
        return render(request, 'content/style_view.html', context=dict(
                                                              feed=feed, user=user_content, user_content=user_content, email=email))

