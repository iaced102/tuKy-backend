from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userName, password, **extra_fields):
        """
            Creates and saves a User with the given email and password.
            """
        if not userName:
            raise ValueError('The given email must be set')
        user = self.model(userName=userName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userName, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(userName, password, **extra_fields)

    def create_superuser(self, userName, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(userName, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    userNameDisplay = models.CharField(_('user name display'), max_length=35)
    userName = models.CharField(_('user name'), max_length=35, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userName'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
