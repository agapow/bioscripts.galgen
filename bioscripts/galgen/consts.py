"""
Module-wide constants.

Some more localized constants are kept in indivdual files.
"""

### IMPORTS

import re
from exceptions import StandardError


### CONSTANTS & DEFINES

# various files that 
FILE_FORMATS = {
	'fasta': ['fas', 'fa'],
	'csv': [],
	'tsv': ['tabular', 'tab'],
}

FILE_EXT_TO_FORMAT = {}

for k,v in FILE_FORMATS:
	FILE_EXT_TO_FORMAT[k] = k
	for ext in v:
		FILE_EXT_TO_FORMAT[ext] = k



### END #######################################################################
