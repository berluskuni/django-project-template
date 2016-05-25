# coding=utf-8
__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponse
from ..models import Group


def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups_list.html', {'groups': groups})


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')
