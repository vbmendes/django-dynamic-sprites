import os

from django.conf import settings


class MockedImage(object):
    pass


def get_absolute_path(path):
    return os.path.join(settings.MEDIA_ROOT, path)
