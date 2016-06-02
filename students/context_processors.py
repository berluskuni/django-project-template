__author__ = 'berluskuni'
from .util import get_groups


def group_processor(request):
    return {'GROUPS': get_groups(request)}
