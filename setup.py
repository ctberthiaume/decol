from setuptools import setup

setup(
    name='decol',
    version='1.0.0',
    author='Chris T. Berthiaume',
    author_email='chrisbee@uw.edu',
    license='LICENSE.txt',
    description='A tool to remove columns from a CSV file.',
    long_description=open('README.rst', 'r').read(),
    py_modules=['decol'],
    include_package_data=True,
    install_requires=[
        'click'
    ],
    entry_points='''
        [console_scripts]
        decol=decol:cli
    ''',
)
