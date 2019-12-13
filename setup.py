import ast
import re


from setuptools import setup, find_packages

"""Packaging settings"""
DEPENDENCIES = ['python-hcl2']


def package_metadata():
    """Read __version__.py for package metadata without importing package"""

    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    _license_re = re.compile(r'__license__\s+=\s+(.*)')

    with open('tuvok/__version__.py', 'rb') as f:
        metadata_content = f.read()
        version = str(ast.literal_eval(_version_re.search(metadata_content.decode('utf-8')).group(1)))
        licencia = str(ast.literal_eval(_license_re.search(metadata_content.decode('utf-8')).group(1)))
    return {
        'version': version,
        'license': licencia,
    }


_about = package_metadata()

setup(
    name='tuvok',
    version=_about['version'],
    description='Terraform code validation',
    url='https://github.com/rackerlabs/tuvok/',
    author='Rackers',
    author_email='',
    license=_about['license'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
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
