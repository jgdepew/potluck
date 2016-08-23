from django.shortcuts import render, redirect, reverse
from .models import User

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
	return render(request, 'cooking_app/index.html', {'user': User.objects.get(id=request.session['id'])})

def show_meal(request, id):
	if request.method == 'POST':
		return redirect(reverse('potluck:create'))
	return render(request, 'cooking_app/show_meal.html')\

def show_user(request, id):
	return render(request, 'cooking_app/show_user.html', {'user': User.objects.get(id=id)})

def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect(reverse('potluck:login'))
