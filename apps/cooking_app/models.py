from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.
class ValidationManager(models.Manager):
	def RegisterValidation(self, request, form_info):
		if 'password' in form_info:
			return False

		errors = 0
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
			messages.error(request, 'No email entered')
			errors += 1
		elif not EMAIL_REGEX.match(email):
			messages.error(request, 'Not a valid email.')
			errors += 1	
		elif User.objects.filter(email=email):
			messages.error(request, 'Email already in use.')
			errors += 1

		if len(first_name) < 2 or len(first_name) < 2:
			messages.error(request, 'Name must be longer than 2 characters.')
			errors += 1

		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			errors += 1			
		elif len(password1)<8:
			messages.error(request, 'Not a valid password.')
			errors += 1			

		if errors > 0:
			return False
		else:
			password = str(password1)
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=first_name, last_name=last_name,email=email, password=hashed, user_level=user_level, description=None)
			user = User.objects.get(email=email)
			request.session['name'] = user.first_name
			request.session['id'] = user.id
			request.session['user_level'] = user.user_level
			request.session['email'] = user.email			
			return True
	def LoginValidation(self, request, form_info):
		if 'first_name' in form_info:
			return False

		email = form_info['email']
		password = form_info['password']
		if len(User.objects.filter(email=email))<1:
			messages.error(request, 'Invalid login information.')
			return False
		user = User.objects.get(email=email)
		password_entered = password.encode()
		hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
		if email == user.email and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
			request.session['name'] = user.first_name
			request.session['id'] = user.id
			request.session['user_level'] = user.user_level
			request.session['email'] = user.email
			return True
		else: 
			messages.error(request, 'Password incorrect.')
			return False

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	user_level = models.IntegerField()
	description = models.CharField(max_length=255, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ValidationManager()

class Comment(models.Model):
	comment = models.CharField(max_length=255)
	user = models.ForeignKey('User')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	

class Recipe(models.Model):
	user = models.ManyToManyField('User')
	description = models.CharField(max_length=1000)
	prep_time = models.DateTimeField()
	cook_time = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Ingredient(models.Model):
	ingredient = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Measurement(models.Model):
	measurement = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Step(models.Model):
	recipe = models.ForeignKey('Recipe')
	measurement = models.ForeignKey('Measurement')
	ingredient = models.ManyToManyField('Ingredient')
	step = models.IntegerField()
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)