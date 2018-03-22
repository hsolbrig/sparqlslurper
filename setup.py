import sys
from setuptools import setup


if sys.version_info < (3, 6):
    print("This module requires python 3.6 or later")
    sys.exit(1)

setup(
    name='sparql_slurper',
    version='0.1.1',
    packages=['sparql_slurper'],
    url="http://github.com/hsolbrig/sparql_slurper",
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig@solbrig-informatics.com',
    description='SPARQL Slurper for rdflib',
    install_requires=['rdflib', 'SPARQLWrapper'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6']
)
