"""
Various user-interface routines.

A question is formatted as follows::

	helptext helptext helptext helptext
	helptext helptext helptext helptext
	helptext
	question [hints or choices]:

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
	


### CONVERTERS

class Converter (object):
	"""
	Converts and validates user input.
	
	Should throw an error if any problems.
	"""
	
	def __call__ (self, value):
		assert False, "must override in subclass"
		
		
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
		assert value in self._allowed_values, "'%s' is not an allowed value" % value
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
		print "%s\n" % _clean_text(help)
	# build presentation
	if hints:
		hint_str = " [%s]" % hints
	else:
		hint_str = ""
	question_str = _clean_text ("%s%s: " % (question, hint_str))
	# ask question until you get a valid answer
	while True:
		print question_str,
		raw_answer = raw_input().strip()
		if strip_flanking_space:
			raw_answer = raw_answer.strip()
		raw_answer = raw_answer or default
		try:
			for conv in converters:
				raw_answer = conv.__call__ (raw_answer)
		except StandardError, err:
			print "A problem: %s!" % err
		except:
			print "A problem: unknown error!"
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


def ask_long_choice (question, choices, converters=[], help=None, default=None):
	"""
	Ask the user to make a choice from a list
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
	


class Choice (object):
	def __init__ (self, value, help=None, shortcut=None):
		self.value = value
		self.help = help
		self.shortcut = shortcut

	
	
