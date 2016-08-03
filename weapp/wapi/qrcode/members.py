# -*- coding: utf-8 -*-

from core import api_resource, paginator
from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
from wapi.decorators import param_required
from modules.member.models import *
from utils.string_util import hex_to_byte, byte_to_hex

class QrcodeMember(api_resource.ApiResource):
	"""
	二维码
	"""
	app = 'qrcode'
	resource = 'members'

	@param_required(['channel_qrcode_id'])
	def get(args):
		"""
		获取会员
		"""
		channel_qrcode_id = int(args.get('channel_qrcode_id'))
		channel_qrcode = ChannelQrcodeSettings.objects.filter(id=channel_qrcode_id)
		user_id = 0
		if channel_qrcode.count() > 0:
			user_id = channel_qrcode[0].owner_id
		userprofile = UserProfile.objects.filter(user_id=user_id)
		webapp_id = 0
		if userprofile.count() > 0:
			webapp_id = userprofile[0].webapp_id

		filter_data_args = {
			"channel_qrcode_id": channel_qrcode_id
		}

		member_name = args.get('member_name', None)
		start_date = args.get('start_date', None)
		end_date = args.get('end_date', None)
		if member_name:
			members = Member.objects.filter(webapp_id=webapp_id, username_hexstr__contains=byte_to_hex(member_name))
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids

		if start_date and end_date:
			start_time = start_date + ' 00:00:00'
			end_time = end_date + ' 23:59:59'
			members = Member.objects.filter(webapp_id=webapp_id, created_at__gte=start_time, created_at__lte=end_time)
			member_ids = []
			for member in members:
				member_ids.append(member.id)
			filter_data_args["member_id__in"] = member_ids

		channel_members = ChannelQrcodeHasMember.objects.filter(**filter_data_args).order_by('-created_at')

		#处理分页
		count_per_page = int(args.get('count_per_page', '20'))
		cur_page = int(args.get('cur_page', '1'))
		pageinfo, channel_members = paginator.paginate(channel_members, cur_page, count_per_page)
		member_ids = [member_log.member_id for member_log in channel_members]
		channel_members = Member.objects.filter(id__in=member_ids)
		members = []
		for channel_member in channel_members:
			members.append({
				"member_name": channel_member.username_for_html,
				"follow_time": channel_member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				"pay_times": channel_member.pay_times,
				'pay_money': '%.2f' % channel_member.pay_money
			})



		return {
			'items': members,
			'pageinfo': paginator.to_dict(pageinfo) if pageinfo else ''
		}
