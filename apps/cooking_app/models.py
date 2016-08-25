from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

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



class RecipeManager(models.Manager):
	def validateRecipe(self, form_info):
		errors = []
		if len(form_info['title']) < 1:
			errors.append('Title must be filled out')
		if len(form_info['description']) < 1:
			errors.append('Description must be filled out')
		if len(form_info['prep_time_hour']) < 1:
			errors.append('Prep Time Hour must be filled out')
		# if int(form_info['prep_time_hour']) >= 0:
		# 	errors.append('Prep Time Hour must be a number 0 or more')
		if len(form_info['prep_time_minute']) < 1:
			errors.append('Prep Time minute must be filled out')
		# if int(form_info['prep_time_minute']) >= 0 and int(form_info['prep_time_minute']) < 60:
		# 	errors.append('Prep Time minute must be a number 0 or more and less than 60')
		if len(form_info['cook_time_hour']) < 1:
			errors.append('Cook Time Hour must be filled out')
		# if int(form_info['cook_time_hour']) >= 0:
		# 	errors.append('Cook Time Hour must be a number 0 or more')
		if len(form_info['cook_time_minute']) < 1:
			errors.append('Cook Time minute must be filled out')
		# if int(form_info['cook_time_minute']) >= 0 and int(form_info['cook_time_minute']) < 60:
		# 	errors.append('Cook Time minute must be a number 0 or more and less than 60')
		return errors
	def update(self, form_info, recipe_id):
		recipe = Recipe.objects.get(id=recipe_id)
		recipe.title = form_info['title']
		recipe.description = form_info['description']
		recipe.prep_time_hour = form_info['prep_time_hour']
		recipe.prep_time_minute = form_info['prep_time_minute']
		recipe.cook_time_hour = form_info['cook_time_hour']
		recipe.cook_time_minute = form_info['cook_time_minute']
		recipe.save()

class StepManager(models.Manager):
	def add_step(self, form_info):
		measurement = self.find_measurement(form_info)
		ingredient = self.find_ingrediant(form_info)
		# create and return step
		return Step.objects.create(recipe=Recipe.objects.get(id=form_info['recipe_id']), measurement=measurement, ingredient=ingredient, description=form_info['description'])

	def update_step(self, form_info, step_id):
		measurement = self.find_measurement(form_info)
		ingredient = self.find_ingrediant(form_info)
		# update and return step
		step = Step.objects.get(id=step_id)
		step.measurement = measurement
		step.ingredient = ingredient
		step.description = form_info['description']
		step.save()
		return step

	def find_measurement(self, form_info):
		if form_info['new_measurement'] == '': # They selected an existing measurement
			measurement = Measurement.objects.get(id=form_info['measurement'])
		else: # They opted to create a new measurement
			#test if measurement is already in the table
			measurements = Measurement.objects.all()
			create = True
			for measure in measurements:
				if measure.measurement == form_info['new_measurement']: # They typed in an existing measurement
					measurement = measure # this prevents duplicate values
					create = False
					break
			if create: # the measurement they provided is new and should be added
				measurement = Measurement.objects.create(measurement=form_info['new_measurement'])
		return measurement

	def find_ingrediant(self, form_info):
		if form_info['new_ingredient'] == '': # They selected an existing ingredient
			ingredient = Ingredient.objects.get(id=form_info['ingredient'])
		else: # They opted to create a new ingredient
			#test if ingredient is already in the table
			ingredients = Ingredient.objects.all()
			create = True
			for ingred in ingredients:
				if ingred.ingredient == form_info['new_ingredient']: # They typed in an existing ingredient
					ingredient = ingred # this prevents duplicate values
					create = False
					break
			if create: # the ingredient they provided is new and should be added
				ingredient = Ingredient.objects.create(ingredient=form_info['new_ingredient'])
		return ingredient






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

class Comment(models.Model):
	comment = models.CharField(max_length=255)
	user = models.ForeignKey('User')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
	title = models.CharField(max_length=255)
	creator = models.ForeignKey('User')
	user = models.ManyToManyField('User', related_name='others')
	description = models.CharField(max_length=1000)
	prep_time_hour = models.IntegerField()
	prep_time_minute = models.IntegerField()
	cook_time_hour = models.IntegerField()
	cook_time_minute = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = RecipeManager()

class RecipePic(models.Model):
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to='FoodPics')
	recipe = models.OneToOneField('Recipe', on_delete=models.CASCADE)
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
	ingredient = models.ForeignKey('Ingredient')
	description = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = StepManager()













#
