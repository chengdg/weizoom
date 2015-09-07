import re

# To be set in settings.py
STRIPPER_TAG = '__STRIPPER_TAG__'

# Finders
FIND_BLANK_LINE = r'\n(\s*)\n'
FIND_START_BLANK_LINE = r'^(\s*)\n'
FIND_TAG = STRIPPER_TAG

# Deleters
DELETE_BLANK_LINE = '\n'
DELETE_START_BLANK_LINE = ''
DELETE_TAG = ''

STRIPPER_ENABLED = True


'''
strip lines
'''
def strip_lines(content):
	if not STRIPPER_ENABLED:
		return content

	# Checks if the content type is allowed
	allowed = True

	# If the content type is not allowed, untag and return
	if not allowed:
		content = content.replace(STRIPPER_TAG, DELETE_TAG)
		return content

	# Suppress a blank line at the beginning of the document
	content = re.sub(FIND_START_BLANK_LINE, DELETE_START_BLANK_LINE, content)
	# Suppress blank lines
	content = re.sub(FIND_BLANK_LINE, DELETE_BLANK_LINE, content)
	# Delete STRIPPER_TAG
	# response.content = re.sub(FIND_TAG, DELETE_TAG, response.content)
	content = content.replace(STRIPPER_TAG, DELETE_TAG)
	return content
	