# coding=utf-8
__author__ = 'berluskuni'
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestStudentUpdateForm(TestCase):

    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()

        # remember url to edit form
        self.url = reverse('students_edit', kwargs={'pk': 1})

    def test_form(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(self.url)

        # check response status
        self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn(u'Редагувати Студента', unicode(response.content, encoding='utf-8'))
        self.assertIn(u'Білет', unicode(response.content, encoding='utf-8'))
        self.assertIn(u'Прізвище', unicode(response.content, encoding='utf-8'))
        self.assertIn('name="add_button"', response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)
        self.assertIn('podoba.jpg', response.content)