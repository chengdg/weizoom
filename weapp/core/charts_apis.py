# -*- coding: utf-8 -*-

__author__ = 'chuter'


import copy

from jsonresponse import create_response

from utils.classes_util import singleton

@singleton
class MyEcharts(object):
	TOOLTIP_OPTION_NAME = 'tooltip'
	DEFAULT_TOOLTIP_OPTION = {
			"trigger": "item",
			"formatter": "{a} <br/>{b} : {c} ({d}%)"
		}

	LEGEND_OPTION_NAME = 'legend'
	DEFAULT_LEGEND_OPTION = {
			"orient": "horizontal",
			"x": "left"
		}

	TOOLBOX_OPTION_NAME = 'toolbox'
	DEFAULT_TOOLBOX_OPTION = {
			"show": True,
			"feature": {
			   "saveAsImage": {"show": True} 
			}
		}

	CALCULABLE_OPTION_NAME = 'calculable'
	DEFAULT_CALCULABLE_OPTION = True

	SERIES_OPTION_NAME = 'series'
	DEFAULT_SERIES_OPTION = [{
		}]

	COMMON_OPTION = {
			TOOLTIP_OPTION_NAME: DEFAULT_TOOLTIP_OPTION,
			LEGEND_OPTION_NAME: DEFAULT_LEGEND_OPTION,
			TOOLBOX_OPTION_NAME: DEFAULT_TOOLBOX_OPTION,
			CALCULABLE_OPTION_NAME: DEFAULT_CALCULABLE_OPTION,
			SERIES_OPTION_NAME: DEFAULT_SERIES_OPTION
		}

	ITEMSTYLE_OPTION_NAME = 'itemStyle'
	DEFAULT_PIE_ITEMSTYLE = {
		"normal": {
			"label": {
				"show": False
			},
			"labelLine": {
				"show": False
			}
		},
		"emphasis": {
			"label": {
				"show": True,
				"position": 'center',
				"textStyle": {
					"fontSize": '30',
					"fontWeight": 'bold'
				}
			}
		}
	}

	DEFAULT_MAP_ITEMSTYLE = {
		"normal": {"label":{"show":True}},
		"emphasis": {"label":{"show":True}}
	}

	def create_pie_chart_option(self, title, name_2_values, tooltip=None):
		option = copy.deepcopy(self.COMMON_OPTION)
		option[self.LEGEND_OPTION_NAME]['data'] = []

		series_options = option[self.SERIES_OPTION_NAME][0]
		series_options['type'] = 'pie'
		series_options['name'] = title
		series_options['radius'] = ["50%", "70%"]

		series_options['data'] = []

		data_dict_arr = series_options['data']
		lagend_data_arr = option[self.LEGEND_OPTION_NAME]['data']
		for name in name_2_values:
			data_item = {}
			data_item['name'] = name
			data_item['value'] = name_2_values[name]

			lagend_data_arr.append(name)
			data_dict_arr.append(data_item)

		#add by duhao 20150525
		if tooltip:
			option[self.TOOLTIP_OPTION_NAME] = tooltip

		series_options[self.ITEMSTYLE_OPTION_NAME] = self.DEFAULT_PIE_ITEMSTYLE

		return option

	def create_line_chart_option(
			self, 
			x_unit_label,
			y_unit_label,
			x_values,
			y_values_list,
			color_list = None, 
			use_double_y_lable = False
		):
		option = copy.deepcopy(self.COMMON_OPTION)
		option[self.LEGEND_OPTION_NAME]['data'] = []
		option[self.SERIES_OPTION_NAME] = []

		option[self.TOOLTIP_OPTION_NAME] = {
			"trigger": 'axis',
			# "formatter": "{b}%s : {c}%s" % (x_unit_label, y_unit_label)
		}

		option['xAxis'] = {
			"type" : 'category',
			"axisLine" : {"onZero": False},
			"axisLabel" : {
				"formatter": '{value}%s' % (x_unit_label)
			},
			"data" : x_values
		}
		
		if use_double_y_lable:
			option['yAxis'] = [{
				"type" : 'value',
				"axisLabel" : {
					"formatter": '{value}%s' % (y_unit_label)
				}
			}, {
				"type" : 'value',
				"axisLabel" : {
					"formatter": '{value}%s' % (y_unit_label)
				}
			}]
		else:
			option['yAxis'] = {
				"type" : 'value',
				"axisLabel" : {
					"formatter": '{value}%s' % (y_unit_label)
				}
			}

		lagend_data_arr = option[self.LEGEND_OPTION_NAME]['data']
		series_options = option[self.SERIES_OPTION_NAME]
		index = 0
		for y_values in y_values_list:
			name = y_values['name']
			values = y_values['values']

			one_series_options = {}
			one_series_options['name'] = name
			one_series_options['type'] = 'line'
			one_series_options['smooth'] = True
			one_series_options['data'] = values
			if use_double_y_lable:
				one_series_options['yAxisIndex'] = index
				index = (index + 1) % 2

			if y_values.has_key('tooltip'):
				one_series_options['tooltip'] = y_values['tooltip']

			lagend_data_arr.append(name)
			series_options.append(one_series_options)

		if color_list:
			option['color'] = color_list
		
		return option

	def create_bar_chart_option(
			self, 
			x_values,
			y_values_list,
			reverse=False,
			show_legend=True
		):
		option = copy.deepcopy(self.COMMON_OPTION)
		option[self.LEGEND_OPTION_NAME]['data'] = []
		option[self.SERIES_OPTION_NAME] = []

		if not show_legend:
			option[self.LEGEND_OPTION_NAME]['show'] = False

		if reverse:  #横向柱状图
			option['xAxis'] = {
				"type" : 'value',
				# "data" : x_values
			}

			option['yAxis'] = {
				"type" : 'category',
				"data" : x_values
			}
		else:
			option['xAxis'] = {
				"type" : 'category',
				"data" : x_values
			}

			option['yAxis'] = {
				"type" : 'value',
			}

		lagend_data_arr = option[self.LEGEND_OPTION_NAME]['data']
		series_options = option[self.SERIES_OPTION_NAME]
		for y_values in y_values_list:
			name = y_values['name']
			values = y_values['values']

			one_series_options = {}
			one_series_options['name'] = name
			one_series_options['type'] = 'bar'
			one_series_options['data'] = values

			#add by duhao 205-05-22 加入提示条控制信息
			if y_values.has_key('tooltip'):
				one_series_options['tooltip'] = y_values['tooltip']
			if y_values.has_key('barWidth'):
				one_series_options['barWidth'] = y_values['barWidth']

			lagend_data_arr.append(name)
			series_options.append(one_series_options)
		return option

	def create_map_char_option(self, title, name_2_values_list):
		option = copy.deepcopy(self.COMMON_OPTION)
		option[self.LEGEND_OPTION_NAME]['data'] = []
		option[self.SERIES_OPTION_NAME] = []

		series_options = option[self.SERIES_OPTION_NAME]

		lagend_data_arr = option[self.LEGEND_OPTION_NAME]['data']
		minValue = 9999999999999
		maxValue = 0
		for name_2_values in name_2_values_list:
			name = name_2_values['name']

			one_series_options = {}
			one_series_options['name'] = name
			one_series_options['type'] = 'map'
			one_series_options['mapType'] = 'china'
			one_series_options['roam'] = False
			one_series_options[self.ITEMSTYLE_OPTION_NAME] = self.DEFAULT_MAP_ITEMSTYLE

			data_dict_arr = []
			for value in name_2_values['values']:
				#value format is like: {'name':value}
				key = value.keys()[0]
				key_value = value[key]

				data_item = {}
				data_item['name'] = key
				data_item['value'] = value[key]
				data_dict_arr.append(data_item)

				if key_value < minValue:
					minValue = key_value
				if key_value > maxValue:
					maxValue = key_value

			one_series_options['data'] = data_dict_arr 

			lagend_data_arr.append(name)
			series_options.append(one_series_options)

		option['dataRange'] = {
			"min": minValue,
			"max": maxValue,
			"x": 'left',
			"y": 'bottom',
			"text":['高','低'], 
			"calculable" : True
		}

		option['roamController'] = {
			"show": True,
			"x": 'right',
			"y": 'center',
			"mapTypeControl": {
				'china': True
			}
		}

		return option

