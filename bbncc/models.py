from __future__ import unicode_literals

from django.db import models

class Problem(models.Model):
	title = models.CharField(max_length=100)
	problem_content = models.TextField()

	def __str__(self):
		return self.title