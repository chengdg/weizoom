#coding: utf8

from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from market_tools.tools.lottery.models import LotteryRecord, Lottery
from modules.member.models import Member
import re

activity_network_option =  {
	"title": {
		"text" : '活动跟踪',
	},
	"toolbox": {
		"show": True,
		"feature": {
			"mark": {"show": True},
			"dataView": {"show": True, "readOnly": False},
			"restore": {"show": True},
			"saveAsImage": {"show": True},
		}
	},
	"series": [
		{
			"name": '树图',
			"type": 'tree',
			"orient": 'horizontal',
			"rootLocation": {"x": 100, "y": 230},
			"nodePadding": 8,
			"layerPadding": 200,
			"hoverable": False,
			"roam": True,
			"symbolSize": 6,
			"itemStyle": {
				"normal": {
					"color": '#4883b4',
					"label": {
						"show": True,
						"position": 'right',
						"formatter": '{b}',
						"textStyle": {
							"color": '#000',
							"fontSize": 5,
						}
					},
					"lineStyle": {
						"color": '#ccc',
						"type": 'curve'
					}
				},
				"emphasis": {
					"color": '#4883b4',
					"label": {
						"show": False
					},
					"borderWidth": 0
				}
			},
			"data": [{
				"name": "冰桶挑战",
				"children": [{
					"name": "刘作虎",
					"children": [{
						"name": "周鸿祎"
					}]
				}]
			}]
		}
	]
}

def get_activity_network_chart(activity_id):
	option = activity_network_option
	return option


def __remove_emoji(name):
	"""
	去掉表情符

	举例: ```<span class="emoji emoji 1f44c"></span>```
	"""
	return re.sub(r'<span.*>.*?</span>', '', name)


def get_channel_member_network_chart(setting_id):
	option = activity_network_option
	setting = ChannelQrcodeSettings.objects.get(id=setting_id)
	member_ids = [relation.member_id for relation in \
		ChannelQrcodeHasMember.objects.filter(channel_qrcode=setting_id)]
	
	members = Member.objects.filter(id__in=member_ids)
	children = []
	for member in members:
		#channel_members.append(__build_member_basic_json(member))
		children.append({"name": __remove_emoji(member.username_for_html)})

	series = option['series']
	series[0]['data'] = [{
		"name": setting.name,
		"children": children
	}]
	return option


def get_lottery_member_network_chart(lottery_id):
	option = activity_network_option
	lottery = Lottery.objects.get(id=lottery_id)
	member_ids = [relation.member_id for relation in \
		LotteryRecord.objects.filter(lottery_id=lottery_id)]
	
	members = Member.objects.filter(id__in=member_ids)
	children = []
	for member in members:
		#channel_members.append(__build_member_basic_json(member))
		children.append({"name": __remove_emoji(member.username_for_html)})

	series = option['series']
	series[0]['data'] = [{
		"name": lottery.name,
		"children": children
	}]
	return option
