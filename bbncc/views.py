from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User

from .models import Problem
from .forms import UserForm

# TODO
# 1. BLOCK ALL PAGES BEFORE CONTEST STARTS
# 2. Restrict download source to once per minute

problem_cache = {}

def loginView(request):

	if request.method == "POST":

		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("/")

	return render(request, "login.html", {})

def logoutView(request):

	logout(request)

	return redirect('/')

def contest1(request):

	if request.user.is_authenticated() == False:
		return redirect("/login/")


	problems = Problem.objects.all()

	return render(request, "contest1.html", {"problems": problems})

def problem(request, problem_id):

	if request.user.is_authenticated() == False:
		return redirect("/login/")

	if problem_id in problem_cache:
		problem = problem_cache[problem_id]

	else:
		try:
			problem = Problem.objects.get(id=problem_id)
			problem_cache[problem_id] = problem

		except Problem.DoesNotExist:
			raise Http404("<h1>Page does not exist.")


	return render(request, "problem.html", {"problem": problem})

def register(request):

	if request.method == "POST":

		form = UserForm(request.POST)
		
		if form.is_valid():

			user = form.save(commit=False)
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			email = form.cleaned_data["email"]

			user.set_password(password)

			user.save()

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
	
					return redirect("/contest1/")

	return render(request, "register.html", {})
