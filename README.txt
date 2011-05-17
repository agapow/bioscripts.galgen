Introduction
============

Writing tool template files for Galaxy can sometimes be extended and error-prone
process, especially if you're not a programmer or inexperienced in XML and
templating systems. *bioscripts.gengtool* is a Python library that packages a
script for generating the files that Galaxy requires to wrap a commandline tool
from a series of interactive questions. For simple tools, these files should be
complete and ready for use. For more complex tools, they will serve as a useful
basis for further customization and tweaking.


Installation
============


Tool generation overview
========================

The tool generation script is called ``gene-gtool`` and can be called from the
commandline as such::

	% gen-gtool

Commandline options are available, see below.

The script then asks a series of questions about the tool to be generated: first
general information about the tool (e.g. is it a script, what version), followed
by how the tool is called on the commandline (e.g. how many and what sort of
options). Finally, it steps through each of these options, allowing the user to
define how these are set. These answers are then used to generate the entry in
tool_conf.xml, the tool folder and various entries within (e.g. the
config file).





Tool generation options
=======================



References
==========

