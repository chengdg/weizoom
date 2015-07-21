#coding=utf8

from pandas import DataFrame
from pandas import ExcelWriter

def dump_table(table):
	print(">>>>>> %s <<<<<<" % table.title)
	print '{}'.format(table.row_name),
	for y in table.column_list:
		print "\t",
		print y,
	print
	rows = table.rows
	for (key, row) in table.rows.items():
		print key,
		for y in table.column_list:
			print "\t",
			value = row.get(y)
			if value is None:
				print '-',
			else:
				print '{}'.format(value),
		print
	return	


# Table表示二维数据表
class Table:

	def __init__(self, title="Table", row_name='-'):
		self.title = title
		self.row_name = row_name
		self.column_names = set() # 名字集合
		self.column_list = []  # 列表
		self.rows = dict()
		self.row_name = row_name

	# 添加元素
	def put(self, row_key, col, element):
		row = self.rows.get(row_key)
		if row is None:
			row = dict()
			self.rows[row_key] = row
		row[col] = element
		if not col in self.column_names:
			self.column_names.add(col)
			self.column_list.append(col)
		return

	# 获取元素
	def get(self, row_key, col):
		row = self.rows.get(row_key)
		if row:
			return row.get(col)
		return None

	def has_key(self, key):
		return key in self.rows

	def get_row_keys(self):
		return self.rows.keys()

	# 为(row_key, col)元素增加delta
	def add(self, row_key, col, delta):
		value = self.get(row_key, col)
		if value is None:
			value = delta
		else:
			value+=delta
		self.put(row_key, col, value)
		return value

	# 转换成DataFrame
	def to_dataframe(self, is_sorted=False):
		if is_sorted:
			return DataFrame(self.rows).T
		return DataFrame(self.rows, index=self.column_list).T


	def to_html(self, filename):
		df = self.to_dataframe()
		df.to_html(filename) #, force_unicode=True)
		return


	def to_excel(self, filename, encoding="utf8"):
		writer = ExcelWriter(filename, writer_options={'use_xlsxwriter': True})
		df = self.to_dataframe()
		df.to_excel(writer, self.title, float_format="%.3f", encoding=encoding)
		writer.close()
		return

if __name__=="__main__":
	table = Table("test")
	table.put('1', 'A', "1A")
	table.put('3', 'C', 3)
	table.put('2', 'C', '2C')
	table.put('2', 'B', "2B")

	dump_table(table)

	df = table.to_dataframe()
	print(df)
	df.to_html("sample.html", force_unicode=True)
	table.to_excel("sample.xlsx", encoding='utf8')