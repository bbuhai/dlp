from django.conf.urls import patterns, url
from accounts import views


urlpatterns = patterns('',
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^create/', views.CreateView.as_view(), name='create')
)

