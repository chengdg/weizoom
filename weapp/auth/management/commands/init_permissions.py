# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from auth.models import Permission

PERMISSIONS = [{
	"name": u"商品管理",
	"code_name": u"manage_product",
	"permissions": [{
		"name": u"添加新商品",
		"code_name": u"add_product"
	}, {
		"name": u"在售商品管理",
		"code_name": u"manage_onshelf_product"
	}, {
		"name": u"待售商品管理",
		"code_name": u"manage_offshelf_product"
	}, {
		"name": u"商品回收站",
		"code_name": u"manage_deleted_product"
	}, {
		"name": u"图片管理",
		"code_name": u"manage_image"
	}, {
		"name": u"分组管理",
		"code_name": u"manage_product_category"
	}, {
		"name": u"属性规格管理",
		"code_name": u"manage_product_property_and_model_property"
	}]	
}, {
	"name": u"促销管理",
	"code_name": u"manage_promotion",
	"permissions": [{
		"name": u"促销查询",
		"code_name": u"search_promition"
	}, {
		"name": u"限时抢购",
		"code_name": u"manage_flash_sale"
	}, {
		"name": u"买赠",
		"code_name": u"manage_premium_sale"
	}, {
		"name": u"满减",
		"code_name": u"manage_price_cut"
	}, {
		"name": u"优惠券",
		"code_name": u"manage_coupon"
	}, {
		"name": u"积分应用",
		"code_name": u"manage_integral_sale"
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
	}]	
}, {
	"name": u"权限管理",
	"code_name": u"manage_system_auth",
	"permissions": [{
		"name": u"账号帮助",
		"code_name": u"view_account_help"
	}, {
		"name": u"角色管理",
		"code_name": u"manage_role"
	}, {
		"name": u"员工管理",
		"code_name": u"manage_account"
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


