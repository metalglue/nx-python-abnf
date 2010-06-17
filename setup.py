from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='nx-python-abnf',
      version=version,
      description="ABNF",
      long_description="""\
ABNF""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ABNF',
      author='Norio Kimura',
      author_email='norioxkimura@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
