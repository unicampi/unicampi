# This is the main testing file which can be run as `python setup.py test`

import sys
from setuptools import setup, find_packages

REQUIREMENTS = [

]

TEST_REQUIREMENTS = [
    'tox',
    'pytest',
]


setup(
    name='unicampi',
    license='GNU Public License v3.0',
    version='0.1',
    description='API to fetch Unicamp public data.',
    long_description=open('README.rst').read(),
    author='Gabriela Surita',
    author_email='gabsurita@gmail.com',
    
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    )

