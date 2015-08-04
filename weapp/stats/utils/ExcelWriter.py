#/usr/bin/python
# coding:utf-8
"""
写Excel的工具
"""

import xlwt
#from datetime import datetime

class ExcelWriter:
	def __init__(self, filename):
		self.filename = filename

		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True

		self.wb = xlwt.Workbook()
		self.ws = self.wb.add_sheet("Default")
		return

	def close(self):
		if self.wb is not None:
			self.wb.save(self.filename)
		self.wb = None
		return

	# 添加一个元素
	def add(self, row, column, element):
		self.ws.write(row, column, element)
		return

	def addString(self, row, column, text):
		self.add(row, column, text)
		return

	def currentSheet(self):
		return self.ws


if __name__=="__main__":
	writer = ExcelWriter("sample.xls")
	writer.add(0, 0, "Hello")
	writer.add(2, 1, "World!")
	writer.close()
