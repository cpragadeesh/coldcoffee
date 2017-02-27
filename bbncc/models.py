from __future__ import unicode_literals

from django.db import models
from md5 import md5
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from problem_id_hashes import id_hashes
from django.core.exceptions import ValidationError

class Problem(models.Model):
	
	title = models.CharField(max_length=100)
	problem_content = models.TextField()
	nick = models.CharField(max_length=100, blank=True)
	problem_id = models.CharField(max_length=100, blank=True)
	source_filename = models.CharField(max_length=100, blank=True)
	input_file_name = models.CharField(max_length=100, blank=True)
	source_author = models.ForeignKey(User, on_delete=models.CASCADE)
	validator = models.CharField(max_length = 100)
	contest = models.ForeignKey("Contest", on_delete=models.SET_NULL, null=True)

	def save(self):

		#Fills problem_id, nick fields

		super(Problem, self).save()
		
		self.problem_id = md5(str(self.id)).hexdigest()
		self.nick = self.title;
		self.nick = self.nick.replace(" ", "_")

		if len(self.source_filename) < 5:
			self.source_filename = self.nick + "_source.cpp"

		if len(self.input_file_name) < 5:
			self.input_file_name = self.nick + "_input.txt"

		super(Problem, self).save()

	def __str__(self):
		return self.title


class Submission(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	problem = models.ForeignKey("Problem", on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now_add=True)
	submit_time = models.DateTimeField(blank=True, null=True)
	deadline = models.DateTimeField()
	output_filename = models.CharField(max_length = 100)
	source_filename = models.CharField(max_length = 100)
	evaluation_result = models.CharField(max_length = 100, default="0")

	#evaluation_result: 0 for unevaluated submission, 1 for correct answer, -1 for wrong answer

	def __init__(self, *args, **kwargs):
		
		super(Submission, self).__init__(*args, **kwargs)

		if self.pk is None: 
			self.deadline = datetime.now() + timedelta(minutes=8)


	def __str__(self):
		return "User: " + self.user.username + " | problem: " + str(id_hashes[self.problem.problem_id])


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
