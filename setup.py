from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='bioscripts-gengtool',
      version=version,
      description="Script for generating Galaxy tool templates",
      long_description=open("README.txt").read() + "\n" +
         open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='galaxy bioinformatics toolsi generate',
      author='Paul-Michael Agapow',
      author_email='pma@agapow.net',
      url='http://svn.plone.org/svn/collective/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bioscripts'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
