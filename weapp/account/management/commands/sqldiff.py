# -*- coding: utf-8 -*-

import os
import subprocess
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

class Field(object):
	def __init__(self, line):
		self.raw_line = line
		self.__parse(line)

	def __get_default_value(self, type):
		if 'int(' in type:
			return "0"
		elif 'double' in type:
			return "0.0"
		elif 'char' in type or 'longtext' in type:
			return '""'
		else:
			return 'NULL'

	def __parse(self, line):
		try:
			line = line.strip()
			items = line.split(' ')
			self.name = items[0][1:-1]
			self.type = items[1]
			self.default_value = self.__get_default_value(self.type)
		except:
			print 'line: ', line
			raise

	def __str__(self):
		return str({
			"name": self.name,
			"type": self.type,
			"default_value": self.default_value
		})


class Table(object):
	def __init__(self, name):
		self.name = name
		self.fields = []

	def add_field(self, field):
		self.fields.append(field)

	def finish(self):
		self.fields.sort(lambda x,y: cmp(x.name, y.name))

	def __str__(self):
		buf = []
		buf.append('*'*20 + ' table ' + self.name + ' ' + '*'*20)
		for field in self.fields:
			buf.append(str(field))
		return '\n'.join(buf)


class Database(object):
	def __init__(self, name, tables):
		self.name = name
		self.tables = tables

	def __str__(self):
		buf = []
		for table in self.tables:
			buf.append(str(table))
		return '\n\n'.join(buf)


class Migrater(object):
	def __init__(self, old_database, new_database):
		self.new_database = new_database
		self.old_database = old_database

	def __compare_table(self, source, target):
		name2targettable = dict([(table.name, table) for table in target.tables])
		tables = []

		for table in source.tables:
			if not table.name in name2targettable:
				tables.append(table.name) 

		return tables

	def __emit_filed_solution(self, old_table, new_table):
		table_name = new_table.name

		sql_buf = []
		name2oldfield = dict([(field.name, field) for field in old_table.fields])
		for new_field in new_table.fields:
			field_name = new_field.name
			old_field = name2oldfield.get(field_name, None)
			if not old_field:
				if 'longtext' in new_field.type:
					sql = 'ALTER TABLE `%s` ADD COLUMN `%s` %s NOT NULL;' % (table_name, new_field.name, new_field.type)
				else:
					sql = 'ALTER TABLE `%s` ADD COLUMN `%s` %s DEFAULT %s;' % (table_name, new_field.name, new_field.type, new_field.default_value)
				sql_buf.append(sql)
				continue

			if old_field.type != new_field.type:
				old_field = '/* %s */' % old_field.raw_line
				sql_buf.append(old_field)
				if 'longtext' in new_field.type:
					sql = '/* ALTER TABLE `%s` MODIFY COLUMN `%s` %s NOT NULL; */' % (table_name, new_field.name, new_field.type)
				else:
					sql = '/* ALTER TABLE `%s` MODIFY COLUMN `%s` %s DEFAULT %s; */' % (table_name, new_field.name, new_field.type, new_field.default_value)
				sql_buf.append(sql)

		if len(sql_buf) > 0:
			buf = ['\n\n--']
			buf.append('-- update sql for table `%s`' % table_name)
			buf.append('--')
			buf.extend(sql_buf)
			return '\n'.join(buf)
		else:
			return ''


	def emit_migrate_solution(self):
		tables_to_be_add = self.__compare_table(self.new_database, self.old_database)
		tables_to_be_delete = self.__compare_table(self.old_database, self.new_database)

		name2oldtable = dict([(table.name, table) for table in self.old_database.tables])
		buf = []
		for new_table in self.new_database.tables:
			table_name = new_table.name
			old_table = name2oldtable.get(table_name, None)
			if old_table:
				migrate_solution = self.__emit_filed_solution(old_table, new_table)
				if migrate_solution:
					buf.append(migrate_solution)

		target = open('add_table', 'wb')
		for table in tables_to_be_add:
			print >> target, table
		target.close()

		target = open('delete_table', 'wb')
		for table in tables_to_be_delete:
			print >> target, table
		target.close()

		target = open('migrate.sql', 'wb')
		print >> target, '\n'.join(buf)
		target.close()


class Parser(object):
	def __init__(self):
		pass

	def __is_comment_line(self, line):
		if line.startswith('--') or line.startswith('/*'):
			return True
		return False

	def __is_drop_table_line(self, line):
		if 'DROP TABLE' in line:
			return True
		return False

	def __is_create_table_start(self, line):
		if line.startswith('CREATE TABLE'):
			return True
		return False

	def __is_create_table_end_line(self, line):
		if 'ENGINE=' in line:
			return True
		return False		

	def __extract_table_name(self, line):
		beg = line.find('`', 0)
		end = line.find('`', beg+1)
		return line[beg+1:end]

	def __is_field_line(self, line):
		if 'KEY' in line or 'CONSTRAINT' in line:
			return False
		return True

	def parse(self, sql_file_name):
		tables = []
		current_table = None
		for line in open(sql_file_name, 'rb'):
			if self.__is_comment_line(line) or\
				self.__is_drop_table_line(line):
				continue

			line = line.strip()
			if not line:
				continue

			if self.__is_create_table_start(line):
				table_name = self.__extract_table_name(line)
				current_table = Table(table_name)
				tables.append(current_table)
			elif self.__is_create_table_end_line(line):
				current_table.finish()
				current_table = None
			else:
				if self.__is_field_line(line):
					field = Field(line)
					current_table.add_field(field)

		return Database(sql_file_name, tables)
	


class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--old',
			action='store',
			dest='old_sql_file',
			default='',
			help='old sql file'
		),
		make_option('--new',
			action='store',
			dest='new_sql_file',
			default='',
			help='new sql file'
		)
	)
	help = "compare new sql and old sql to generate sql migrate file"
	args = ''
	
	def handle(self, *args, **options):
		old_file = options['old_sql_file']
		new_file = options['new_sql_file']

		parser = Parser()
		new_database = parser.parse(new_file)
		old_database = parser.parse(old_file)

		migrater = Migrater(old_database, new_database)
		migrater.emit_migrate_solution()
		print 'finish!'