myecharts = MyEcharts()

def create_pie_chart_response(title, name_2_values, tooltip=None):
	"""
	创建饼图数据的response
	@title 饼图的标题, 如果不需要设置为""
	@param name_2_values 饼图中所有项的名称和数值

	例如：
	{"微众":90, "微盟":4, "时趣":5, "其它":1}
	"""

	pie_charts_jsondata = myecharts.create_pie_chart_option(title, name_2_values, tooltip)

	response = create_response(200)
	response.data = pie_charts_jsondata
	
	return response.get_response()


def create_map_chart_response(title, name_2_values_list):
	"""
	创建地图数据的response
	@title 地图的标题，如果不需要设置为""
	@param name_2_values 地图中所有项的名称和数值

	例如：
	[{
		"name": "iphone",
		"values" : [
			{'北京': 100000},
			{'上海': 10000},
			{'广州': 20000},
		]
	}, {
		"name" : "小米",
		"values" : [
			{'北京': 100000},
			{'上海': 10000},
			{'广州': 20000},
		]
	}]
	"""

	map_charts_jsondata = myecharts.create_map_char_option(title, name_2_values_list)

	response = create_response(200)
	response.data = map_charts_jsondata
	
	return response.get_response()

def create_line_chart_response(
		x_unit_label,
		y_unit_label,
		x_values,
		y_values_list,
		color_list = None,
		use_double_y_lable = False,
		get_json=False
	):
	"""
	创建折线图数据的response
	@param x_unit_label 折线图中x轴显示的单位名称
		例如"个"，如果不需要单位可指定为""
	@param y_unit_label 折线图中y轴显示的单位名称
		例如"个"，如果不需要单位可指定为""
	@param x_values 折线图中x轴的所有坐标点
		例如['2010-10-10', '2010-10-11', '2010-10-12']
	@param y_values_list 折线图中要显示的所有线的所有y轴的值序列
		例如：
		[{
			"name": "iphone",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "小米",
			"values" : [60, 70, 80, 100]
		}]
	"""

	map_charts_jsondata = myecharts.create_line_chart_option(
		   x_unit_label,
		   y_unit_label,
		   x_values,
		   y_values_list,
		   color_list, 
		   use_double_y_lable
		)
	if get_json:
		return map_charts_jsondata
	response = create_response(200)
	response.data = map_charts_jsondata
	
	return response.get_response()

