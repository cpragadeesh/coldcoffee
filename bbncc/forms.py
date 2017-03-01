from django import forms

from .models import Submission, Problem

class SubmissionForm(forms.ModelForm):

	class Meta:
		model = Submission
		fields = ['source_file', 'output_file']

class SourceSubmissionForm(forms.ModelForm):

	class Meta:
		model = Problem
		fields = ['source_file', 'input_file']