from __future__ import unicode_literals
from django.db import models
from ..loginRegistration_app.models import User, UserPic
# import re
# from django.contrib import messages
# import bcrypt

# get things ready for json
# class ItemManager(models.Manager):
#     def as_dict(self, item):
#         return {
#             'id': item.id,
#             'objective': item.objective,
#             'createdAt': item.createdAt.isoformat(),
#             'updatedAt': item.updatedAt.isoformat()
#         }

# Create your models here.
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

		recipe = Recipe.objects.get(id=recipe_id)
		all_categories = Category.objects.all()
		prev_select = Category.objects.filter(recipe=Recipe.objects.get(id=recipe_id))
		for select in prev_select:
			if select.category not in form_info:
				Category.objects.get(category=select.category).recipe.remove(recipe)
		for category in all_categories:
			if category.category in form_info and category not in prev_select:
				Category.objects.get(category=category.category).recipe.add(recipe)



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

class RatingManager(models.Manager):
	def add_rating(self, id, user_id, form_info):
		rating = form_info['rating']
		recipe = Recipe.objects.get(id=id)
		user = User.objects.get(id=user_id)
		Rating.objects.create(recipe=recipe, user=user, rating=rating)

class RecipePicManager(models.Manager):
	def update(self, recipe_id, files):
		if len(RecipePic.objects.filter(recipe=Recipe.objects.get(id=recipe_id))) > 0:
			pic = RecipePic.objects.get(recipe=Recipe.objects.get(id=recipe_id))
			pic.image = files['image']
			pic.save()
			return pic
		else:
			return RecipePic.objects.create(title=Recipe.objects.get(id=recipe_id).title, recipe=Recipe.objects.get(id=recipe_id), image=files['image'])

class CategoryManager(models.Manager):
	def create_categories(self):
		categories = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Drinks', 'Other']
		all_categories = Category.objects.all()
		if len(all_categories) < 1:
			for category in categories:
				Category.objects.create(category=category)
		elif len(all_categories) < len(categories):
			for category in categories:
				if len(Category.objects.filter(category=category)) < 1:
					Category.objects.create(category=category)
		return Category.objects.all()

	def addCategory(self, form_info, recipe):
		categories = Category.objects.all()
		for category in categories:
			if category.category in form_info:
				Category.objects.get(category=category.category).recipe.add(recipe)



class Comment(models.Model):
	comment = models.TextField()
	user = models.ForeignKey(User)
	recipe = models.ForeignKey('Recipe')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Recipe(models.Model):
	title = models.CharField(max_length=255)
	creator = models.ForeignKey(User)
	user = models.ManyToManyField(User, related_name='others')
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
	objects = RecipePicManager()

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

class Rating(models.Model):
	recipe = models.ForeignKey('Recipe')
	user = models.ForeignKey(User)
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = RatingManager()

class Category(models.Model):
	recipe = models.ManyToManyField('Recipe', related_name='recipe_category')
	category = models.CharField(max_length=75)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = CategoryManager()











#
