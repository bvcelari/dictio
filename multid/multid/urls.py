from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'multid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<lang_id>\w+)/index/$', 'multid.views.index', name='index'),
    url(r'^(?P<lang_id>\w+)/about/$', 'multid.views.about', name='about'),
    url(r'^(?P<lang_id>\w+)/contact/$', 'multid.views.contact', name='contact'),

    ##url(r'^$', 'multid.views.concepts', name='concepts'),
    url(r'^en/search/$', 'multid.views.searchen', name='concepts'),
    url(r'^ge/search/$', 'multid.views.searchge', name='concepts'),
    url(r'^fr/search/$', 'multid.views.searchfr', name='concepts'),
    url(r'^es/search/$', 'multid.views.searches', name='concepts'),
    url(r'^(?P<lang_id>\w+)/(?P<concept_id>\d+)/$', 'multid.views.definition', name='definition'),
    url(r'^import_concepts/$', 'multid.views.import_concepts', name='concepts'),

    url(r'^admin/', include(admin.site.urls)),

url(r'^login/$', views.login, name='login'),
url(r'^logout/$', views.logout, name='logout'),

)