def create_bar_chart_response(
		x_values,
		y_values_list,
		reverse=False,
		show_legend=True
	):
	"""
	创建柱状图数据的response
	@param x_values 柱状图中x轴的所有类别名称
		例如['2010-10-10', '2010-10-11', '2010-10-12']
		又例如['总订单量', '未支付订单量', '支付订单量']
	@param y_values_list 柱状图中要显示的所有类别的值序列列表
		例如：
		[{
			"name": "上个月",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "这个月",
			"values" : [60, 70, 80, 100]
		}]
	"""

	bar_charts_jsondata = myecharts.create_bar_chart_option(
		   x_values,
		   y_values_list, 
		   reverse,
		   show_legend
		)

	response = create_response(200)
	response.data = bar_charts_jsondata

	return response.get_response()

def create_table_response(column_names, data_lines, pageinfo=None, sortAttr=None):
	"""
	创建表格数据的response
	@param column_names 表格列的描述
		例如：
		[{
			"name": "date",
			"title": "日期",
		}, {
			"name": "url",
			"title": "访问地址",
		}, {
			"name": "user",
			"title": "用户",
		}]
	@param data_lines 所有行的数据
		例如：
		[
			['2014-10-17', '/app/demo', '用户1'],
			['2014-10-18', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户1'],
			['2014-10-20', '/app/demo', '用户1'],
		]
	"""

	response_data = {}
	response_data['cols'] = column_names
	response_data['lines'] = data_lines
	response_data['pageinfo'] = pageinfo
	response_data['sortAttr'] = sortAttr

	response = create_response(200)
	response.data = response_data
	
	return response.get_response()


