from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.contest1),
    url(r'^login/$', views.loginView),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logoutView),
    url(r'^problem/(?P<problem_id>[0-9]+$)', views.problem)
]