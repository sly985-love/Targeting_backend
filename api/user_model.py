from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# UserManagerBase包含创建新用户的逻辑
class UserManagerBase(BaseUserManager):
    """UserManager doc"""

    # 创建新用户
    def create_user(self, name, army, telephone, **extra_fields):
        """Creates and saves a new User"""
        if not name:
            raise ValueError('Users must have a name ')
        user = self.model(name=name, army=army, telephone=telephone, **extra_fields)
        user.save(using=self._db)
        return user

        # 创建超级用户

    def create_superuser(self, name, password, **extra_fields):
        """Creates and saves a new  superuser"""
        # user = self.create_user(name, password)
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 需要在用户表里存储什么样的信息
class UserBase(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    name = models.CharField(max_length=255, verbose_name='用户姓名', unique=True)
    army = models.CharField(max_length=255, default='', verbose_name='用户所在部队')
    telephone = models.CharField(max_length=255, default='', verbose_name='用户联系方式')  # , unique=True 是否用用户电话作为用户的唯一标识
    target = models.CharField(max_length=255, default='', verbose_name='用户所选靶位', help_text='仅战士用户填写')
    is_active = models.BooleanField(default=True)  # 用户是否已经激活
    is_staff = models.BooleanField(default=False)  # 用户是否为战士
    objects = UserManagerBase()  # 用户创建的方式
    USERNAME_FIELD = 'name'  # 用户的姓名作为用户的唯一标识
