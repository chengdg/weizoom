# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta

from ofc import Chart

colours = ["#FFB300", "#0379C8", "#8F032C", "#2BF34B", "#8909F5", "#D75F22", "#0379C8", "#8F032C", "#2BF34B", "#8909F5", "#D75F22"]
empty_data_colours = ['#8F8F8F',]
chart_color = {
		u'日订单量' : '#0099FF',
		u'日出货量' : '#993300',
		u'来自商城' : '#669900',
		u'来自微信' : '#6633FF',
		u'录音数' : '#00CCFF',
		u'收听数' : '#CC9900',
		u'日总金额': '#FF6600'
	}
y_value_lambda = lambda item : item['y']
#===============================================================================
# create_line_chart : 创建ocf中的line char
#===============================================================================
def create_line_chart(infos, display_today_data=False):
	y_min = 9999999
	y_max = 0
	#遍历values，创建多条line
	lines = []
	index = 0
	type = 'area' if len(infos['values']) == 1 else 'line'
	for line_info in infos['values']:
		line = Chart()
		line.type = type
		line.fill = "#FFE4A1"
		line.fill_alpha = 0.4
		line.width = 3
		line.text = line_info['title']
		line.colour = colours[index]
		#line.colour = "#FFB300"
		line.font_size = 10
		line.dot_style =	{
									"type": "hollow-dot",
									"dot-size": 4,
									"halo-size": 2,
								}
		line.on_show = {"type":"pop-up","cascade":1,"delay":0.5}
		
		line.values = line_info['values']
		lines.append(line)
		index += 1
		
		#确定chart中y轴的值域
		#line.values中的元素为{'y': 68L, 'x': 8, 'on-click': "..."}
		#所以得到max, min元素后，需要抽取出y进行比较
		if len(line.values) != 0:
			max_value = max(line.values, key=y_value_lambda)['y']
			if max_value > y_max:
				y_max = max_value
			
			min_value = min(line.values, key=y_value_lambda)['y']
			if min_value < y_min:
				y_min = min_value
	
	if len(lines) == 0:
		y_min = 0
		y_max = 100

	#获取用于横轴显示的文本
	x_labels = None
	x_labels_step = 2
	total_days = infos['date_info']['days']
	low_date = infos['date_info']['low_date']
	if 'x_labels' in infos:
		x_labels = infos['x_labels']
	else:
		x_labels = []
		for days in range(0, total_days):
			d = low_date + timedelta(days=days)
			x_labels.append(d.strftime("%m.%d"))
		if total_days >= 20:
			x_labels_step = total_days/10

	#如果用户传入了cur_date，则表示需要高亮今天的数据点
	if 'highlight_date' in infos['date_info']:
		highlight_date = infos['date_info']['highlight_date']
		highlight_date_index = (highlight_date - low_date).days
		for line in lines:
			for dot in line.values:
				if dot['x'] == highlight_date_index:
					dot['type'] = 'star'
					dot['colour'] = '#FF0000'
					dot['dot-size'] = 7

	#如果包含了“今天”的数据，则将该数据点删除
	if not display_today_data:
		today = datetime.today().date()
		today_index = (today - low_date).days
		for line in lines:
			dot_index = 0
			for dot in line.values:
				if dot['x'] != today_index:
					dot_index += 1
				else:
					line.values[dot_index] = None

	# Create chart object
	chart = Chart()
	chart.title.text = infos['title']
	chart.y_axis.colour = "#53B0E9"
	if y_max <= 100:
		chart.y_axis.min = int(y_min/10)*10
		chart.y_axis.max = int(y_max/10+1)*10
	elif y_min > 1000:
		chart.y_axis.min = int(y_min/1000)*1000
		chart.y_axis.max = int(y_max/1000+1)*1000
	else:
		chart.y_axis.min = int(y_min/100)*100
		chart.y_axis.max = int(y_max/100+1)*100

	#防止最低点与x轴重合
	if chart.y_axis.min == y_min:
		if chart.y_axis.min < 10:
			if chart.y_axis.min != 0:
				chart.y_axis.min -= 1
		else:
			chart.y_axis.min -= 10
			
	chart.y_axis.steps = int((chart.y_axis.max - chart.y_axis.min)/10)
	#如果max是13，则step保持1，如果max是16，则step变为2，以获得最佳显示效果
	if chart.y_axis.max % 10 > 5:
		chart.y_axis.steps += 1
	chart.y_axis.grid_colour = "#D5ECFA"
	
	chart.x_axis.colour = "#53B0E9"
	chart.x_axis.min = 0
	if total_days == 1:
		chart.x_axis.max = 1
	else:
		chart.x_axis.max = total_days - 1
	
	chart.x_axis.steps = 1
	chart.x_axis.grid_colour = "#D5ECFA"
