from setuptools import setup, find_packages
from tuvok import __version__, __license__

"""Packaging settings."""

DEPENDENCIES = []

setup(
    name='tuvok',
    version=__version__,
    description='Terraform code validation',
    url='https://github.com/rackerlabs/tuvok/',
    author='Rackers',
    author_email='',
    license=__license__,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    packages=find_packages(exclude=['venv']),
    package_data={'tuvok': ['.tuvok.json']},
    install_requires=DEPENDENCIES,
    entry_points={
        'console_scripts': [
            'tuvok=tuvok.cli:main',
        ],
    },
)
