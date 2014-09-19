from django.conf.urls import patterns, url

from personalitytests import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='tests_list'),
    url(r'^(?P<test_id>\d+)/$', views.test, name='test'),
    url(r'^(?P<test_id>\d+)/result/(?P<score>\d+)$', views.result, name='result'),
)