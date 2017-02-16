from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User

from .models import Problem, SourceURL
from .forms import UserForm
from problem_id_hashes import id_hashes

problem_cache = {}
source_url_cache = ""
problems = []

def custom_404():

	return HttpResponse("<h1>Page does not exist.</h1>")

def get_problem_object(problem_id):

	# Get problem by problem_id. Includes caching mechanism.
	# Returns problem object if found, None otherwise

	problem = Problem()

	if problem_id in problem_cache:
		problem = problem_cache[problem_id]

	else:
		try:
			problem = Problem.objects.get(problem_id=problem_id)
			problem_cache[problem_id] = problem

		except Problem.DoesNotExist:
			return None

	return problem

def get_source_url():

	if len(source_url_cache) > 0:
		return source_url_cache

	else:
		return SourceURL.objects.all()[0].url

def source_download(request, problem_id):

	problem = get_problem_object(problem_id)

	if problem == None:
		return custom_404()

	url = get_source_url()
	filename = problem.source_filename

	if url[-1] != '/':
		url = url + '/'

	url = url + filename

	return redirect(url)

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

	global problems 

	if len(problems) == 0:
		problems = Problem.objects.all()
		for problem in problems:
			problem_cache[problem.problem_id] = problem

	return render(request, "contest1.html", {"problems": problems})

def problem(request, problem_id):

	if request.user.is_authenticated() == False:
		return redirect("/login/")

	problem = get_problem_object(problem_id)

	if problem == None:

		return custom_404()

	return render(request, "problem.html", {"problem": problem})

def register(request):

	logout(request)

	if request.method == "POST":
		
		user = User()

		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		
		user.username = username
		user.email = email
		user.set_password(password)

		user.save()

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)

				return redirect("/contest/")

	return render(request, "register.html", {})

def cachereset(request):

	# Resets all cache, Use when cache becomes stale.
	problem_cache = {}
	source_url_cache = ""

	return HttpResponse("<h1>All cache were reset<br> --Emperor of Pragusia </h1>")