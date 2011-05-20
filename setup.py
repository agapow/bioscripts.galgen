from setuptools import setup, find_packages
import os

from bioscripts.galgen import __version__

setup(name='bioscripts-galgen',
	version=__version__,
	description="Script for generating Galaxy tool templates",
	long_description=open("README.txt").read() + "\n" +
		open(os.path.join("docs", "HISTORY.txt")).read(),
	classifiers=[
		# TODO: get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Programming Language :: Python",
	],
	keywords='galaxy bioinformatics tools generate',
	author='Paul-Michael Agapow',
	author_email='pma@agapow.net',
	url='http://agapow.net/software/bioscripts-galgen',
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
