"""
Various user-interface routines.

These provide a simple, consistent and robust way of gathering information from
a commandline user. Users are prompted with a question and optionally
explanatory help text and hints of possible answers.

A question is formatted as follows::

	helptext helptext helptext helptext
	helptext helptext helptext helptext
	helptext
	long choices
	long choices
	long choices
	question [hints]:

"""

### IMPORTS

import re
from exceptions import StandardError

__all__ = [
	
]



### CONSTANTS & DEFINES

SPACE_RE = re.compile ('\s+')

YESNO_SYNONYMS = {
	'yes': 'y',
	'no': 'n',
	'true': 'y',
	'false': 'n',
	'on': 'y',
	'off': 'n',
}


### IMPLEMENTATION ###

### INTERNALS

def _clean_text (text):
	"""
	Trim, un-wrap and rewrap text to be presented to the user.
	"""
	return SPACE_RE.sub (' ', text.strip())
	

def _format_hints_text (hints, default=None):
	if hints:
		hint_str = ''.join(hints)
		if default is not None:
			hint_str = "%s, default %s" % (hint_str, default)
		return " [%s]" % hint_str
	else:
		return ""


### CONVERTERS

class Converter (object):
	"""
	Converts and validates user input.
	
	Should throw an error if any problems.
	"""
	def __call__ (self, value):
		# NOTE: override in subclass
		value = self.convert(value)
		self.validate (value)
		return value
	
	def validate (self, value):
		# NOTE: override in subclass
		# probably a series of assertions
		pass
	
	def convert (self, value):
		# NOTE: override in subclass
		return value
		
		
class Clean (Converter):
	"""
	Normalize values by stripping flanking space and converting to lower case.
	
	Note that this does not explicitly throw errors.
	"""
	def __call__ (self, value):
		return value.strip().lower()
		
		
class Synonyms (Converter):
	"""
	Map values to other values.
	
	Note that this does not explicitly throw errors. If a value is un-mapped,
	it is simply returned.
	"""
	def __init__ (self, dict):
		self._syns = dict
		
	def __call__ (self, value):
		return self._syns.get (value, value)
		
		
class Vocab (Converter):
	"""
	Ensure values fall within a fixed set.
	"""
	def __init__ (self, args):
		self._allowed_values = args
		
	def __call__ (self, value):
		assert value in self._allowed_values, "I don't understand '%s'." % value
		return value

class Nonblank (Converter):
	def validate (self, value):
		assert 0 < len(value), "can't be a blank string"
		return value
	

### USER QUESTION FUNCTIONS

def ask (question, converters=[], help=None, hints=None, default='',
		strip_flanking_space=True):
	"""
	Ask for and return an answer from the user.
	
	:Parameters:
		question
			The text of the question asked.
		converters
			An array of conversion and validation functions to be called in
			sucession with the results of the previous. If any throws an error,
			it will be caught and the question asked again.
		help
			Introductory text to be shown before the question.
		hints
			Short reminder text of possible answers.
		default
			The value the answer will be set to before processing if a blank
			answer (i.e. just hitting return) is entered.
		strip_flanking_space
			If true, flanking space will be stripped from the answer before it is
			processed.
		
	This is the most general function for getting information from the user. It
	prints the help text (if any), prints the question and hints and then waits
	for input form the user. All answers are fed from the converters. If
	conversion fails, the question is re-asked. 
	"""
	## Preconditions:
	assert (question), "'ask' requires a question"
	
	## Main:
	# show leadin
	if help:
		if isinstance (help, basestring):
			help = [help]
		for h in help:
			print help
	# build presentation
	question_str = _clean_text ("%s%s: " % (question, _format_hints_text (hints, default)))
	# ask question until you get a valid answer
	while True:
		print question_str,
		raw_answer = raw_input().strip()
		if strip_flanking_space:
			raw_answer = raw_answer.strip()
		if default:
			raw_answer = raw_answer or default
		try:
			for conv in converters:
				raw_answer = conv.__call__ (raw_answer)
		except StandardError, err:
			print "A problem: %s Try again ..." % err
		except:
			print "A problem: unknown error. Try again ..."
		else:
			return raw_answer


def ask_short_choice (question, choice_str, converters=[], help=None, default=None):
	"""
	Ask the user to make a choice using single letters.
	"""
	## Preconditions:
	choice_str = choice_str.strip().lower()
	assert choice_str, "need choices for question"
	if default:
		default = default.lower()
		assert (len(default) == 1), \
		"ask_short_choice uses only single letters, not '%s'" % default
	## Main:
	if default:
		hints = "%s, default %s" % (choice_str, default)
	else:
		hints = choice_str
	## Postconditions & return:
	return ask (question,
		converters= converters or [Vocab(list(choice_str))],
		help=help, hints=hints, default=default)


def ask_yesno (question, help=None, default=None):
	choice_str = 'yn'
	return ask_short_choice (question, choice_str,
		converters=[
			lambda s: s.strip().lower(),
			Synonyms(YESNO_SYNONYMS),
			Vocab(list(choice_str)),
		],
		help=help,
		default=default,
	)

# :Parameters:
#    choices
#        An array of Choices, or raw strings
#
# Users can select a value by typing in the value or selecting a number.
#
def ask_long_choice (question, choices, help=None, default=None):
	"""
	Ask the user to make a choice from a list
	
	:Parameters:
		
	"""
	## Preconditions:
	assert choices, "need choices for question"
	if default:
		default = default.lower()
	## Main:
	# build choices list
	synonyms = {}
	vocab = []
	menu = []
	for i, c in enumerate (choices):
		if isinstance (c, basestring):
			val = c
			desc = c
			syns = []
		elif instance_of (c, Choice):
			val = c.value
			desc = c.desc or value
			syns = c.syns
		else:
			assert false, "shouldn't get here"
		assert val not in vocab, "duplicate choice value '%s'" % val
		vocab.append (val)
		menu_index = str(i + 1)
		syns.append(menu_index)
		for s in syns:
			assert not synonyms.has_key(s), "duplicate choice synonym '%s'" % s
			synonyms[s] = val
		menu.append ("   %s. %s" % (menu_index, desc))
	help = '\n'.join([help]+ menu).strip()

	## Postconditions & return:
	return ask (question,
		converters=[
			Synonyms(synonyms),
			Vocab(vocab)
		],
		help=help,
		hints='1-%s' % len(choices),
		default=default
	)


def ask_string (question, converters=[], help=None, hints=None, default=None,
		strip_flanking_space=True, allow_blank=False):
	return ask (question, converters=converters+[Nonblank()], help=help,
		hints=hints, default=default, strip_flanking_space=True)


class Choice (object):
	def __init__ (self, value, description=None, synonyms=[]):
		self.value = value
		self.desc = description
		self.synonyms = synonyms

	
	
