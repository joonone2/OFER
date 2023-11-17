from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    """
        유저 프로필 사진
        유저 아이디 -> 닉네임
        유저 이름 -> 실제 사용자 이름(우리는 필요 없을수도!)
        유저 이메일주소 -> 회원가입할때 사용하는 아이디
        유저 비밀번호 -> 디폴트로 쓸께요
    """
    profile_image = models.ImageField(upload_to='user_profile_images/')  # 프로필 이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"
