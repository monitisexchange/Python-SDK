#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'Monitis-SDK',
    version = '1.0.1',
    description = 'Monitis API SDK',
    author = 'Jeremiah Shirk',
    author_email = 'jshirk@gmail.com',
    url = 'https://github.com/monitisexchange/Python-SDK',
    requires = [
        'parsedatetime',
        'boto'
    ],
    packages = [
        'monitis',
        'monitis.monitors',
        'monitis.tools',
        'monitis.tools.awsmon'
    ],
    scripts = [
        'monitis/tools/monitis_cloudwatch.py'
    ],
    keywords = [
        '',
    ],
    classifiers = [
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers'
    ],
    long_description = """\
    Monitis API SDK
    ---------------
    
    The Monitis API SDK provides a simple Python interface to the Monitis 
    RESTful API.  More information on the API is available at 
    http://monitis.com/api/api.html.
    """
)
