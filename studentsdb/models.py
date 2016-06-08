# coding=utf-8
__author__ = 'berluskuni'
from django.db import models
from django.contrib.auth.models import User


class StProfile(models.Model):
    """
    To keep extra user data
    """
    # user mapping
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = u'Профиль пользователя'

    mobile_phone = models.CharField(max_length=15, blank=True, verbose_name=u'Мобильный телефон', default='')

    def __unicode__(self):
        return self.user.username
