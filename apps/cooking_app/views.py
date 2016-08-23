from django.shortcuts import render, redirect, reverse
from .models import User, Comment, Recipe, Ingredient, Measurement, Step
from django.contrib import messages
import datetime

# Create your views here.
def login(request):
	if request.method == "POST" and User.objects.LoginValidation(request):
		return redirect(reverse('potluck:index'))
	return render(request, 'cooking_app/login.html')


def register(request):
	if request.method == "POST" and User.objects.RegisterValidation(request):
		return redirect(reverse('potluck:index'))
	return render(request, 'cooking_app/register.html')


def index(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))
	return render(request, 'cooking_app/index.html', {'user': User.objects.get(id=request.session['id'])})


def show_recipe(request, id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST':
		return redirect(reverse('potluck:create'))
	return render(request, 'cooking_app/show_recipe.html')\


def add_recipe(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST':
		if not Recipe.objects.validateRecipe(request):
			return redirect(reverse('potluck:add_recipe'))
		# recipe = Recipe.objects.make_new_recipe(request)
		recipe = Recipe.objects.create(title=request.POST['title'], creator=User.objects.get(id=request.session['id']), description=request.POST['description'], prep_time_hour=request.POST['prep_time_hour'], prep_time_minute=request.POST['prep_time_minute'], cook_time_hour=request.POST['cook_time_hour'], cook_time_minute=request.POST['cook_time_minute'])
		return redirect(reverse('potluck:edit_recipe', kwargs={'recipe_id': recipe.id}))
	return render(request, 'cooking_app/add_recipe.html', {'user': User.objects.get(id=request.session['id'])})


def edit_recipe(request, recipe_id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	if request.method == 'POST':
		# update recipe here
		pass
	if len(Step.objects.filter(recipe=Recipe.objects.get(id=recipe_id)))>0:
		steps = Step.objects.get(recipe=Recipe.objects.get(id=recipe_id))
		step_count = steps.count() + 1
	else:
		steps = []
		step_count = 1
	return render(request, 'cooking_app/edit_recipe.html', {'user': User.objects.get(id=request.session['id']),'recipe': Recipe.objects.get(id=recipe_id), 'steps':steps, 'step_count': step_count})


def add_step(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	#TODO create step
	return render(request, 'cooking_app/edit_recipe.html', {'recipe': Recipe.objects.get(id=recipe_id), 'steps': Step.objects.get(recipe=Recipe.objects.get(id=recipe_id))})


def update_step(request):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	#TODO update step
	return render(request, 'cooking_app/edit_recipe.html', {'recipe': Recipe.objects.get(id=recipe_id), 'steps': Step.objects.get(recipe=Recipe.objects.get(id=recipe_id))})


def show_user(request, id):
	if 'id' not in request.session:
		return redirect(reverse('potluck:login'))

	#TODO pass in user recipes too!

	return render(request, 'cooking_app/show_user.html', {'user': User.objects.get(id=id)})


def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('potluck:login'))









#
