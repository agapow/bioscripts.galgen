

### IMPORTS

import shlex
from pyparsing import *


### CONSTANTS & DEFINES

from string import letters

INTERP_VOCAB = [
	'ruby',
	'python',
	'perl',
]


### IMPLEMENTATION ###


# Take an example commandline and dbreak into symbols
#
def tokenize (cmdline):
	# this handles quoted arguments, redundant 
	return shlex.split (cmdline)

TEST_CMDLINES = [
	"foo infile.txt outfile.txt",
	"ruby myscript.rb --foo outfile.txt",
	"ruby myscript.rb n x infile.txt > outfile",
]


# Things we are currently not trying to handle:
# - quoted arguments
# - options of the form "-nFILE"
# - options of the form "--foo=FILE"
# - options that take multiple parameters (e.g. "--twofiles FILE1 FILE2")
# These *may* be handled in time

# primitives
param = Word (alphas + '-_.').setResultsName("param")

elems = []
printcrap = lambda t: elems.append(t)

interpreter = oneOf ('python perl ruby', caseless=True)
compiled_exe = Word (alphas + '-_')
script_exe = Word (alphas + '-_.')

executable = Or (
	compiled_exe,
	Optional (interpreter) + script_exe,
)

option = Or ([
	Word(letters, min=1, max=1),
	Regex(r'\-\w+'),
	Regex(r'\-\-\w\w+'),
])
option_pair = Group (option + Optional(param))
options_and_args = ZeroOrMore (option_pair)


trailing_args = ZeroOrMore (Word (alphas + '-_.'))

pipe = Literal('>')
output_file = param
pipe_output = Optional (pipe + output_file)



cmdline = executable + options_and_args + trailing_args + pipe_output


for c in TEST_CMDLINES:
	global x
	x = cmdline.parseString(c)
	print type(x)
	print "%s: %s" % (c, x)



