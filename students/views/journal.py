# coding=utf-8
__author__ = 'berluskuni'
from datetime import datetime, date
from calendar import monthrange, weekday, day_abbr
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from ..models.students import Student
from django.views.generic.base import TemplateView
from ..util import paginate, get_current_group
from ..models.monthjournal import MonthJournal
from django.http import JsonResponse


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # перевіряємо чи передали нам місяц в параметрі,
        # якщо ні вичисляемо поточний;
        # поки що ми віддаємо лише поточний
        # check if se need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # обчислюемо поточний рік, попередній і наступний місяці
        # calculate current, previous and next month details
        # we need this for month navigation element in template
        next_month = month + relativedelta(month=1)
        prev_month = month - relativedelta(month=1)
        # а поки прибиваємо их статично

        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year

        # також поточний місяц;
        # змінну cur_month ми використоватимемо пізніше
        # в пагінації; а month_verbose в навигації помисячній
        context['cur_month'] = month.strftime('%Y-%m-%d')
        context['month_verbose'] = month.strftime('%B')

        # тут будемо обчислювати список днів у місяці а поки заб'ємо статично:
        # prepare variable for template to  generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{
            'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]
        # витягуємо усіх студентів посортованних по
        # get all students from database? or just one if we need to display journal for one student
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Student.objects.filter(students_group=current_group)
        elif kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        else:
            queryset = Student.objects.all().order_by('last_name')

        # get all students from database>? or justn one if current_group

        # це адреса для посту AJAX запиту, як бачите ми робимо його на цю ж в'юшку журналу
        # буде ш показувати журнал ы обслуговувати запити типу пост на оновленя журналу
        update_url = reverse('journal')

        # пробыгаэмось по усіх студентах і збіраємо необхідні дані
        students = []

        for student in queryset:
            # TODO: витягуємо журнал для студента і вибранного місця
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # набиваємо дні для студента
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })
            # набиваємо усі решту даних студента
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'update_url': update_url,
                'id': student.id,
            })
            #  застосовуємо пагінацію до списку студентів
        context = paginate(students, 5, self.request, context, var_name='students')
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student? dates and presence data
        current_data = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_data.year, current_data.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])
        # get or create journal object for given student and month
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_data.day, present)
        journal.save()

        return JsonResponse({'status': 'success'})




