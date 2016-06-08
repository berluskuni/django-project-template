# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView, TemplateView
from .settings import MEDIA_ROOT, DEBUG
from students.views.contact_admin import ContactView
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.groups import GroupDelete, GroupUpdateView
from students.views.journal import JournalView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'studentsdb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^users/profile/$',
                           login_required(TemplateView.as_view(template_name='registration/profile.html')),
                           name='profile'),
                       url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
                       url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
                           name='registration_complete'),
                       url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
                       url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
                       url(r'^contact-admin/$', ContactView.as_view(), name='contact-admin'),
                       # url(r'^contact/', include('contact_form.urls')),
                       # Students urls
                       url(r'^$', 'students.views.students.students_list', name='home'),
                       url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),
                       url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
                           name='students_edit'),
                       url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
                           name='students_delete'),
                       # url(r'^journal/$', JournalView.as_view(), name='journal'),
                       url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

                       # Groups urls
                       url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
                       url(r'^groups/add/$', 'students.views.groups.groups_add', name='groups_add'),
                       url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
                       url(r'^groups/(?P<pk>\d+)/delete/$', GroupDelete.as_view(),
                           name='groups_delete'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns("",
                            url(r'^media/(?P<patch>.*)$', 'django.views.static.serve',
                                {'document': MEDIA_ROOT}))
