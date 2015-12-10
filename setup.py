"""Setup script of django-livereload-server"""
import os.path
from setuptools import setup
from setuptools import find_packages

import livereload

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-livereload-server',
    version=livereload.__version__,
    packages=find_packages(),
    include_package_data=True,
    license=livereload.__license__,
    description='LiveReload functionality integrated with your Django development environment',
    long_description=README,
    url=livereload.__url__,
    author=livereload.__author__,
    author_email=livereload.__email__,
    keywords='django, server, runserver, livereload',
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'django>=1.8',
        'beautifulsoup4>=4.3.2',
        'tornado',
        'six',
    ],
)
