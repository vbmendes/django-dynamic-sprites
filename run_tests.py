#!/usr/bin/env python

import coverage
import imp
from os.path import dirname, abspath, join
from optparse import OptionParser
from subprocess import Popen, PIPE
import sys

from django.conf import settings
from django.utils.importlib import import_module

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',

            'dynamic_sprites',

            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
        MEDIA_ROOT=join(dirname(abspath(__file__)), 'tests', 'media'),
        EXCLUDE_FILES_FROM_COVERAGE=['dynamic_sprites/listeners.py', 'dynamic_sprites/model_images.py']
    )

from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    coverage_ = start_coverage()
    test_runner = DjangoTestSuiteRunner(verbosity=kwargs.get('verbosity', 1), interactive=kwargs.get('interactive', False), failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    end_coverage(coverage_)
    sys.exit(failures)

def start_coverage():
    files_to_cover = get_files_to_cover()
    if not files_to_cover:
        coverage_ = None
        print "Not running coverage. No *.py files to test."
    else:
        coverage_ = coverage.coverage(include=files_to_cover, branch=True)
        coverage_.start()
        import_files(files_to_cover)
    return coverage_


def get_files_to_cover():
    return reduce(lambda x, y: x + y,
        (get_files_to_cover_from_app(app) for app
        in ['dynamic_sprites', 'scripts'])
    )


def get_files_to_cover_from_app(app):
    from django import conf
    app_path = import_module(app).__path__[0]
    py_files = (Popen(['find', app_path, '-name', '*.py'], stdout=PIPE)
                .communicate()[0].split('\n'))
    return [file_ for file_ in py_files if file_ and not '/tests/' in file_ and
                                           not any(
                                               exclude_file in file_
                                               for exclude_file in conf.settings.EXCLUDE_FILES_FROM_COVERAGE)]


def import_files(files):
    for file_ in files:
        imp.load_source('foo_module', file_)


def end_coverage(coverage_):
    if coverage_:
        coverage_.stop()
        coverage_.report()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
