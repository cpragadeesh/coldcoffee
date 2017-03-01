from django import forms

from .models import Submission, Problem, User

class SubmissionForm(forms.ModelForm):

	class Meta:
		model = Submission
		fields = ['source_file', 'output_file']

class SourceSubmissionForm(forms.ModelForm):

	class Meta:
		model = Problem
		fields = ['source_file', 'input_file']

class RegistrationForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class LoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ['username', 'password']