from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.contest1),
    url(r'^contest/$', views.contest1),
    url(r'^login/$', views.loginView),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logoutView),
    url(r'^problem/(?P<problem_id>[0-9a-zA-Z]+$)', views.problem),
    url(r'^source-download/(?P<problem_id>[0-9a-zA-Z]+$)', views.source_download),
    url(r'^input-download/(?P<problem_id>[0-9a-zA-Z]+$)', views.input_download),
    url(r'^cachereset/$', views.cachereset),
]