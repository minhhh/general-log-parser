#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, codecs
from distutils.core import setup, Command

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import general_log_parser

with codecs.open('README.rst') as readme_file:
    readme = readme_file.read()

with codecs.open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "click==4.0",
    "fn==0.4.3",
    "six==1.9.0",
    "wsgiref==0.1.2"
]

test_requirements = [
    "pytest"
]

setup(
    name=general_log_parser.__program__,
    version=general_log_parser.__version__,
    description=general_log_parser.__description__,
    long_description=readme + '\n\n' + history,
    author=general_log_parser.__author__,
    author_email=general_log_parser.__email__,
    url='https://github.com/minhhh/general-log-parser',
    packages=[
        'general_log_parser',
    ],
    package_dir={'general_log_parser':
                 'general_log_parser'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='general-log-parser',
    cmdclass = {'test': PyTest},
    scripts=['general_log_parser/logparser'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