#	chart.x_axis.labels.rotate = -30
	chart.x_axis.labels.labels = x_labels
	chart.x_axis.labels.steps = x_labels_step
	chart.x_legend.text = "日期"
	chart.x_legend.style = "{font-size: 12px; color: #778877;}"
	
	chart.bg_colour = "#FFFFFF"
	chart.tooltip.shadow = True
	chart.tooltip.stroke = 5

	# Add lines data to chart object
	chart.elements = lines
	
	# create json String
	return chart.create()

#===============================================================================
# create_line_chart : 创建ocf中的line char
#===============================================================================
def create_wine_line_chart(infos, display_today_data=False):
	y_min = 0
	y_max = 0
	#遍历values，创建多条line
	lines = []
	index = 0
	type = 'area' if len(infos['values']) == 1 else 'line'
	for line_info in infos['values']:
		line = Chart()
		line.type = type
		line.fill = "#FFE4A1"
		line.fill_alpha = 0.4
		line.width = 3
		line.text = line_info['title']
		line.colour = chart_color[line_info['title']]
		#line.colour = "#FFB300"
		line.font_size = 10
		line.dot_style =	{
									"type": "hollow-dot",
									"dot-size": 4,
									"halo-size": 2,
								}
		line.on_show = {"type":"pop-up","cascade":1,"delay":0.5}
		
		line.values = line_info['values']
		lines.append(line)
		index += 1
		
		#确定chart中y轴的值域
		#line.values中的元素为{'y': 68L, 'x': 8, 'on-click': "..."}

		#所以得到max, min元素后，需要抽取出y进行比较
		if len(line.values) != 0:
			max_value = max(line.values, key=y_value_lambda)['y']
			if max_value > y_max:
				y_max = max_value
			
			min_value = min(line.values, key=y_value_lambda)['y']
			if min_value < y_min:
				y_min = min_value
	
	if len(lines) == 0:
		y_min = 0
		y_max = 100

	#获取用于横轴显示的文本
	x_labels = None
	x_labels_step = 1
	total_days = infos['date_info']['days']
	low_date = infos['date_info']['low_date']
	if 'x_labels' in infos:
		x_labels = infos['x_labels']
	else:
		x_labels = []
		for days in range(0, total_days-1):
			d = low_date + timedelta(days=days)
			x_labels.append(d.strftime("%m.%d"))
		

	#如果用户传入了cur_date，则表示需要高亮今天的数据点
	if 'highlight_date' in infos['date_info']:
		highlight_date = infos['date_info']['highlight_date']
		highlight_date_index = (highlight_date - low_date).days
		for line in lines:
			for dot in line.values:
				if dot['x'] == highlight_date_index:
					dot['type'] = 'star'
					dot['colour'] = '#FF0000'
					dot['dot-size'] = 7

	#如果包含了“今天”的数据，则将该数据点删除
	if not display_today_data:
		today = datetime.today().date()
		today_index = (today - low_date).days
		for line in lines:
			dot_index = 0
			for dot in line.values:
				if dot['x'] != today_index:
					dot_index += 1
				else:
					line.values[dot_index] = None

	# Create chart object
	chart = Chart()
	chart.title.text = infos['title']
	chart.y_axis.colour = "#53B0E9"
	if y_max <= 100:
		chart.y_axis.min = int(y_min/10)*10
		chart.y_axis.max = int(y_max/10+1)*10
	elif y_min > 1000:
		chart.y_axis.min = int(y_min/1000)*1000
		chart.y_axis.max = int(y_max/1000+1)*1000
	else:
		chart.y_axis.min = int(y_min/100)*100
		chart.y_axis.max = int(y_max/100+1)*100

	#防止最低点与x轴重合
	if chart.y_axis.min == y_min:
		if chart.y_axis.min < 10:
			if chart.y_axis.min != 0:
				chart.y_axis.min -= 1
		else:
			chart.y_axis.min -= 10
	chart.y_axis.max = int(infos['max_value']*1.2)+1
	chart.y_axis.steps = int((chart.y_axis.max - chart.y_axis.min)/10)
	#如果max是13，则step保持1，如果max是16，则step变为2，以获得最佳显示效果
	if chart.y_axis.max % 10 > 5:
		chart.y_axis.steps += 1
	chart.y_axis.grid_colour = "#D5ECFA"
	
	chart.x_axis.colour = "#53B0E9"
	chart.x_axis.min = 0
	
	chart.x_axis.max = total_days - 1
	
	chart.x_axis.steps = 1
	chart.x_axis.grid_colour = "#D5ECFA"
#	chart.x_axis.labels.rotate = -30
	chart.x_axis.labels.labels = x_labels
	chart.x_axis.labels.steps = 1
	chart.x_legend.text = "日期"
	chart.x_legend.style = "{font-size: 12px; color: #778877;}"
	
	chart.bg_colour = "#FFFFFF"
	chart.tooltip.shadow = True
	chart.tooltip.stroke = 5

	# Add lines data to chart object
	chart.elements = lines
	
	# create json String
	return chart.create()


