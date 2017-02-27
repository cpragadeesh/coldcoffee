from __future__ import unicode_literals

from django.db import models
from md5 import md5
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from problem_id_hashes import id_hashes
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

class Problem(models.Model):
	
	title = models.CharField(max_length=100)
	problem_content = models.TextField()
	nick = models.CharField(max_length=100, blank=True)
	problem_id = models.CharField(max_length=100, blank=True)
	source_file = models.FileField(upload_to=settings.ORIGINAL_SOURCE_URL)
	input_file = models.FileField(upload_to=settings.ORIGINAL_INPUT_URL)
	source_author = models.ForeignKey(User, on_delete=models.CASCADE)
	validator = models.FileField(upload_to=settings.VALIDATOR_URL)
	contest = models.ForeignKey("Contest", on_delete=models.SET_NULL, null=True)

	def save(self):

		#Fills problem_id, nick fields
		
		self.problem_id = md5(str(self.id)).hexdigest()
		self.nick = self.title;
		self.nick = self.nick.replace(" ", "_")

		super(Problem, self).save()

	def __str__(self):
		return self.title


class Submission(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	problem = models.ForeignKey("Problem", on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now_add=True)
	submit_time = models.DateTimeField(blank=True, null=True)
	deadline = models.DateTimeField()
	output_file = models.FileField(upload_to=settings.SUBMISSION_OUTPUT_URL)
	source_file = models.FileField(upload_to=settings.SUBMISSION_SOURCE_URL)
	evaluation_result = models.CharField(max_length = 100, default="0")

	#evaluation_result: 0 for unevaluated submission, 1 for correct answer, -1 for wrong answer

	def __init__(self, *args, **kwargs):
		
		super(Submission, self).__init__(*args, **kwargs)

		if self.pk is None: 
			self.deadline = timezone.now() + timedelta(minutes=8)


	def __str__(self):
		return "User: " + self.user.username + " | problem: " + self.problem.nick


class Contest(models.Model):

	name = models.CharField(max_length = 100)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	def clean(self):

		if self.end_time < self.start_time:
			raise ValidationError("End time cannot be less than Start time.")

	def __str__(self):

		return self.name

class SourceURL(models.Model):

	url = models.CharField(max_length=500)

	def __str__(self):
		return self.url


class InputURL(models.Model):

	url = models.CharField(max_length=500)

	def __str__(self):
		return self.url
