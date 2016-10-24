# Copyright (C) 2014 Chris Warrick.
# From: http://chriswarrick.com/
# License: CC BY http://creativecommons.org/licenses/by/3.0/

from setuptools import setup

setup(name='phylophilter',
      version='0.1.0',
      packages=['phylophilter'],
      entry_points={
          'console_scripts': [
              'phylophilter = phylophilter.__main__:main'
          ]
      },
      )