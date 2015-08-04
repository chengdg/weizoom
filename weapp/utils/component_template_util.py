# -*- coding: utf-8 -*-
"""@package utils.resource_util

"""

import os
import re
__author__ = 'robert'


FILTER_SEPARATOR = '|'
BLOCK_TAG_START = '{%'
BLOCK_TAG_END = '%}'
VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'
COMMENT_TAG_START = '{#'
COMMENT_TAG_END = '#}'
SPACE_SEPARATOR = '\s*'


tag_re = (re.compile('(%s.*?%s|%s.*?%s|%s.*?%s)' %
		  (re.escape(BLOCK_TAG_START), re.escape(BLOCK_TAG_END),
		   re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END),
		   re.escape(COMMENT_TAG_START), re.escape(COMMENT_TAG_END))))
space_re = re.compile(SPACE_SEPARATOR)
num_re = re.compile('\.(\d+)\.')
tail_num_re = re.compile('\.(\d+)$')
DEBUG = False


class Lexer(object):
	"""词法分析器"""
	def __init__(self, template_string):
		self.template_string = template_string

	def tokenize(self):
		"""
		Return a list of tokens from a given template_string.
		"""
		in_tag = False
		result = []
		for bit in tag_re.split(self.template_string):
			result.append(bit)
		return result


class Parser(object):
	"""对词法分析的结果进行语法分析"""
	def __init__(self, tokens):
		self.tokens = tokens

	def parse(self):
		nodes = []
		for token in self.tokens:
			token_length = len(token)
			if token_length == 0:
				continue
			if token_length > 0 and token_length <= 4:
				nodes.append(Text(token))
				continue

			token_start = token[:2]
			token_content = token[2:-2]
			if token_start == VARIABLE_TAG_START:
				nodes.append(Variable(token_content))
			elif token_start == BLOCK_TAG_START:
				nodes.append(Tag.create(token_content))
			elif token_start == COMMENT_TAG_START:
				nodes.append(Comment(token_content))
			else:
				nodes.append(Text(token))

		return nodes


class Node(object):
	def __init__(self, content):
		self.content = content

	def dump_emit_result(self):
		value = self.emit()
		if DEBUG:
			print '[emit]: `%s`\n' % value

	def emit(self):
		raise ValueError('not implemented')

	def do_dump(self):
		self.dump()
		self.dump_emit_result()


class Variable(Node):
	def __init__(self, content):
		Node.__init__(self, content)
		self.content = self.content.strip()
		self.parse()

	def parse(self):
		self.filter = None
		if not FILTER_SEPARATOR in self.content:
			return

		beg = self.content.find(FILTER_SEPARATOR)
		end = self.content.find(':', beg+1)
		if end == -1:
			end = len(self.content)
		self.filter = self.content[beg+1:end]
		self.content = self.content[:beg]


	def emit(self):
		if self.filter == 'safe':
			value = '{{{%s}}}' % self.content
		elif self.filter and 'format_target' in self.filter:
			value = 'javascript:void(0);'
		elif self.filter and 'join_sub_components_html' in self.filter:
			value = """
			{{#each component.components as |sub_component item_index|}}
				{{{sub_component.html}}}
			{{/each}}
			"""
		else:
			value = '{{%s}}' % self.content
		return value

	def dump(self):
		print '[var]: {var:`%s`, filter:"%s"}' % (self.content, self.filter)


class Text(Node):
	def __init__(self, content):
		Node.__init__(self, content)

	def emit(self):
		value = self.content
		return value

	def dump(self):
		print '[text]: `%s`' % self.content


class Comment(Node):
	def __init__(self, content):
		Node.__init__(self, content)

	def emit(self):
		value = "{{!-- %s --}}" % self.content
		return value

	def dump(self):
		print '[comment]: `%s`' % self.content


class Tag(Node):
	def __init__(self, content):
		Node.__init__(self, content)

	@staticmethod
	def create(content):
		if ('if ' in content) or ('endif' == content):
			return IfNode(content)
		elif 'ifequal ' in content:
			return IfNode(content)
		elif 'else' in content:
			return ElseNode(content)
		elif ('for ' in content) or ('for' == content):
			return ForNode(content)
		elif ('with ' in content) or ('endwith' == content):
			return WithNode(content)
		else:
			return Tag(content)

	def emit(self):		
		return ''

	def dump(self):
		print '[tag]: `%s`' % self.content


class ElseNode(Node):
	def __init__(self, content):
		Node.__init__(self, content)

	def emit(self):
		value = "{{else}}"
		return value

	def dump(self):
		print "[else node]: %s" % self.content


