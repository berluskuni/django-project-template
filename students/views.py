#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Views fo Students


def students_list(request):
    students = (
        {
            'id': 1,
            'first_name': u'Сергій',
            'last_name': u'Ганжела',
            'ticket': 235,
            'image': 'img/Serg.jpg',
        },
        {
            'id': 2,
            'first_name': u'Андрій',
            'last_name': u'Ганжела',
            'ticket': 2123,
            'image': 'img/SERG2.gif'
        }
    )
    return render(request, 'students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Students %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Students %s</h1>' % sid)


# Views for Groups

def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


