from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import re
import sys


VERSIONFILE="decol/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='decol',
    version=verstr,
    author='Chris T. Berthiaume',
    author_email='chrisbee@uw.edu',
    license='LICENSE.txt',
    description='A tool to drop or keep columns from a CSV file.',
    long_description=open('README.rst', 'r').read(),
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Click'
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    entry_points={
        'console_scripts': [
            'decol = decol.cli:main'
        ]
    }
)
