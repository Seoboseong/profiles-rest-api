from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """ UserProfile을 위한 Manager

    Args:
        BaseUserManager (BaseUserManager): 기본 user manage class
    """
    def create_user(self, email, name, password=None):
        """ user profiles 생성

        Args:
            email (string): user email
            name (string): user name
            password (string, optional): user password. Defaults to None.

        Raises:
            ValueError: email을 입력하지 않았을 경우

        Returns:
            user: user 객체
        """
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """ superuser profiles 생성

        Args:
            email (string): superuser email
            name (string): superuser name
            password (string): superuser password

        Returns:
            user: superuser 객체
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ system에서 user를 위한 database model

    Args:
        AbstractBaseUser (AbstractBaseUser): 추상화된 user class
        PermissionsMixin (PermissionsMixin): 혼합 권한 class
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ user의 full name을 검색하여 return

        Returns:
            string: user의 full name
        """
        return self.name
    
    def get_short_name(self):
        """ user의 short name을 검색하여 return

        Returns:
            string: user의 short name
        """
        return self.name
    
    def __str__(self):
        """ user의 email을 return

        Returns:
            string: user의 email
        """
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text