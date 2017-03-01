from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings

from wsgiref.util import FileWrapper
import mimetypes

from django.utils.encoding import smart_str

from .models import Problem, SourceURL, InputURL, Submission, Contest
from problem_id_hashes import id_hashes
from datetime import datetime
from .forms import SubmissionForm
from utility import tokenize_file

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

def launch_download(path):

    wrapper = FileWrapper(open(path, "r" ) )
    content_type = mimetypes.guess_type(path)[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path)

    return response

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

    path = problem.source_file.path

    return launch_download(path)


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

    path = problem.input_file.path

    return launch_download(path)


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

    input_button_disabled = ''

    problem = get_problem_object(problem_id)

    # 1. input button disable

    if request.method == "POST":

        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid() and validate_submission(request.user, get_problem_object(problem_id)):

            source = request.FILES['source_file']
            output = request.FILES['output_file']

            submission = get_sumbission_object(request.user, get_problem_object(problem_id))

            submission.submit_time = datetime.now()
            submission.source_file = source
            submission.output_file = output

            submission.save()

    else:
        form = SubmissionForm()

    return render(request, "problem.html", {"problem": problem, "input_button_disabled": input_button_disabled, 'form': form})

def console(request):

    if request.user.is_authenticated() == False:
        return redirect('/')

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

    if user.username == "server":
        return

    with open("validator_logs.txt", "a+") as f:
        f.write("username: " + user.username + " | problem_nick: " + problem.nick + " | ")

        submission = get_sumbission_object(user, problem)

        if submission is None:
            f.write(" No submission\n")

        elif submission.submit_time is not None:

            if submission.output_file is None:

                f.write("Output file name is None\n")

            elif len(submission.output_file) == 0:

                f.write("Empty output file name\n")

            else:

                ret = validate(problem.validator.url,
                                 problem.input_file.url,
                                    submission.output_file.url)

                if ret == "0":
                    submission.evaluation_result = "1"
                    penalty = calculate_penalty(problem, submission.source_file.url)
                    submission.penalty = penalty
                    contest = get_recent_contest()
                    submission.time_penalty = (submission.submit_time - contest.start_time).total_seconds() // 60
                    submission.points = problem.points - penalty
                    ret = "CORRECT ANSWER"

                else:
                    submission.evaluation_result = "-1"
                    ret = "WRONG ANSWER #" + int(ret)

                submission.save()

                f.write(ret + "\n")


def calculate_penalty(problem, submission_source=""):

    t_org_source_path = os.path.join(settings.ORIGINAL_TOKENIZED_URL, os.path.basename(problem.source_file.name))
    t_sub_source_path = os.path.join(settings.SUBMISSION_TOKENIZED_URL, os.path.basename(submission_source))

    t_org_source = open(t_org_source_path, 'r')

    t_source_content = tokenize_file(submission_source)

    f = open(t_sub_source_path, "w")
    f.write(t_source_content)
    f.close()

    #diff file1 file2 | grep "^>" | wc -l

    cmd = "diff %s %s | grep '^>' | wc -l" % (t_org_source_path, t_sub_source_path)
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

    penalty = int(output)

    penalty = problem.penalty_per_line * penalty

    return penalty

def validate(validator, input_file, output_file):

    os.chmod(validator, 0777)
    cmd = [validator, input_file, output_file]

    return str(subprocess.call(cmd))

def scoreboard(request):

    if request.user.is_authenticated() == False:
        redirect('/login')

    score_d = []

    users = get_all_users()
    problems = get_all_problems()

    for user in  users:
        res = {}
        t_penalty = 0
        no_of_submission = 0
        sub_penalty = []
        sub_status = []
        tot_points = 0

        for problem in problems:
            s_object = get_sumbission_object(user, problem)

            if s_object.submit_time is None:
                sub_status.append(2)
                sub_penalty.append(0)
            else :
                no_of_submission = no_of_submission - 1
                t_penalty = t_penalty + s_object.time_penalty
                var = int(s_object.evaluation_result);
                if get_recent_contest().end_time < timezone.now()
                    sub_status.append(var)
                else :
                    if var == -1 or var == 1 :
                        sub_status.append(0)
                    else :
                        sub_status.append(var)
                sub_penalty.append(s_object.penalty)
                tot_points = tot_points + s_object.points

        if no_of_submission == 0 :
            continue

        tot_points = tot_points - t_penalty;
        res[username] = user.username
        res[time_penalty] = t_penalty
        res[number_of_submission] = no_of_submission
        res[submission_status] = sub_status
        res[submission_penalty] = sub_penalty
        res[total_points] = tot_points

        score_d.append(res)

    if get_recent_contest().end_time < timezone.now() :
        score_d.sort(key=lambda k : k['total_points'],reverse = true)
    else :
        score_d.sort(key=lambda k : (k['number_of_submission'],k['time_penalty']))

    return render(request, 'scoreboard.html', {'scores': score_d, 'problems': problems})

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
