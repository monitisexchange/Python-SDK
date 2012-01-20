#!/usr/bin/env python

from distutils.core import setup

setup(name='Monitis-SDK',
      version='1.0',
      description='Monitis API SDK',
      author='Jeremiah Shirk',
      author_email='jshirk@gmail.com',
      packages=['monitis',
                'monitis.monitors',
               ],
      )
