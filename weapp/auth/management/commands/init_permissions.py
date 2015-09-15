# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from auth.models import Permission

PERMISSIONS = [{
	"name": u"首页",
	"code_name": u"manage_index",
	"permissions": [{
		"name": u"统计概况",
		"code_name": u"manage_index_outline"
	}, {
		"name": u"积分规则",
		"code_name": u"manage_index_integral"
	}, {
		"name": u"消息中心",
		"code_name": u"manage_index_notice"
	}]
}, {
	"name": u"商品管理",
	"code_name": u"manage_product",
	"permissions": [{
		"name": u"在售商品管理",
		"code_name": u"manage_product_onshelf"
	}, {
		"name": u"添加新商品",
		"code_name": u"manage_product_add"
	}, {
		"name": u"待售商品管理",
		"code_name": u"manage_product_offshelf"
	}, {
		"name": u"商品回收站",
		"code_name": u"manage_product_deleted"
	}, {
		"name": u"图片管理",
		"code_name": u"manage_product_image"
	}, {
		"name": u"分组管理",
		"code_name": u"manage_product_category"
	}, {
		"name": u"属性管理",
		"code_name": u"manage_product_property_and_model_property"
	}, {
		"name": u"评价管理",
		"code_name": u"manage_product_review"
	}]	
}, {
	"name": u"订单管理",
	"code_name": u"manage_order",
	"permissions": [{
		"name": u"所有订单",
		"code_name": u"manage_order_all"
	},{
		"name": u"订单设置",
		"code_name": u"manage_order_expired_time"
	},{
		"name": u"财务审核",
		"code_name": u"manage_order_audit"
	},{
		"name": u"批量发货",
		"code_name": u"manage_order_batch_delivery"
	}]
}, {
	"name": u"促销管理",
	"code_name": u"manage_promotion",
	"permissions": [{
		"name": u"促销查询",
		"code_name": u"search_promotion"
	}, {
		"name": u"限时抢购",
		"code_name": u"manage_flash_sale"
	}, {
		"name": u"买赠",
		"code_name": u"manage_premium_sale"
	}, {
	# 	"name": u"满减",
	# 	"code_name": u"manage_price_cut"
	# }, {
		"name": u"积分应用",
		"code_name": u"manage_integral_sale"
	}, {
		"name": u"优惠券",
		"code_name": u"manage_coupon"
	}, {
		"name": u"发优惠券",
		"code_name": u"manage_send_coupon"
	}]
}, {
	"name": u"会员管理",
	"code_name": u"manage_member",
	"permissions": [{
		"name": u"会员列表",
		"code_name": u"manage_member_list"
	}, {
		"name": u"会员分组",
		"code_name": u"manage_member_tag"
	}, {
		"name": u"会员等级",
		"code_name": u"manage_member_grade"
	}, {
		"name": u"推广扫码",
		"code_name": u"manage_member_qrcode"
	}]
}, {
	"name": u"数据统计",
	"code_name": u"static",
}, {
	"name": u"权限管理",
	"code_name": u"manage_auth",
	"permissions": [{
		"name": u"账号帮助",
		"code_name": u"manage_auth_help"
	}, {
		"name": u"角色管理",
		"code_name": u"manage_auth_role"
	}, {
		"name": u"员工管理",
		"code_name": u"manage_auth_account"
	}]
}, {
	"name": u"配置管理",
	"code_name": u"manage_mall_config",
	"permissions": [{
		"name": u"运费模板",
		"code_name": u"manage_postage_template"
	}, {
		"name": u"物流名称管理",
		"code_name": u"manage_express"
	}, {
		"name": u"支付方式",
		"code_name": u"manage_pay_interface"
	}, {
		"name": u"运营邮件通知",
		"code_name": u"manage_config_mail"
	}]
}]

class Command(BaseCommand):
	help = "init global navbar for all user"
	args = ''
	
	def process_permissions(self, permissions, parent_permission=None):
		parent_id = parent_permission.id if parent_permission else 0
		for permission in permissions:
			print '[create] permission %s with parent %d' % (permission['name'], parent_id)
			db_permission = Permission.objects.create(
				parent_id = parent_id,
				name = permission['name'],
				code_name = permission['code_name']
			)

			if 'permissions' in permission:
				self.process_permissions(permission['permissions'], db_permission)

	def handle(self, **options):
		permission_count = Permission.objects.all().count()
		if permission_count > 0:
			print 'Already have %d permissions, Clear it first!!!' % permission_count
			return

		self.process_permissions(PERMISSIONS)


