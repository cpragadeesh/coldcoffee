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
from .forms import SubmissionForm, SourceSubmissionForm, RegistrationForm
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

    if len(contest) == 0:
        contest = Contest.objects.all().filter(end_time__gt = timezone.now()).order_by('end_time')
        if len(contest) == 0:
            contest = Contest.objects.all().order_by('end_time')
            return contest[len(contest) - 1]

    if contest[0].end_time < timezone.now():
        contest = contest[1:]
        if len(contest) == 0:
            contest = Contest.objects.all().order_by('end_time')
            return contest[len(contest) - 1]

    print 33333
    print contest

    return contest[0]


def get_all_problems(contest=get_recent_contest()):

    global problems

    if len(problems) == 0:
        problems = Problem.objects.all().filter(contest=contest).order_by("points")

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

    error = ""

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")

        error = "Invalid login details"

    return render(request, "login.html", {'error': error})
    

def logoutView(request):

    logout(request)

    return redirect('/')

def contest_switch(request):

    if request.user.is_authenticated() == False:
        return redirect("/login/")

    contest = get_recent_contest()

    if contest.phase == 1:
        return redirect("/contest1/")

    else:
        return redirect("/contest2/")

def contest1(request):
    
    if request.user.is_authenticated() == False:
        return redirect("/login/")

    problems = Problem.objects.all().filter(source_author=request.user)

    start_time = get_recent_contest().start_time
    if start_time <= timezone.now():
        start_time = 0

    print start_time

    return render(request, "problems_page.html", {"problems": problems, "start_time": start_time})

def contest2(request):

    if request.user.is_authenticated() == False:
        return redirect("/login/")

    contest = get_recent_contest()

    start_time = contest.start_time

    if contest.start_time > timezone.now():
        prob_list = []

    else:
        prob_list = get_all_problems(contest)
        start_time = 0

    return render(request, "problems_page.html", {"problems": prob_list, "start_time": start_time})

def problem(request, problem_id):

    if request.user.is_authenticated() == False:
        return redirect("/login/")

    problem = get_problem_object(problem_id)

    if get_recent_contest().phase == 1:
        return render(request, "problem_phase1.html", {"problem": problem})
    
    if get_recent_contest().phase == 2:
        return render(request, "problem.html", {"problem": problem})

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
                user = User.objects.get(id=userid)

                for problem in problems:

                    validate_user_problem(user, problem)

            else:

                user = User.objects.get(id=userid)
                problem = Problem.objects.get(id=problem_id)

                validate_user_problem(user, problem)


        problems = get_all_problems()

        users = get_all_users()

        validation_log_content = ""

        with open("validator_logs.txt", "r") as f:
            validation_log_content = f.read()

        validation_log_content = validation_log_content.replace("\n", "<br>")


        return render(request, "console.html", {"users": users, "problems": problems, "v_log": validation_log_content})


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
                    submission.points = problem.points - penalty
                    ret = "CORRECT ANSWER"

                else:
                    submission.evaluation_result = "-1"
                    ret = "WRONG ANSWER #" + str(ret)

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
    
    print validator
    print input_file
    print output_file

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

        # Submission status codes: 
        #       2 - Hidden results
        #       0 - No submission
        #       1 - Correct Answer
        #      -1 - Wrong Answer

        for problem in problems:
            s_object = get_sumbission_object(user, problem)


            if s_object is None or s_object.submit_time is None:
                sub_status.append(0)
                sub_penalty.append(0)
            else:
                no_of_submission = no_of_submission - 1
                t_penalty = t_penalty + s_object.time_penalty

                status_code = int(s_object.evaluation_result)

                if get_recent_contest().end_time < timezone.now():
                    sub_status.append(status_code)
                else:
                    sub_status.append(2)
    
                sub_penalty.append(s_object.penalty)
                tot_points = tot_points + s_object.points

        if no_of_submission == 0 :
            continue

        res['username'] = user.username
        res['time_penalty'] = t_penalty
        res['number_of_submission'] = no_of_submission
        res['submission_status'] = sub_status
        res['submission_penalty'] = sub_penalty
        res['total_points'] = tot_points

        score_d.append(res)

    if get_recent_contest().end_time < timezone.now():
        score_d.sort(key=lambda k : k['total_points'],reverse = True)
    else :
        score_d.sort(key=lambda k : (k['number_of_submission'],k['time_penalty']))

    if get_recent_contest().end_time > timezone.now():
        res['total_points'] = '?'

    return render(request, 'scoreboard.html', {'scores': score_d, 'problems': problems})

def submit_source(request, problem_id):

    if request.method == "POST":

        form = SourceSubmissionForm(request.POST, request.FILES)

        if form.is_valid() and get_recent_contest().phase == 1 or get_recent_contest().end_time >= timezone.now():

            source_file = request.FILES['source_file']
            input_file = request.FILES['input_file']

            problem = get_problem_object(problem_id)
            problem.source_file = source_file
            problem.input_file = input_file

            problem.save()

            submission = Submission(user=request.user, problem=problem)

            return HttpResponse("<h1>Source submitted successfully :)</h1>")

        else:
            return HttpResponse("<h1>Invalid submission :(</h1>")

    form = SourceSubmissionForm()

    if get_recent_contest().phase == 2 or get_recent_contest().end_time <= timezone.now():
        return HttpResponse("<h1> o.O What are you doing here? (Submission deadline passed) </h1>")

    return render(request, "submit_source.html", {"form": form})


def submit(request, problem_id):

    if request.method == "POST":

        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid() and validate_submission(request.user, get_problem_object(problem_id)):

            source = request.FILES['source_file']
            output = request.FILES['output_file']

            submission = get_sumbission_object(request.user, get_problem_object(problem_id))

            submission.submit_time = datetime.now()
            submission.source_file = source
            submission.output_file = output

            submission.time_penalty = (timezone.now() - get_recent_contest().start_time).total_seconds() // 60

            submission.save()

            return HttpResponse("<h2>Submission Successful :)</h2>")

        else:
            return HttpResponse("<h2>Invalid Submission.</h2>")

    else:
        form = SubmissionForm()

    submission = get_sumbission_object(request.user, get_problem_object(problem_id))

    submission_triggered = 0
    counter = 0

    if submission is not None:
        if submission.deadline < timezone.now():
            return HttpResponse("<h2>Deadline passed :( </h2>")
        else:
            submission_triggered = 1
            counter = (submission.deadline - timezone.now()).total_seconds() // 1

    if get_recent_contest().end_time <= timezone.now():
        return HttpResponse("Contest ended :( ")

    return render(request, "submit.html", {'form': form, 'problem': get_problem_object(problem_id), 'triggered': submission_triggered, 'counter': counter})


def register(request):

    logout(request)

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():
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

                    return redirect("/")

    else:
        form = RegistrationForm()

    return render(request, "register.html", {'form': form})


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
