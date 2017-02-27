from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings

from django.utils.encoding import smart_str

from .models import Problem, SourceURL, InputURL, Submission, Contest
from problem_id_hashes import id_hashes
from datetime import datetime

import subprocess, os

# START cache declarations

problem_cache = {}
submission_cache = {}
source_url_cache = ""
input_url_cache = ""
problems = []
users = []
contest = []

# END cache declations
# Ensure all caches are reset in cachereset()

def custom_404():

    return HttpResponse("<h1>Page does not exist.</h1>")

def limit_exceeded():

    return HttpResponse("<h1>Request Limit exceeded.</h1>")

def get_recent_contest():

    # Returns contest with the nearest end time.

    global contest

    if len(contest) == 0 or contest[0].end_time < timezone.now():
        contest = Contest.objects.all().order_by("-end_time")

    return contest[0]

def get_all_problems(contest=get_recent_contest()):

    global problems

    if len(problems) == 0:
        problems = Problem.objects.all().filter(contest=contest)

    return problems

def get_all_users():

    global users

    if len(users) == 0:
        users = User.objects.all()

    return users

def validate_submission(user, problem):

    # Confirms if time is within deadline

    submission = get_sumbission_object(user, problem)
    
    contest = get_recent_contest()

    current_time = timezone.now()

    print submission.submit_time

    if (current_time <= submission.deadline 
        and submission.submit_time is None
        and current_time <= contest.end_time):

        return True

    else:
        return False

def get_problem_object(problem_id):

    # Get problem by problem_id. Cached.
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

    return settings.ORIGINAL_SOURCE_URL

def get_input_url():

    return settings.ORIGINAL_INPUT_URL


def get_sumbission_object(user, problem):

    if (user.username, problem) in submission_cache:

        return submission_cache[(user.username, problem_id)]

    else:
        submission = Submission.objects.filter(user=user).filter(problem=problem)

        if len(submission) == 0:
            return None
        elif len(submission) == 1:
            return submission[0]
        else:
            with open("notorious_activity.txt", "w") as f:
                f.write(submission)

            return submission[0]


def source_download(request, problem_id):

    problem = get_problem_object(problem_id)

    if problem == None:
        return custom_404()

    url = problem.source_file.url

    filename = os.path.basename(problem.source_file.name)

    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(url)

    return response


def input_download(request, problem_id):

    # Triggers input file download, Also adds entry in Submission model

    problem = get_problem_object(problem_id)

    if problem == None:
        return custom_404()

    prev_submission = Submission.objects.filter(user=request.user).filter(problem=problem)

    if len(prev_submission) > 0:
        return limit_exceeded()

    submission = Submission(user=request.user, problem=problem)
    submission.save()

    url = problem.input_file.url
    filename = os.path.basename(problem.input_file.name)

    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    response['X-Sendfile'] = smart_str(url)

    return response


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

    contest = get_recent_contest()

    if contest.start_time > timezone.now():
        prob_list = []
        start_time = contest.start_time

    else:
        prob_list = get_all_problems(contest)
        start_time = 0

    return render(request, "contest1.html", {"problems": prob_list, "start_time": start_time})

def problem(request, problem_id):

    if request.user.is_authenticated() == False:
        return redirect("/login/")

    submission_success = False
    was_submission = False

    if request.method == "POST":
        
        was_submission = True

        if validate_submission(request.user, get_problem_object(problem_id)) and 'source' in request.FILES and 'output' in request.FILES:

            source = request.FILES['source']
            output = request.FILES['output']

            source.name = str(request.user.id) + "_" + str(id_hashes[problem_id]) + "_source"
            output.name = str(request.user.id) + "_" + str(id_hashes[problem_id]) + "_output"

            fs = FileSystemStorage(location=settings.SUBMISSION_SOURCE_URL)
            fs.save(source.name, source)

            fs = FileSystemStorage(location=settings.SUBMISSION_OUTPUT_URL)
            fs.save(output.name, output)

            submission = get_sumbission_object(request.user, get_problem_object(problem_id))

            submission.submit_time = datetime.now()
            submission.source_filename = source.name
            submission.output_filename = output.name

            submission.save()

            submission_success = True

    submission_message = ""

    if was_submission == True:
        if submission_success == True:
            submission_message = "Submitted solution."
        else:
            submission_message = "Submission unsucessful."

    problem = get_problem_object(problem_id)
    submission = get_sumbission_object(request.user, problem)

    input_button_disabled = ""

    if submission is not None:
        input_button_disabled = "disabled"

    if problem == None:

        return custom_404()

    return render(request, "problem.html", {"problem": problem, "input_button_disabled": input_button_disabled, "sub_mess": submission_message})

def console(request):

    if request.user.is_superuser == True:

        if request.method == "POST":

            # problem_id here refers to auto generated primary key
            userid = request.POST["userid"]
            problem_id = request.POST["problem_id"]

            if userid == "all" and problem_id == "all":
                
                users = get_all_users()
                problems = get_all_problems()
                
                for user in users:
                    for problem in problems:
                        validate_user_problem(user, problem)
                            

            elif userid == "all":
                
                users = get_all_users()

                for user in users:

                    problem = Problem.objects.get(id=problem_id)
                    validate_user_problem(user, problem)

            elif problem_id == "all":

                problems = get_all_problems()
                user = User.objets.get(id=userid)

                for problem in problems:

                    validate_user_problem(user, problem)

            else:
                
                user = User.objects.get(id=userid)
                problem = Problem.objects.get(id=problem_id)

                validate_user_problem(user, problem)


        problems = get_all_problems()

        users = get_all_users()

        return render(request, "console.html", {"users": users, "problems": problems})


    else:
        redirect("/")

def validate_user_problem(user, problem):

    with open("validator_logs.txt", "a+") as f:
        f.write("username: " + user.username + " | problem_nick: " + problem.nick + " | ")
                            
        submission = get_sumbission_object(user, problem)

        if submission is None:
            f.write(" No submission\n")

        elif submission.submit_time is not None:

            if submission.output_filename is None:

                f.write("Output file name is None\n")
            
            elif len(submission.output_filename) == 0:

                f.write("Empty output file name\n")
            
            else:

                ret = validate(submission.output_filename, problem.validator)

                if ret == "0":
                    submission.evaluation_result = "CORRECT"
                else:
                    submission.evaluation_result = "WRONG (#" + ret + ")"

                submission.save()
                f.write(ret + "\n")


def validate(output, validator):

    cmd = ["./validators/" + validator, output]

    return str(subprocess.call(cmd))


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
    global problem_cache
    global submission_cache
    global source_url_cache
    global input_url_cache
    global problems
    global users
    global contest
    
    problem_cache = {}
    submission_cache = {}
    source_url_cache = ""
    input_url_cache = ""
    problems = []
    users = []
    contest = []

    return HttpResponse("<h1>All cache were reset<br> --Emperor of Pragusia </h1>") 