def process_x_labels(labels):
	proper_nouns = ['http', 'com', 'cn', 'net', 'www', 'ftp', 'bbs', 'blog']
	new_labels = []
	for label in labels:
		items = label.split('.')
		count = len(items)
		if count > 2:
			x_label = items[1]
		else:
			x_label = items[0]

		if x_label in proper_nouns:
			x_label = [item for item in items if item not in proper_nouns][0]

		new_labels.append(x_label)
	return new_labels
			
#===============================================================================
# create_bar_chart : 创建ocf中的bar chart
#===============================================================================
def create_bar_chart(infos):
	bar_chart = Chart()
	bar_chart.type = 'bar_glass'
	bar_chart.on_show = {"type":"grow-up", "cascade":1, "delay":1}
	bar_chart.text = infos['bar_title']
	bar_chart.colour = "#FFB300"
	bar_chart.values = infos['values']
	
	chart = Chart()
	chart.title.text = infos['title']
	chart.y_axis.colour = "#53B0E9"
	chart.y_axis.min = 0
	#news_counts[0]包含着最大的news count值
	#chart.y_axis.max = int(news_counts[0]['top']*1.2)+1

	chart.y_axis.max = int(infos['max_value']*1.2)+1
	chart.y_axis.steps = int((chart.y_axis.max - chart.y_axis.min)/10)
	#如果max是13，则step保持1，如果max是16，则step变为2，以获得最佳显示效果
	if chart.y_axis.max % 10 > 5:
		chart.y_axis.steps += 1
	chart.y_axis.grid_colour = "#D5ECFA"
	
	chart.x_axis.colour = "#53B0E9"
	chart.x_axis.min = 0	
	chart.x_axis.steps = 1
	chart.x_axis.grid_colour = "#D5ECFA"

	#获取用于横轴显示的文本
	x_labels = []
	x_labels_step = 1
	total_days = infos['date_info']['days']
	low_date = infos['date_info']['low_date']
	for days in range(0, total_days-1):
		d = low_date + timedelta(days=days)
		x_labels.append(d.strftime("%m.%d"))
	
	chart.x_axis.labels.labels = x_labels
	chart.x_axis.max = len(x_labels)
	#chart.x_axis.labels.labels = infos['x_labels']
	chart.x_axis.labels.steps = 1
	#chart.x_axis.labels.rotate = 30
	#chart.x_axis.labels.size = 14
	#chart.x_axis.labels.colour = '#0000FF'
	chart.x_legend.text = infos['x_legend_text']
	chart.x_legend.style = "{font-size: 12px; color: #778877;}"
	#chart.x_axis.labels.visible_steps = 1	
	#chart.bg_colour = "#E8F3FA"
	chart.bg_colour = "#FFFFFF"
	chart.tooltip.shadow = True
	chart.tooltip.stroke = 5
	
	# Add pie data to chart object
	#chart.elements = [bar_chart]
	
	elements = []
	
	cycle_count = 0
	for trend_values in infos['values']:
		if trend_values['values']:
			bar_chart = Chart()
			bar_chart.type = 'bar_glass'
			bar_chart.on_show = {"type":"grow-up", "cascade":1, "delay":1}
			bar_chart.text = trend_values['title']
			bar_chart.colour = chart_color[trend_values['title']]
			day_values = []
			for value in trend_values['values']:
				day_values.append(value['y'])
			bar_chart.values = day_values

			elements.append(bar_chart)
	chart.elements = elements
	return chart.create()


#===============================================================================
# create_pie_chart : 创建ocf中的pie chart
#===============================================================================
def create_pie_chart(infos):
	#create pie chart
	is_empty_data = False
	if len(infos['values']) == 1 and infos['values'][0]['label'] == u'暂无数据':
		is_empty_data = True
	
	try:
		if infos['type'] == 'proportion_only':
			proportion_only = True
		else:
			proportion_only = False
	except:
		proportion_only = False

	pie_chart = Chart()
	pie_chart.type = "pie"
	pie_chart.start_angle = 35
	pie_chart.gradient_fill = True
	if is_empty_data:
		pie_chart.tip = '暂无数据'
	else:
		if proportion_only:
			pie_chart.tip = "#percent#"
		else:
			pie_chart.tip = "#val# of #total#<br>#percent# of 100%"
	pie_chart.animate = [{ "type": "fade" }, { "type": "bounce", "distance": 5 }]
	pie_chart.values = infos['values']
	if is_empty_data:
		pie_chart.colours = empty_data_colours
	else:
		pie_chart.colours = colours[:len(infos['values'])]#infos['colours']
	
	#create chart object
	chart = Chart()
	chart.title.text = infos['title']
	chart.title.style = "margin: 5px 0px 20px 0px; font-size: 12px;"
	#chart.bg_colour = "#E8F3FA"
	chart.bg_colour = "#FFFFFF"
	chart.tooltip.shadow = True
	chart.tooltip.stroke = 5
	
	# Add line data to chart object
	chart.elements = [pie_chart]

	# Create chart json string
	return chart.create()