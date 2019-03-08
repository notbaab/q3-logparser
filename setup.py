from setuptools import setup, find_packages
import sys


if sys.version_info < (3, 4):
    sys.exit("Sorry, python 3.4 and later is what's supported")

setup(name="quake3_log_parser",
      version='0.1',
      python_requires='>3.4.0',
      author="ET",
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      quake3-log-parser=quake3_log_parser.parser:main
      """,
      )
