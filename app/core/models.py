from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

"""
https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
"""


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extrafields):
        """create and save new user"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        # https://stackoverflow.com/questions/57667334/what-is-the-value-of-self-db-by-default-in-django

        return user

    def create_superuser(self, email, password):
        """Create and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
