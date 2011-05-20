#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Interactively generate the supporting files for a Galaxy extension."
# TODO: all the format crap should be in one table

__docformat__ = 'restructuredtext en'
__author__ = 'Paul-Michael Agapow <pma@agapow.net>'


### IMPORTS ###

from os import path
from argparse import ArgumentParser
from exceptions import BaseException

from bioscripts.galgen import __version__
from bioscripts.galgen import ui


### CONSTANTS & DEFINES ###

MAKEID_RE = re.compile (r'[\s_-\\\/]+')

_DEV_MODE = True


### IMPLEMENTATION ###

### UTILS

def print_section (section_title):
	print ("\n%s\n" % section_title)


def make_id (name):
	return MAKEID_RE.sub ('_', name)



### ASK ABOUT & GENERATE TOOL FILES

def generate_tool_files (options):
	ask_tool_information (options)
	ask_commandline_form (options)
	ask_generation_details (options)
	

def ask_tool_information (options):
	print_section ("Tool details"):
	options.tool_name = ask_string ("What is the tool name",
		help="""The tool must have a name, which will be publically visible and
			appears on the tool menu and form."""
	)
	options.tool_version = ask_string ("What is the tool version",
		help="""The tool may have a version number, which is only important for
			tool updates."""
		default="0.1",
	)
	options.tool_id = ask_string ("What is the tool's id",
		help="""The tool must have a unique id, which is used internally for
			distinguishing tools.""",
		default=make_id(options.tool_name),
	)
	options.tool_desc = ask_string ("What is the tool's description",
		help="A short description may be supplied and will appear in the tool menu.",
		allow_blank=True,
	)
	options.tool_help = ask_string ("What is the tool's help text",
		help="""Extended help text may be supplied in restructured text format.""",
		allow_blank=True,
	)
	
	
def ask_commandline_form (options):
	print_section ("Commandline details"):
	options.tool_help = ask_string ("What is the form of the command-line",
		help="""How is the wrapped commandline executable called? Choose one of
			the below options, or manually enter one, using either the abstract
			notation or an actual commandline. The abstract """,
		choices=[
			'exe option* infile > outfile',
			'exe option* infile outfile',
			'exe option* infile > outfile',
			'exe option* infile > outfile',
			
		],
		default=1,
	)
	pass

def ask_generation_details (options):
	ask_yesno ("Is the executable internal",
		default='y',
		help="""Tools can call executables that are internal (i.e. packaged
			inside the tool directory) or external (i.e. present elsewhere on the
			system)""",
	)
	ask_string ("Name the tool-conf.xml entry fragment",
		default=
	)
	ask_string ("Name the tool folder",
		default=
	)
	ask_string ("Name the config file",
		default=
	)


### MAIN ###

def parse_main_args (op, args):
	op.epilog="""The following commands are available:\n* tool: generate files for wrapping a commandline tool for Galaxy""",
	options, pargs = optparser.parse_args (args)
	return 'main', options, pargs
	
	
def parse_tool_args (op, args):
	op.usage = '%s tool [options]' % op.prog
	op.epilog="""This command generates the necessary supporting files for
		wrappping a commandline and incorporating it into Galaxy. In more detail,
		given an example of program, it deduces the """,
		
	
	
	

	
	optparser.add_argument ('--tool-name',
		dest='tool_name',
		help='The name for the generated tool',
		metavar='DIR-NAME',
	)
	
	optparser.add_argument ('--tool-conf-entry-name',
		dest='tool-conf-name',
		help='The name for the generated tool-conf.xml file entry',
		metavar='FILE-NAME',
		default='%(tool_name)s-tool-conf-entry.xml'
	)
		
	optparser.add_argument ('--tool-dir-name',
		dest='tool_dir_name',
		help='The name for the generated tool directory',
		metavar='DIR-NAME',
		default='%(tool_name)s'
	)
	
	optparser.add_argument ('--dryrun',
		 dest='dryrun',
		 help='Test user input but do not actually generate files.'
		 action='store_true',
	)
	
	# XXX: don't actually use input files, may at some point in future
	options, pargs = optparser.parse_args()
	
	## Postconditions & return:
	if (0 <= len (pargs)):
		optparser.error ('unrecognised trailing arguments')
	return out_fmt, infiles, options
		
		
		
	options, pargs = optparser.parse_args (args)
	return 'main', options, pargs
	
	
def parse_args():
	# Construct the general option parser.
	usage = '%(prog)s COMMAND [options]'
	version = 'version %s' %  __version__
	desc = 'Generates templates and files for Galaxy extensions.'
	op = ArgumentParser (usage=usage, version=version, prog=prog, description=desc)

	
	# if you have a command
	if (0 < len(args)):
		cmd = args[0].lower()
		if cmd == 'tool':
			return parse_tool_args (op, args[1:])
			
	# Return:
	return op.parse_args()



def main():
	options, pargs = parse_args()
	generate_tool_files (options)


if __name__ == '__main__':
	try:
		main()
	except BaseException, err:
		if (_DEV_MODE):
			raise
		else:
			print err
	except:
		print "An unknown error occurred.\n"



### END ######################################################################

