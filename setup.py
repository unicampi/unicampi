# This is the main testing file which can be run as `python setup.py test`

from setuptools import setup, find_packages

REQUIREMENTS = [
    'bs4',
    'cornice',
    'lxml',
    'pyramid',
    'requests'
]

REQUIREMENTS_DEV = [
    'pytest',
    'webtest',
    'coverage',
    'coveralls',
    'flake8',
    'pep8',
    'tox',
]

setup(
    name='unicampi',
    license='GNU Public License (3.0)',
    version='0.1',
    description="API to fetch Unicamp's public data.",
    long_description=open('README.rst').read(),
    author='Gabriela Surita',
    author_email='gabsurita@gmail.com',

    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_DEV,

    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
)
