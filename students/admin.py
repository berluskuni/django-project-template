# coding=utf-8
from django.contrib import admin

from .models import Student, Group, MonthJournal
from django.core.urlresolvers import reverse
# Register your models here.
from django.forms import ModelForm, ValidationError


class GroupFormAdmin(ModelForm):

    def clean_leader(self):

        students = Student.objects.filter(students_group=self.instance)
        if len(students) > 0 and self.cleaned_data['leader'] != students[0]:
            raise ValidationError(u'Студент не є членом єтой групи', code='invalid')
        return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):

    list_display = ['title', 'leader']
    list_display_links = ['title', 'leader']
    ordering = ['title']
    list_filter = ['title']

    form = GroupFormAdmin

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})


class StudentFormAdmin(ModelForm):

    def clean_students_group(self):
        """
        Check i student is leader in any group
        if yes, then ensure it's the same is selected group

        """
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['students_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
        return self.cleaned_data['students_group']


class StudentAdmin(admin.ModelAdmin):

    list_display = ['last_name', 'first_name', 'ticket', 'students_group']
    list_display_links = ['last_name', 'first_name']
    ordering = ['last_name']
    list_filter = ['students_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']

    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)


