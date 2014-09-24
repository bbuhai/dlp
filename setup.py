import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dependencies = (
    'Django==1.6',
    'argparse==1.2.1',
    'sqlparse==0.1.11',
    'wsgiref==0.1.2',
    'django-debug-toolbar==1.2.1',
    'factory-boy==2.4.1'
)

setup(
    name='dj_start',
    version='0.1dev',
    license='BSD',
    author='Bogdan Buhai',
    description='A simple django project with some small apps.',
    long_description=README,
    packages=find_packages(),
    install_requires=dependencies,
    include_package_data=True,  # what does this do?
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers'
    ],
    test_require=[
        'coverage==3.7',
        'django-coverage==1.2'
    ]
)