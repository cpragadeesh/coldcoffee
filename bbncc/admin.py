from django.contrib import admin

from .models import Problem, SourceURL, InputURL, Submission

admin.site.register(Problem)
admin.site.register(SourceURL)
admin.site.register(InputURL)
admin.site.register(Submission)