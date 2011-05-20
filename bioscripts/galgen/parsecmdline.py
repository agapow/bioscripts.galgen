"""
Reduce a commandline to identifiable components. 

To produce tool templates and 

"""


### IMPORTS

import re

from pyparsing import *


### CONSTANTS & DEFINES

FILENAME_RE = re.compile (r'^[\w\-\.\_]+\.[a-zA-z]\w*$')
INPUT_FILE_RE = re.compile (r'^(in|input)\W', re.IGNORECASE)
OUTPUT_FILE_RE = re.compile (r'^(out|output)\W', re.IGNORECASE)

INTERP_VOCAB = [
	'ruby',
	'python',
	'perl',
]


### IMPLEMENTATION ###

class Token (dict):
	def __init__ (self, type, val, **kwargs):
		self.type = type
		self.value = val
		for k,v in kwargs.iteritems():
			self[k] = v

	def _set_type (self, v):
		self['type'] = v
		
	def _set_value (self, v):
		self['value'] = v
	
	type = property (lambda: self['type'], _set_type)
	value = property (lambda: self['value'], _set_value)



# Take an example commandline and dbreak into symbols
#
def tokenize (cmdline):
	# this handles quoted arguments, redundant 
	return shlex.split (cmdline)

TEST_CMDLINES = [
	"foo infile.txt outfile.txt",
	"ruby myscript.rb --foo outfile.txt",
	"myscript.rb --foo outfile.txt",
	"myscript.rb --foo --bar outfile.txt",
	"ruby myscript.rb n x infile.txt > outfile",
]


# Things we are currently not trying to handle:
# - quoted arguments
# - options of the form "-nFILE"
# - options of the form "--foo=FILE"
# - options that take multiple parameters (e.g. "--twofiles FILE1 FILE2")
# These *may* be handled in time

# primitives

def make_argument_token (val):
	return val

param = Word(alphanums + '-_.')

option = Or ([
	Word(alphas, min=1, max=1),
	Combine (Literal('-') + Word(alphanums + '-_')),
	Combine (Literal('--') + Word(alphanums + '-_')),
]).setParseAction (
	lambda t: Token ("option", t[0])
)

option_list = ZeroOrMore (option).setParseAction (
	lambda t: Token ("option_list", t.asList())
)


trailing_args = ZeroOrMore (param).setParseAction (
	lambda t: Token ("trailing_args", t.asList())
)

# NOTE: we can infer this is an output file from context
captured_output = Optional (
	Group (Literal('>') + param).setParseAction (
		lambda t: Token ("captured_output", t[0][1])
	)
)


# components of the commandline
interpreter = oneOf ('python perl ruby', caseless=True)

script_exe = Combine (Word (alphas + '-_') +'.' + oneOf ('py pl rb'))

def make_interpreted_token (vals):
	if len(vals) == 2:
		return Token ("executable", vals[1], intepreter=vals[0])
	else:
		script = vals[0]
		interps = {
			"py": "python",
			"pl": "perl",
			"rb": "ruby",
		}
		for k,v in interps.iteritems():
			if script.endswith (".%s" % k):
				return Token ("executable", script, interpreter=v)
		return Token ("executable", script, interpreter=None)
		
interpreted_exe = Group (Optional (interpreter) + script_exe).setParseAction (
	lambda t: make_interpreted_token(t[0])
)

compiled_exe = Word (alphanums + '-_').setParseAction (
	lambda t: Token ("executable", t[0])
)

executable = Or ([
	interpreted_exe,
	compiled_exe,
])


# the actual commandline, the starting point
cmdline = executable + option_list + trailing_args + captured_output


for c in TEST_CMDLINES:
	try:
		x = cmdline.parseString(c)
		print "%s:" % c
		for item in x:
			print "- %s" % item
		print "\n"
	except ParseException, err:
		print "Error!"
		print "Line: %s" % err.line
		print "Message: %s" % err.msg
		print "Location: %s:%s:%s" % (err.loc, err.lineno, err.column)


