from django.shortcuts import render, redirect, reverse
from .models import User

# Create your views here.
def login(request):
	return render(request, 'cooking_app/login.html')

def register(request):
	return render(request, 'cooking_app/register.html')

def loginValidation(request):
	if User.objects.LoginValidation(request, request.POST) == False:
		return redirect(reverse('potluck:login'))
	return redirect(reverse('potluck:index'))

def registerValidation(request):
	if User.objects.RegisterValidation(request, request.POST) == False:
		return redirect(reverse('potluck:register'))
	return redirect(reverse('potluck:index'))

def index(request):
	return render(request, 'cooking_app/index.html')

def show_meal(request, id):
	if request.method == 'POST':
		return redirect(reverse('potluck:create'))
	return render(request, 'cooking_app/show_meal.html')\

def show_user(request, id):
	return render(request, 'cooking_app/show_user.html')

def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('potluck:login'))