# coding=utf-8
__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponse
from ..models import Student


def students_list(request):
    students = Student.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == 1:
            students = students.reversw()
    return render(request, 'students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Students %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Students %s</h1>' % sid)
