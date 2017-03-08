from django.shortcuts import render, redirect
from .models import User, UserPic
from django.contrib import messages
# import datetime
# from django.http import JsonResponse
# from .forms import PicsForm
# from django.db.models import Q




def login(request):
	if request.method == "POST":
		results = User.objects.LoginValidation(request.POST)
		if len(results[0])<1:
			request.session['id'] = results[1]
			request.session['user_level'] = results[2]
			return redirect('main:index')
		else:
			for error in results:
				messages.error(request, error)
	return render(request, 'loginRegistration/login.html')


def register(request):
	if request.method == "POST":
		results = User.objects.RegisterValidation(request.POST)
		if len(results[0])<1:
			request.session['id'] = results[1]
			request.session['user_level'] = results[2]
			return redirect('main:index')
		else:
			for error in results:
				messages.error(request, error)
	return render(request, 'loginRegistration/register.html')


def logout(request):
	for key in request.session.keys():
		del request.session[key]
	return redirect('main:welcome')
