from __future__ import unicode_literals

from django.db import models
import re  #regex
import bcrypt  #encryption
# from django.contrib import messages #to display errors
# from datetime import datetime
# from django.core.exceptions import ValidationError

# Create your models here.
class UserManager(models.Manager):
	def RegisterValidation(self, form_info):
		if 'password' in form_info:
			return False

		errors = []
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		first_name = form_info['first_name']
		last_name = form_info['last_name']
		email = form_info['email']
		password1 = form_info['password1']
		password2 = form_info['password2']
		if  len(User.objects.all()) < 1:
			user_level = 9
		else:
			user_level = 1

		if len(email)<1:
			errors.append('No email entered.')
		elif not EMAIL_REGEX.match(email):
			errors.append('Not a valid email.')
		elif User.objects.filter(email=email):
			errors.append('Email already in use.')

		if len(first_name) < 2 or len(first_name) < 2:
			errors.append('First and last name must be longer than 2 characters.')

		if password1 != password2:
			errors.append('Passwords do not match.')
		elif len(password1)<8:
			errors.append('Password must be at least 8 characters.')

		if len(errors) > 0:
			return (errors)
		else:
			password = str(password1)
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=first_name, last_name=last_name,email=email, password=hashed, user_level=user_level, description=None)
			user = User.objects.get(email=email)
			# request.session['id'] = user.id
			# request.session['user_level'] = user.user_level
			return (errors, user.id, user.user_level)

	def LoginValidation(self, form_info):
		errors = []
		email = form_info['email']
		password = form_info['password']
		if len(User.objects.filter(email=email))<1:
			errors.append('Invalid login information.')
			return (errors)
		user = User.objects.get(email=email)
		password_entered = password.encode()
		hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
		if email == user.email and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
			# request.session['id'] = user.id
			# request.session['user_level'] = user.user_level
			return (errors, user.id, user.user_level)
		else:
			errors.append('Password incorrect.')
			return (errors)

class UserPicManager(models.Manager):
	def pic(self, post, files, user_id):
		if len(UserPic.objects.filter(user=User.objects.get(id=user_id))) > 0:
			pic = UserPic.objects.get(user=User.objects.get(id=user_id))
			pic.image = files['image']
			pic.save()
			return pic
		else:
			return UserPic.objects.create(user=User.objects.get(id=user_id), image=files['image'])

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	user_level = models.IntegerField()
	description = models.CharField(max_length=255, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class UserPic(models.Model):
	image = models.ImageField(upload_to='UserPics')
	user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='pic')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserPicManager()