def create_bar_timeline_response(
		timeline,
		x_values,
		y_values_list
	):
	
	"""
	创建带时间轴柱状图数据的response
	@param x_values 柱状图中x轴的所有类别名称
		例如[['2010-10-10', '2010-10-11', '2010-10-12'],['2010-10-10', '2010-10-11', '2010-10-12']]
		又例如['总订单量', '未支付订单量', '支付订单量']
	@param y_values_list 柱状图中要显示的所有类别的值序列列表
		例如：
		[[{
			"name": "上个月",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "这个月",
			"values" : [60, 70, 80, 100]
		}],[{
			"name": "上个月",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "这个月",
			"values" : [60, 70, 80, 100]
		}]]
	"""
	
	options = []
	for i in range(len(x_values)):
		bar_charts_jsondata = myecharts.create_bar_chart_option(
			   x_values[i],
			   y_values_list[i] 
			)
		options.append(bar_charts_jsondata)

	response = create_response(200)
	response.data.options = options
	response.data.timeline = timeline
	
	return response.get_response()


def create_line_timeline_chart_response(
		timeline,
		x_unit_label,
		y_unit_label,
		x_values,
		y_values_list
	):
	"""
	创建带时间轴折线图数据的response
	@param x_unit_label 折线图中x轴显示的单位名称
		例如"个"，如果不需要单位可指定为""
	@param y_unit_label 折线图中y轴显示的单位名称
		例如"个"，如果不需要单位可指定为""
	@param x_values 折线图中x轴的所有坐标点
		例如[['2010-10-10', '2010-10-11', '2010-10-12'], ['2010-10-10', '2010-10-11', '2010-10-12']]
	@param y_values_list 折线图中要显示的所有线的所有y轴的值序列
		例如：
		[[{
			"name": "iphone",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "小米",
			"values" : [60, 70, 80, 100]
		}], [{
			"name": "iphone",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "小米",
			"values" : [60, 70, 80, 100]
		}]]
	"""
	options = []
	for i in range(len(x_values)):
		map_charts_jsondata = myecharts.create_line_chart_option(
			   x_unit_label,
			   y_unit_label,
			   x_values[i],
			   y_values_list[i] 
			)
		options.append(map_charts_jsondata)
	response = create_response(200)
	response.data.options = options
	response.data.timeline = timeline
	
	return response.get_response()


def create_table_line_chart_response(table_data, line_data):
	"""
	表格的数据格式table_data
		例如：
		{
			column_names: [],
			data_lines: [],
			pageinfo: None,
			sortAttr: None
	
		}
	@param column_names 表格列的描述
		例如：
		[{
			"name": "date",
			"title": "日期",
		}, {
			"name": "url",
			"title": "访问地址",
		}, {
			"name": "user",
			"title": "用户",
		}]
	@param data_lines 所有行的数据
		例如：
		[
			['2014-10-17', '/app/demo', '用户1'],
			['2014-10-18', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户2'],
			['2014-10-19', '/app/demo', '用户1'],
			['2014-10-20', '/app/demo', '用户1'],
		]
		
		
	与之关联的折线图的数据line_data
		例如：
		{
			x_unit_label: '',
			y_unit_label: '',
			x_values: [],
			y_values_list: []
		}
	@param x_unit_label 折线图中x轴显示的单位名称
	例如"个"，如果不需要单位可指定为""
	@param y_unit_label 折线图中y轴显示的单位名称
		例如"个"，如果不需要单位可指定为""
	@param x_values 折线图中x轴的所有坐标点
		例如['2010-10-10', '2010-10-11', '2010-10-12']
	@param y_values_list 折线图中要显示的所有线的所有y轴的值序列
		例如：
		[{
			"name": "iphone",
			"values" : [50, 60, 80, 90]
		}, {
			"name" : "小米",
			"values" : [60, 70, 80, 100]
		}]
	"""

	response_table_data = {}
	response_table_data['cols'] = table_data['column_names']
	response_table_data['lines'] = table_data['data_lines']
	response_table_data['pageinfo'] = table_data['pageinfo']
	response_table_data['sortAttr'] = table_data['sortAttr']
	
	line_charts_jsondata = myecharts.create_line_chart_option(
	   line_data['x_unit_label'],
	   line_data['y_unit_label'],
	   line_data['x_values'],
	   line_data['y_values_list'] 
	)
	pic_data = {}
	pic_data['type'] = 'line'
	pic_data['data'] = line_charts_jsondata

	response = create_response(200)
	data = {}
	data['table_data'] = response_table_data
	data['pic_data'] = pic_data
	response.data = data
	
	return response.get_response()

