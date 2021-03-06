from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name='activitysim',
    version='0.1dev',
    description='Travel modeling',
    author='Autodesk',
    author_email='udst@autodesk.com',
    license='AGPL',
    url='https://github.com/udst/activitysim',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
    packages=find_packages(exclude=['*.tests']),
    install_requires=[
        'numpy >= 1.8.0',
        'openmatrix >= 0.2.2',
        'orca >= 1.1',
        'pandas >= 0.13.1',
        'pyyaml >= 3.0',
        'tables >= 3.1.0',
        'toolz >= 0.7',
        'zbox >= 1.2'
    ]
)
