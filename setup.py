#!/usr/bin/env python

from setuptools import setup

setup(name='objtrack',
      version='.'.join(map(str, __import__('objtrack', globals(), locals(), []).__version__)),
      description='Django Object View Tracking',
      author='David Cramer',
      author_email='dcramer@gmail.com',
      url='http://github.com/dcramer/objtrack/',
      packages=['objtrack', 'objtrack.templatetags'],
     )
