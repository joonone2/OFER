from django.db import models

# Create your models here.
class Feed(models.Model):  # 게시물
    content = models.TextField()    # 글내용
    image = models.ImageField(upload_to='feed_images/')  # 피드 이미지
    email = models.EmailField(default='')


class Like(models.Model):  #게시물 좋아요
    feed_id = models.IntegerField(default=0) #게시물 고유번호
    email = models.EmailField(default='')  #좋아요 누른사람 이메일 => 이거 count해서 feed에 좋아요 수 뿌려줌
    is_like = models.BooleanField(default=True) #좋아요 눌렀는지 여부


class Reply(models.Model): #댓글
    feed_id = models.IntegerField(default=0) #게시물 고유번호
    email = models.EmailField(default='') #댓글 쓴사람 email
    reply_content = models.TextField() #댓글 본문


class Bookmark(models.Model): #저장
    feed_id = models.IntegerField(default=0)  #게시물 고유번호
    email = models.EmailField(default='')   #저장한 사람의 email
    is_marked = models.BooleanField(default=True)   #저장했는지 여부(저장했는데 또 저장하면 안되니까)

