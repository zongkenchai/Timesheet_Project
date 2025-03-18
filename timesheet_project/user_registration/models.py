import email
from email.policy import default
from multiprocessing.managers import BaseManager
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
# from pytz import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
# from django.contrib.auth.models import User
# from django.forms import ImageField

# Create your models here.
# class Users(models.Model):
# 	username = models.TextField(max_length=50, primary_key=True)
# 	name = models.TextField(max_length=50)
# 	email = models.EmailField(max_length=100)
# 	password = models.TextField()
# 	verified = models.BooleanField()

# class UserProfileInfo(models.Model):

# 	# Create relationship
# 	user = models.OneToOneField(User)

# 	# Add any additional attributes you want
# 	picture = models.ImageField(upload_to='profile_pics')
# 	password = models.PasswordInput()

# 	def __str__(self):
# 		return self.user.username

# class CustomAccountManager(BaseManager):

# 	def create_user(self, email, user_name, name, password, **other_fields):

# 		if not email:
# 			raise ValueError("You must provide a registered email address")

# 		email = self.normalize_email(email)
# 		user = self.model(email= email, user_name=user_name, name=name, **other_fields)
# 		user.set_password(password)
# 		user.save()
# 		return user

# 	def create_superuser(self, email, user_name, name, password, **other_fields):
# 		other_fields.setdefault('is_staff', True)
# 		other_fields.setdefault('is_super_user', True)
# 		other_fields.setdefault('is_active', True)

# 		return self.create_user(email, user_name, name, password, **other_fields)


	

# class NewUser(AbstractBaseUser, PermissionsMixin):
# 	email = models.EmailField(unique=True, primary_key=True)
# 	user_name = models.CharField(max_length=100, unique=True)
# 	name = models.CharField(max_length=100)
# 	start_date = models.DateField(default=timezone.now)
# 	password = models.TextField()
# 	is_staff = models.BooleanField(default=False)
# 	is_active = models.BooleanField(default=False)

# 	objects: CustomAccountManager()

# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['user_name', 'password']

# 	def __str__(self):
# 		return self.user_name


class RegisteredEmail(models.Model):
	email_address = models.EmailField(unique=True)
	name = models.CharField(max_length=100, unique=True)
	is_active = models.BooleanField(default=1)

# class User(AbstractUser):
# 	is_email_verified = models.BooleanField(default=False)

# 	def __str__(self):
# 		return self.email