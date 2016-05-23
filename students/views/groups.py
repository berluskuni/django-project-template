# coding=utf-8
__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponse


def groups_list(request):
    groups = (
        {
            'id': 1,
            'name': u'МтМ-21',
            'steward': u'Ганжела Сергій',
        },
        {
            'id': 2,
            'name': u'МтМ-22',
            'steward': u'Ганжела Андрйій',
        },
        {
            'id': 3,
            'name': u'МтМ-23',
            'steward': u'Ганжела Пётр',
        },
        {
            'id': 4,
            'name': u'МтМ-24',
            'steward': u'Шевчук Максим',
        },

    )
    return render(request, 'groups_list.html', {'groups': groups})


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')
