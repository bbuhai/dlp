from django.conf.urls import patterns, url

from survey import views

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^page/(?P<page>\d+)$', views.ListView.as_view(), name='list'),
    url(r'^page/(?P<page>\d+)/limit/(?P<limit>\d+)$', views.ListView.as_view(), name='list'),
    url(r'^(?P<survey_id>\d+)$', views.SurveyView.as_view(), name='survey'),
    url(r'^(?P<survey_id>\d+)/page/(?P<page>\d+)$', views.SurveyView.as_view(), name='survey'),
    url(r'^(?P<survey_id>\d+)/result$', views.ResultView.as_view(), name='result'),
    url(r'^(?P<survey_id>\d+)/closest_path$', views.ClosestPath.as_view(), name='closest')
)