# coding=utf-8
from django.views.generic import UpdateView, DeleteView
from studentsdb import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from crispy_forms.bootstrap import FormActions
from ..models import Student, Group
from datetime import datetime
from ..util import get_current_group


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-5'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'middle_name',
                'last_name',
                'birthday',
                'photo',
                'ticket',
                'students_group'
            ),
            FormActions(
                Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
                Submit('cancel_button', u'Скасувати', css_class='btn btn-link'),
            )
        )


def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(students_group=current_group)
    else:
        students = Student.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer? deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out range (e.g. 9999), deliver
        # last page of results
        students = paginator.page(paginator.num_pages)
    return render(request, 'students/students_list.html', {'students': students})


@login_required
def students_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введить коректний формат дати (напр. 1984-12-15)"
                else:
                    data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            student_group = request.POST.get('student_group', '').strip()

            if not student_group:
                errors['student_group'] = u"Номер групи є обов'язковим"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Номер групи є обов'язковим"
                else:
                    data['students_group'] = groups[0]
            photo = request.FILES.get('photo')
            if photo:
                if photo._size > 2 * 1024 * 1024:
                    errors['photo'] = u"Размер файла слишком велик ( максимум 2mb )"
                elif photo.content_type not in settings.VALID_IMAGE_FORMATS:
                    errors['photo'] = u"Файл не является изображением"
                else:
                    data['photo'] = photo
            if not errors:
                # create student object
                student = Student(**data)
                # save it to database
                student.save()
                # redirect user to student list
                return HttpResponseRedirect(u'%s?status_message=Студента %s %s успишно додано!' % (reverse('home'),
                                            data['first_name'],  data['last_name']))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                      'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано' % reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Студента успешно збереженно' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено' % reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)