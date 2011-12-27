# -*- coding: UTF-8 -*-

"""
TableParser
	Objects for parsing an HTML file with tables in it.

Copyright © 2004 Jason R. Coombs
"""

import htmllib
import formatter
import types
import logging

log = logging.getLogger('TableParser')

class HTMLObject(object):
	def __init__(self, name):
		self.name = name

class HTMLTable(list):
	current_row = None

class HTMLRow(list):
	current_element = None

class HTMLElement(object):
	"A mutable variant object"
	def __init__(self):
		self.value = None

	def append(self, value):
		if type(self.value) == types.ListType:
			self.value.append(value)
		if type(self.value) == types.TupleType:
			self.value += (value,)
		if type(self.value) == types.StringType:
			self.value += value
		if self.value is None:
			self.value = value

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return repr(self.value)

class TableParser(htmllib.HTMLParser):
	"""
	Parse any number of tables from an HTML file.  Attempts to parse incorrect
	HTML as well, but no guarantees are made.

	The parser will accept nested tables as <table> inside <td> elements.
	"""
	def __init__(self):
		htmllib.HTMLParser.__init__(self, formatter.NullFormatter())
		self.tables = []
		self.current_table = None

	def start_table(self, attrs):
		if self.current_table:
			# We were already in a table, so grab any data that was already
			#  parsed for this element.
			self.save_current()
		new_table = HTMLTable()
		self.tables.append(new_table)
		new_table.parent_table = self.current_table
		self.current_table = new_table
		self.current_table.extra_rows = {}

	def end_table(self):
		self.current_table = self.current_table.parent_table
		if self.current_table:
			# we were already in a table, so start saving data again.
			self.save_bgn()

	def start_tr(self, attrs):
		self.end_tr()
		new_row = HTMLRow()
		self.current_table.append(new_row)
		self.current_table.current_row = new_row

	def end_tr(self):
		if self.current_table.current_row is None:
			#do nothing and
			return
		self.check_for_extra_rows()
		# The following two statements might be a bit confusing, so here's
		#  some background. The first statement replaces all elements in the
		#  current row with elements converted to strings.  It uses the [:]
		#  notation so it modifies the existing object in place and doesn't
		#  just replace it... and since that object is referenced by the list
		#  of rows in the current_table, that list will also be modified. The
		#  second statement removes the current_row reference, but the object
		#  is still referenced by the list of rows in the current_table.
		self.current_table.current_row[:] = (
			x.value for x in self.current_table.current_row
		)
		self.current_table.current_row = None

	def start_td(self, attrs):
		if self.current_table.current_row is None:
			# found a <td> tag not preceeded by a <tr> tag, so one is implied.
			self.start_tr({})
		self.check_for_extra_rows()
		attrs = dict(attrs)
		try:
			# TODO: assign for additional columns as well if 'colspan' is set
			current_column_number = len(self.current_table.current_row)
			self.current_table.extra_rows[current_column_number] = (
				int(attrs['rowspan']) - 1
			)
		except KeyError:
			pass
		try:
		    self.current_table.current_row.extraCols = int(attrs['colspan']) - 1
		except KeyError:
			self.current_table.current_row.extraCols = 0
		new_element = HTMLElement()
		self.current_table.current_row.append(new_element)
		self.current_table.current_row.current_element = new_element
		# start remembering the contents of the element
		self.save_bgn()

	def end_td(self):
		self.save_current()
		# fill in blanks for the extra columns
		self.current_table.current_row.extend(
			[HTMLElement()] * self.current_table.current_row.extraCols)
		)
		self.current_table.current_row.current_element = None

	def save_current(self):
		self.current_table.current_row.current_element.append(self.save_end())

	def check_for_extra_rows(self):
		current_column_number = len(self.current_table.current_row)
		extra_rows = self.current_table.extra_rows
		if extra_rows.has_key(current_column_number):
			extra_rows[current_column_number] -= 1
			self.current_table.current_row.append(HTMLElement())
			if extra_rows[current_column_number] == 0:
				del extra_rows[current_column_number]
			# Now check again
			self.check_for_extra_rows()
