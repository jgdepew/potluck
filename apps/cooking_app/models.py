from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def RegisterValidation(self, request):
		if 'password' in request.POST:
			return False

		errors = 0
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if  len(User.objects.all()) < 1:
			user_level = 9
		else:
			user_level = 1

		if len(email)<1:
			messages.error(request, 'No email entered.')
			errors += 1
		elif not EMAIL_REGEX.match(email):
			messages.error(request, 'Not a valid email.')
			errors += 1
		elif User.objects.filter(email=email):
			messages.error(request, 'Email already in use.')
			errors += 1

		if len(first_name) < 2 or len(first_name) < 2:
			messages.error(request, 'First and last name must be longer than 2 characters.')
			errors += 1

		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			errors += 1
		elif len(password1)<8:
			messages.error(request, 'Password must be at least 8 characters.')
			errors += 1

		if errors > 0:
			return False
		else:
			password = str(password1)
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=first_name, last_name=last_name,email=email, password=hashed, user_level=user_level, description=None)
			user = User.objects.get(email=email)
			request.session['id'] = user.id
			request.session['user_level'] = user.user_level
			return True

	def LoginValidation(self, request):
		if 'first_name' in request.POST:
			return False

		email = request.POST['email']
		password = request.POST['password']
		if len(User.objects.filter(email=email))<1:
			messages.error(request, 'Invalid login information.')
			return False
		user = User.objects.get(email=email)
		password_entered = password.encode()
		hashed_entered = bcrypt.hashpw(password_entered, bcrypt.gensalt())
		if email == user.email and bcrypt.hashpw(password_entered, user.password.encode()) == user.password:
			request.session['id'] = user.id
			request.session['user_level'] = user.user_level
			return True
		else:
			messages.error(request, 'Password incorrect.')
			return False



class RecipeManager(models.Manager):
	def validateRecipe(self, request):
		no_errors = True
		if len(request.POST['title']) < 1:
			messages.error(request, 'Title must be filled out')
			no_errors = False
		if len(request.POST['description']) < 1:
			messages.error(request, 'Description must be filled out')
			no_errors = False
		if len(request.POST['prep_time_hour']) < 1:
			messages.error(request, 'Prep Time Hour must be filled out')
			no_errors = False
		# if int(request.POST['prep_time_hour']) >= 0:
		# 	messages.error(request, 'Prep Time Hour must be a number 0 or more')
		# 	no_errors = False
		if len(request.POST['prep_time_minute']) < 1:
			messages.error(request, 'Prep Time minute must be filled out')
			no_errors = False
		# if int(request.POST['prep_time_minute']) >= 0 and int(request.POST['prep_time_minute']) < 60:
		# 	messages.error(request, 'Prep Time minute must be a number 0 or more and less than 60')
		# 	no_errors = False
		if len(request.POST['cook_time_hour']) < 1:
			messages.error(request, 'Cook Time Hour must be filled out')
			no_errors = False
		# if int(request.POST['cook_time_hour']) >= 0:
		# 	messages.error(request, 'Cook Time Hour must be a number 0 or more')
		# 	no_errors = False
		if len(request.POST['cook_time_minute']) < 1:
			messages.error(request, 'Cook Time minute must be filled out')
			no_errors = False
		# if int(request.POST['cook_time_minute']) >= 0 and int(request.POST['cook_time_minute']) < 60:
		# 	messages.error(request, 'Cook Time minute must be a number 0 or more and less than 60')
		# 	no_errors = False
		return no_errors

	def update(self, request, recipe_id):
		recipe = Recipe.objects.get(id=recipe_id)
		recipe.title = request.POST['title']
		recipe.description = request.POST['description']
		recipe.prep_time_hour = request.POST['prep_time_hour']
		recipe.prep_time_minute = request.POST['prep_time_minute']
		recipe.cook_time_hour = request.POST['cook_time_hour']
		recipe.cook_time_minute = request.POST['cook_time_minute']
		recipe.save()
		messages.success(request, 'Your recipe has been updated')



class StepManager(models.Manager):
	def add_step(self, request):
		measurement = self.find_measurement(request)
		ingredient = self.find_ingrediant(request)
		# create and return step
		return Step.objects.create(recipe=Recipe.objects.get(id=request.POST['recipe_id']), measurement=measurement, ingredient=ingredient, description=request.POST['description'])

	def update_step(self, request, step_id):
		measurement = self.find_measurement(request)
		ingredient = self.find_ingrediant(request)
		# update and return step
		step = Step.objects.get(id=step_id)
		step.measurement = measurement
		step.ingredient = ingredient
		step.description = request.POST['description']
		step.save()
		return step

	def find_measurement(self, request):
		if request.POST['new_measurement'] == '': # They selected an existing measurement
			measurement = Measurement.objects.get(id=request.POST['measurement'])
		else: # They opted to create a new measurement
			#test if measurement is already in the table
			measurements = Measurement.objects.all()
			create = True
			for measure in measurements:
				if measure.measurement == request.POST['new_measurement']: # They typed in an existing measurement
					measurement = measure # this prevents duplicate values
					create = False
					break
			if create: # the measurement they provided is new and should be added
				measurement = Measurement.objects.create(measurement=request.POST['new_measurement'])
		return measurement

	def find_ingrediant(self, request):
		if request.POST['new_ingredient'] == '': # They selected an existing ingredient
			ingredient = Ingredient.objects.get(id=request.POST['ingredient'])
		else: # They opted to create a new ingredient
			#test if ingredient is already in the table
			ingredients = Ingredient.objects.all()
			create = True
			for ingred in ingredients:
				if ingred.ingredient == request.POST['new_ingredient']: # They typed in an existing ingredient
					ingredient = ingred # this prevents duplicate values
					create = False
					break
			if create: # the ingredient they provided is new and should be added
				ingredient = Ingredient.objects.create(ingredient=request.POST['new_ingredient'])
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
