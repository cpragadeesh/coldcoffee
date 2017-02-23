from django.contrib import admin

from .models import Problem, SourceURL, InputURL, Submission, Contest

admin.site.register(Problem)
admin.site.register(SourceURL)
admin.site.register(InputURL)
admin.site.register(Submission)
admin.site.register(Contest)