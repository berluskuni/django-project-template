# coding=utf-8
__author__ = 'berluskuni'
from django.apps import AppConfig


class StudentAppConfig(AppConfig):
    name = 'students'
    verbose_name = u'База Студентів'

    def ready(self):
        from students import signals
