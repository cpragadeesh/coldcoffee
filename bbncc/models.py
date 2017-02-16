from __future__ import unicode_literals

from django.db import models
from md5 import md5
from django.contrib.auth.models import User

class Problem(models.Model):
	
	title = models.CharField(max_length=100)
	problem_content = models.TextField()
	nick = models.CharField(max_length=100, blank=True)
	problem_id = models.CharField(max_length=100, blank=True)
	source_filename = models.CharField(max_length=100, blank=True)
	input_file_name = models.CharField(max_length=100, blank=True)
	source_author = models.CharField(max_length=100, default = "server")

	def save(self):

		# This is a workaround to auto generate a problem_id hash
		# everytime a new problem is added

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

class SourceURL(models.Model):

	url = models.CharField(max_length=500)

	def __str__(self):
		return self.url

class InputURL(models.Model):

	url = models.CharField(max_length=500)

	def __str__(self):
		return self.url
