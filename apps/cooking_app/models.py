from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.
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