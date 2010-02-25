#!/usr/bin/env python

from distutils.core import setup

setup(name='objtrack',
      version='1.0',
      description='Django Object View Tracking',
      author='David Cramer',
      author_email='dcramer@gmail.com',
      url='http://github.com/dcramer/objtrack/',
      packages=['objtrack', 'objtrack.templatetags'],
     )
