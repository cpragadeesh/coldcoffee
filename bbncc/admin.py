from django.contrib import admin

from .models import Problem, SourceURL, InputURL

admin.site.register(Problem)
admin.site.register(SourceURL)
admin.site.register(InputURL)