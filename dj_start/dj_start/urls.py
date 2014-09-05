from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'dj_start.views.home', name='home'),
    url(r'^contact/$', include('contact.urls'), name="contact"),
    url(r'^test/', include('personalitytests.urls', namespace='pers')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^survey/', include('survey.urls', namespace='survey'))
)
