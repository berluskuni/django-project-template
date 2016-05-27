# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from .settings import MEDIA_ROOT, DEBUG
from students.views.contact_admin import ContactView
from students.views.students import StudentUpdateView, StudentDeleteView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'studentsdb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^contact-admin/$', ContactView.as_view(), name='contact-admin'),
                       # url(r'^contact/', include('contact_form.urls')),
                       # Students urls
                       url(r'^$', 'students.views.students.students_list', name='home'),
                       url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),
                       url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
                           name='students_edit'),
                       url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
                           name='students_delete'),

                       # Groups urls
                       url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
                       url(r'^groups/add/$', 'students.views.groups.groups_add', name='groups_add'),
                       url(r'^groups/(?P<gid>\d+)/edit/$', 'students.views.groups.groups_edit', name='groups_edit'),
                       url(r'^groups/(?P<gid>\d+)/delete/$', 'students.views.groups.groups_delete',
                           name='groups_delete'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns("",
                            url(r'^media/(?P<patch>.*)$', 'django.views.static.serve',
                                {'document': MEDIA_ROOT}))
