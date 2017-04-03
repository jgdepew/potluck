from django.shortcuts import render, redirect, reverse
from .models import Comment, Recipe, Ingredient, Measurement, Step, RecipePic, Rating, Category
from ..loginRegistration_app.models import User, UserPic
from django.contrib import messages
import datetime
from django.http import JsonResponse
from .forms import PicsForm
from django.db.models import Q


# Create your views here.
def welcome(request):
	return redirect("loginReg:login")


def index(request):
	if 'id' not in request.session:
		return redirect('loginReg:login')
	context ={
		'user_name': User.objects.get(id=request.session['id']).first_name,
		'recipes': Recipe.objects.all().order_by('-updated_at'),
	}
	return render(request, 'cooking_app/index.html', context)


def show_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	if request.method == 'POST':
		post = Comment.objects.create(comment=request.POST['comment'], user=User.objects.get(id=request.session['id']), recipe=Recipe.objects.get(id=recipe_id))
		return redirect(reverse('main:show_recipe', kwargs={'recipe_id': recipe_id}))

	recipe = Recipe.objects.get(id=recipe_id)
	ratings = recipe.ratings.all()
	sum_rating = 0.
	if len(ratings)>0:
		for rating in ratings:
			sum_rating += rating.rating
		avg_rating = sum_rating / len(ratings)
	else:
		avg_rating = 'No ratings yet.'

	total_time_hour = recipe.prep_time_hour + recipe.cook_time_hour
	total_time_minute = recipe.prep_time_minute + recipe.cook_time_minute

	if len(Rating.objects.filter(user=request.session['id'], recipe=recipe_id))>0:
		rating = False
	else:
		rating = True

	context = {
		'user': User.objects.get(id=request.session['id']),
		'recipe': recipe,
		'avg_rating': avg_rating,
		'total_time_hour': total_time_hour,
		'total_time_minute': total_time_minute,
		'rating': rating,
	}
	return render(request, 'cooking_app/show_recipe.html', context)


def add_recipe(request):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	if request.method == 'POST': # if 'POST' we are trying to add something, else trying to display form to add
		errors = Recipe.objects.validateRecipe(request.POST) #run validations. returns errors if failed
		if len(errors) > 0:
			for error in errors:
				messages.error(request, error)
			return redirect('main:add_recipe')

		#create the recipe if validations passed
		recipe = Recipe.objects.create(title=request.POST['title'], creator=User.objects.get(id=request.session['id']), description=request.POST['description'], prep_time_hour=request.POST['prep_time_hour'], prep_time_minute=request.POST['prep_time_minute'], cook_time_hour=request.POST['cook_time_hour'], cook_time_minute=request.POST['cook_time_minute'])
		#Add Categories
		Category.objects.addCategory(request.POST, recipe)

		#add image
		if 'image' in request.FILES:
			RecipePic.objects.create(title=request.POST['title'], image=request.FILES['image'], recipe=recipe)

		#redirect to edit page so user can add steps to recipe
		return redirect(reverse('main:edit_recipe', kwargs={'recipe_id': recipe.id}))

	return render(request, 'cooking_app/add_recipe.html', {'user': User.objects.get(id=request.session['id']), 'categories': Category.objects.create_categories()})


def edit_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	if request.method == 'POST': # if 'POST' we are trying to update recipe, else trying to display edit page
		#TODO: Implement updating of photo
		# if 'image' in request.FILES:
		# 	RecipePic.objects.update(recipe_id, request.Files)
		if 'title' in request.POST:
			errors = Recipe.objects.validateRecipe(request.POST)
			if len(errors) > 0: # run validations. returns errors if failed
				for error in errors:
					messages.error(request, error)
				return redirect('main:edit_recipe')
			else:
				Recipe.objects.update(request.POST, recipe_id) # passed validation, not update

	context = {
		'user': User.objects.get(id=request.session['id']),
		'recipe': Recipe.objects.get(id=recipe_id),
		'ingredients': Ingredient.objects.all().order_by('ingredient'),
		'measurements': Measurement.objects.all().order_by('measurement'),
		'categories': Category.objects.all(),
	}
	return render(request, 'cooking_app/edit_recipe.html', context)


def delete_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	Recipe.objects.get(id=recipe_id).delete()
	return redirect('main:index')


def add_step(request):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	step = Step.objects.add_step(request.POST) # runs code to validate step and return step after creation
	return redirect(reverse('main:edit_recipe', kwargs={'recipe_id': step.recipe.id}))


def update_step(request, step_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	step = Step.objects.update_step(request.POST, step_id) # runs code to validate step and return step after update
	return redirect(reverse('main:edit_recipe', kwargs={'recipe_id': step.recipe.id}))


def delete_step(request, step_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	Step.objects.get(id=step_id).delete()
	return JsonResponse({'to_delete': step_id})


def show_user(request, id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	if request.method == 'POST':
		if 'image' in request.FILES:
			user_pic = UserPic.objects.pic(request.POST, request.FILES, id)
	else:
		if len(UserPic.objects.filter(user=User.objects.get(id=id))) > 0:
			user_pic = UserPic.objects.get(user=User.objects.get(id=id))
		else:
			user_pic = ''

	context = {
		'self': User.objects.get(id=request.session['id']),
		'user': User.objects.get(id=id),
	}
	return render(request, 'cooking_app/show_user.html', context)


def add_rating(request, recipe_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	Rating.objects.add_rating(recipe_id, request.session['id'], request.POST)
	return redirect(reverse('main:show_recipe', kwargs={'recipe_id':recipe_id}))


def save_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	user = User.objects.get(id=request.session['id'])
	recipe = Recipe.objects.get(id=recipe_id)
	if user in recipe.user.all():
		recipe.user.remove(user)
	else:
		recipe.user.add(user)
	recipe.save()
	return redirect(reverse('main:show_recipe', kwargs={'recipe_id':recipe_id}))


def search(request):
	if 'id' not in request.session:
		return redirect('loginReg:login')

	results = []
	if request.method == 'POST':
		results = Recipe.objects.filter(Q(title__icontains=request.POST['search']) | Q(description__icontains=request.POST['search']))
		if request.POST['category'] != 'noCategory':
			category = Category.objects.get(id=request.POST['category'])
			results = results.filter(categories=category)

	context = {
		'results': results,
		'user': User.objects.get(id=request.session['id']),
		'categories': Category.objects.all(),
	}
	return render(request, 'cooking_app/search.html', context)










#
