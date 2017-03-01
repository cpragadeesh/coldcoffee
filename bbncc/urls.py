from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.contest_switch),
    url(r'^contest1/$', views.contest1),
    url(r'^contest2/$', views.contest2),
    url(r'^login/$', views.loginView),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logoutView),
    url(r'^problem/(?P<problem_id>[0-9a-zA-Z]+$)', views.problem),
    url(r'^source-download/(?P<problem_id>[0-9a-zA-Z]+$)', views.source_download),
    url(r'^input-download/(?P<problem_id>[0-9a-zA-Z]+$)', views.input_download),
    url(r'^cachereset/$', views.cachereset),
    url(r'^console/$', views.console),
    url(r'^scoreboard/$', views.scoreboard),
    url(r'^submit/(?P<problem_id>[0-9a-zA-Z]+$)', views.submit),
    url(r'^submit_source/(?P<problem_id>[0-9a-zA-Z]+$)', views.submit_source),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)