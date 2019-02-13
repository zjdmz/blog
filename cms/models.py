from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import time

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, telephone, password, email, **kwargs):
        user = self.model(username=username, telephone=telephone,email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, email = None, **kwargs):
        kwargs["is_superuser"] = False
        return self._create_user(username, telephone, password, email, **kwargs)

    def create_superuser(self, username, telephone, password, email=None, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = 1
        return self._create_user(username, telephone, password, email, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100,null=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    create_time = models.DateTimeField('注册时间', auto_now_add=True)
    last_login = models.DateTimeField("最近登录时间", auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-create_time"]

    USERNAME_FIELD = 'telephone'  # 进行验证的时候的字段
    REQUIRED_FIELDS = ['username']  # 使用createsuperuser命令时指定的字段
    EMAIL_FIELD = 'email'  # 发送邮箱时指定的字段
    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_staffs(self):
        return self.is_staff

    def create_times(self):
        return self.create_time.strftime("%Y年%m月%d日  %H:%M:%S")

    def last_login_time(self):
        return self.last_login.strftime("%Y年%m月%d日  %H:%M:%S")