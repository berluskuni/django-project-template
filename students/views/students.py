# coding=utf-8
__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponse


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
