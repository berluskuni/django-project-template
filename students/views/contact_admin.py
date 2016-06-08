# coding=utf-8
from django.views.generic.edit import FormView

__author__ = 'berluskuni'
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from studentsdb.settings import ADMIN_EMAIL
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

"""
def contact_admin(request):
    # check inf form was posted
    if request.method == 'POST':
        # create form instance and populate it with data from the request
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                message = u'Під час відправки листа виниклаьнепередбачувана помилка. ' \
                          u'Спробуйте скористатися даною формаю пізніше'
            else:
                message = u'Повідомлення успішно надіслане!'
            # redirect to same contact page with success message
            return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('contact-admin'), message))
    else:
        form = ContactForm()
    return render(request, 'contact_admin/form.html', {'form': form})
"""


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)
        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact-admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-4'

        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))
    from_email = forms.EmailField(label=u'Ваша Емейл Адреса')
    subject = forms.CharField(label=u'Загаловок листа', max_length=128)
    message = forms.CharField(label=u'Текс повідомлення', max_length=2560, widget=forms.Textarea)


class ContactView(FormView):
    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = '/email-sent/'

    def form_valid(self, form):
        """
        This method is called for valid data
        """
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']

        send_mail(subject, message, from_email, [ADMIN_EMAIL])
        return super(ContactView, self).form_valid(form)

    @method_decorator(permission_required('auth.add_user'))
    def dispatch(self, *args, **kwargs):
        return super(ContactView, self).dispatch(*args, **kwargs)




