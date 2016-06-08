# coding=utf-8
__author__ = 'berluskuni'
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Group
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from ..util import get_current_group


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'post'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-4'

        # add buttons
        self.helper.layout[-1] = FormActions(Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
                                             Submit('cancel_button', u'Скасувати', css_class='btn btn-link'), )


def groups_list(request):
    current_group = get_current_group(request)
    if current_group:
        groups = Group.objects.filter(title=current_group.title)
    else:
        groups = Group.objects.all()
        # try to order groups list
        order_by = request.GET.get('order_by', '')
        if order_by in ('title', 'leader'):
            groups = groups.order_by(order_by)
            if request.GET.get('reverse', '') == '1':
                groups = groups.reverse()

    # paginate students
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer? deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out range (e.g. 9999), deliver
        # last page of results
        groups = paginator.page(paginator.num_pages)
    return render(request, 'groups/groups_list.html', {'groups': groups, 'current_group': current_group})


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'groups/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Група успешно збереженно' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування групи відмінено' % reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDelete(DeleteView):
    model = Group
    template_name = 'groups/groups_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Групу успішно видалено!' % reverse('home')


def groups_add(request):
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:

            errors = {}
            # validate groups data will go here
            data = {'notes': request.POST.get('notes')}

            # validate user input
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва є обов'язковим"
            else:
                data['title'] = title

            if not errors:
                # create student object
                group = Group(**data)
                # save it to database
                group.save()
                # redirect user to student list
                return HttpResponseRedirect(u'%s?status_message=Групу %s  успішно додано!' % (reverse('groups'),
                                            data['title']))
            else:
                # render form with errors and previous user input
                return render(request, 'groups/groups_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                  'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'%s?status_message=Додавання Групи скасовано' % reverse('groups'))
    else:
        # initial form render
        return render(request, 'groups/groups_add.html', {'groups': Group.objects.all().order_by('title')})

