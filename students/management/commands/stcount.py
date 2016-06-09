__author__ = 'berluskuni'
from django.core.management.base import BaseCommand
from students.models import Student, Group
from django.contrib.auth.models import User

"""
class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = "Print to console number odf student related object in a database"

    def handle(self, *args, **options):
        if 'student' in args:
            self.stdout.write("Number of students in database: %d" % Student.objects.count())
        elif 'group' in args:
            self.stdout.write("Number of groups in database: %d" % Group.objects.count())
        elif 'user' in args:
            self.stdout.write("number of users in database: %d" % User.objects.count())
"""


class Command(BaseCommand):
    args = '<model_name model_name ...>'
    help = "Print to console number odf student related object in a database"

    models = (('student', Student), ('group', Group), ('user', User))

    def handle(self, *args, **options):
        for name, model in self.models:
            if name in args:
                self.stdout.write("Number of %ss in database: %d" % (name, model.objects.count()))