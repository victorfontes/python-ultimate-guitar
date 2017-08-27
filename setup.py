# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    from pip.req import parse_requirements
except ImportError:
    def requirements(f):
        reqs = open(f, 'r').read().splitlines()
        reqs = [r for r in reqs if not r.strip().startswith('#')]
        return reqs
else:
    def requirements(f):
        install_reqs = parse_requirements(f, session='hack')
        reqs = [str(r.req) for r in install_reqs]
        return reqs


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()
#print list(parse_requirements('requirements.txt'))
setup(
    name='python-ultimate-guitar',
    version='0.1.0',
    description='Search ultimate-guitar.com and download the results from the command line.',
    long_description=readme,
    author='Victor Costa',
    author_email='contato@victorfontes.com',
    url='https://github.com/victorfontes/python-ultimate-guitar',
    license=license,
    packages=find_packages(exclude=('tests', 'docs',)),
    #install_requirements = parse_requirements('requirements.txt', session=PipSession),
    install_requires = requirements('requirements.txt')

)

