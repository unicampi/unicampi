# This is the main testing file which can be run as `python setup.py test`

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    # Run tox as a test runner for all tests
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        cov.stop()
        sys.exit(errcode)


setup(
    name='example-project',
    version='1.0',
    description='Insert description here',
    author='Chris Mark',
    platforms='any',
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    author_email='chris@robinpowered.com',

    # install_requires=['pyserial==2.7',],
    # packages=[''],
    # tests_require=['pytest'],
    # long_description=long_description,
    # packages=[''],
    # include_package_data=True,
    # test_suite='',
    )