class IfNode(Node):
	def __init__(self, content):
		Node.__init__(self, content)
		self.parse()

	def parse(self):
		self.is_end = False
		if 'end' in self.content:
			self.is_end = True

		self.source = None
		self.operator = None
		self.target = None
		if not self.is_end:
			bits = []
			for bit in space_re.split(self.content):
				if not bit:
					continue

				bits.append(bit)

			if bits[0] == 'ifequal':
				#处理{% ifequal type 'abc' %}
				self.source = bits[1]
				self.target = bits[2]
				self.operator = '=='
			elif bits[1] == 'not':
				#处理{% if not is_active %}
				self.source = bits[2]
				self.operator = 'isnotvalid'
				self.target = ''
			else:
				#处理{% if is_active %}, {% if name == 'abc' %}
				if len(bits) > 2:
					self.source, self.operator, self.target = bits[1:]
				else:
					self.source = bits[1]

		if self.source:
			self.source = tail_num_re.sub(r'.[\g<1>]', self.source)

		self.is_forloop_first = False
		if 'forloop.first' in self.content:
			self.is_forloop_first = True
			
	def emit_start_tag(self):
		if self.is_forloop_first:
			value = "{{#ifCond item_index '===' 0}}"
		else:
			if self.operator:
				if self.operator == 'isnotvalid':
					value = "{{#ifCond %s 'isnotvalid' ''}}"  % self.source
				else:
					value = "{{#ifCond %s '%s' %s}}" % (self.source, self.operator, self.target)
			else:
				value = "{{#ifCond %s 'isvalid' ''}}" % self.source

		return value

	def emit_end_tag(self):
		value = "{{/ifCond}}"

		return value


	def emit(self):
		if self.is_end:
			value = self.emit_end_tag()
		else:
			value = self.emit_start_tag()

		return value
		

	def dump(self):
		data = {
			'is_end': self.is_end,
			'content': "`%s`" % self.content,
			'source': self.source,
			'operator': self.operator,
			'target': self.target
		}
		print '[ifnode]: %s' % data


class ForNode(Node):
	def __init__(self, content):
		Node.__init__(self, content)
		self.parse()

	def parse(self):
		self.is_end = False
		if 'end' in self.content:
			self.is_end = True

		self.source = None
		self.item_name = None
		
		if not self.is_end:
			bits = []
			for bit in space_re.split(self.content):
				if not bit:
					continue
				bits.append(bit)

			self.item_name = bits[1]
			self.source = bits[3]

	def emit_start_tag(self):
		value = "{{#each %s as |%s item_index|}}" % (self.source, self.item_name)
		return value

	def emit_end_tag(self):
		value = "{{/each}}"
		return value

	def emit(self):
		if self.is_end:
			value = self.emit_end_tag()
		else:
			value = self.emit_start_tag()

		return value

	def dump(self):
		data = {
			'is_end': self.is_end,
			'content': "`%s`" % self.content,
			'source': self.source,
			'item_name': self.item_name
		}
		print '[fornode]: %s' % data


class WithNode(Node):
	def __init__(self, content):
		Node.__init__(self, content)
		self.parse()

	def parse(self):
		self.is_end = False
		if 'end' in self.content:
			self.is_end = True

		self.source = None
		self.filter = None
		self.target = None
		
		if not self.is_end:
			bits = []
			for bit in space_re.split(self.content):
				if not bit:
					continue
				bits.append(bit)

			self.source_and_filter = bits[1]
			self.target = bits[3]
			items = self.source_and_filter.split(FILTER_SEPARATOR)
			if len(items) == 1:
				self.source = items[0]
			else:
				self.source = items[0]
				self.filter = items[1]

	def emit_start_tag(self):
		value = "{{#updateContext %s}}" % self.source
		return value

	def emit_end_tag(self):
		value = "{{/updateContext}}"
		return value

	def emit(self):
		if self.is_end:
			value = self.emit_end_tag()
		else:
			value = self.emit_start_tag()

		return value

	def dump(self):
		data = {
			'is_end': self.is_end,
			'content': "`%s`" % self.content,
			'source': self.source,
			'filter': self.filter,
			'target': self.target
		}
		print '[withnode]: %s' % data




def convert_to_handlebar_template(lines):
	result_lines = []
	for index, line in enumerate(lines):
		if DEBUG:
			print '*$*' * 20
			print 'line%d:`%s`' % (index, line)
		lexer = Lexer(line)
		tokens = lexer.tokenize()
		parser = Parser(tokens)
		nodes = parser.parse()
		items = []
		for node in nodes:
			if DEBUG:
				node.do_dump()
			items.append(node.emit())

		result_lines.append(''.join(items))

	return '\n'.join(result_lines)


def generate_handlebar_template(components_dir):
	template_paths = []
	for dir in os.listdir(components_dir):
		template_name = '%s.html' % dir
		dir = os.path.join(components_dir, dir)
		if not os.path.isdir(dir):
			continue

		template_path = os.path.join(dir, template_name)
		if not os.path.exists(template_path):
			continue

		# if not 'image.html' in template_name:
		# 	continue

		if 'itemlist.html' in template_name:
			continue

		template_paths.append(template_path)
	template_paths.append(os.path.join(components_dir, '..', 'common', 'common.html'))

	templates = []
	for template_path in template_paths:
		lines = []
		src = open(template_path, 'rb')
		for line in src:
			lines.append(line.rstrip())
		src.close()

		handlebar_template = convert_to_handlebar_template(lines)		
		templates.append(handlebar_template)

	return '\n'.join(templates)



if __name__ == '__main__':
	DEBUG = True
	components_dir = '../termite/static/termite_js/app/component/wepage'
	handlebar_template = generate_handlebar_template(components_dir)
	
	dst = open('hanblebar.html', 'wb')
	print >> dst, handlebar_template
	print 'write handlebar template content into handlebar.html'
	dst.close()