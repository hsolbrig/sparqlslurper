#!/usr/bin/env python
import sys

from setuptools import setup

if sys.version_info < (3, 6):
    raise Exception("Python 3.6 or higher is required. Your version is %s." % sys.version)

NAME = 'sparqlslurper'
setup(
    name=NAME,
    setup_requires=['pbr'],
    pbr=True,
)
