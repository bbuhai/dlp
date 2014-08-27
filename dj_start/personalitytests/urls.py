from django.conf.urls import patterns, url

from personalitytests import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^test/(?P<test_id>\d+)/$', views.test, name='test'),
    url(r'^test/(?P<test_id>\d+)/result$', views.result, name='result'),
    url(r'^test/(?P<test_id>\d+)/score', views.compute_score, name='score')
)