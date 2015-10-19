# # -*- coding: utf-8 -*-
# #duhao 20151019注释
# import os
# import subprocess

# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand, CommandError
# from django.conf import settings

# from auth.models import Permission

# PERMISSIONS = [{
# 	"name": u"首页",
# 	"code_name": u"manage_index",
# 	"permissions": [{
# 		"name": u"统计概况",
# 		"code_name": u"manage_index_outline"
# 	}, {
# 		"name": u"积分规则",
# 		"code_name": u"manage_index_integral"
# 	}, {
# 		"name": u"消息中心",
# 		"code_name": u"manage_index_notice"
# 	}, {
# 		"name": u"店铺装修",
# 		"code_name": u"manage_wepage"
# 	}, {
# 		"name": u"店铺导航",
# 		"code_name": u"manage_wepage_navbar"
# 	}]
# }, {
# 	"name": u"商品管理",
# 	"code_name": u"manage_product",
# 	"permissions": [{
# 		"name": u"在售商品管理",
# 		"code_name": u"manage_product_onshelf"
# 	}, {
# 		"name": u"添加新商品",
# 		"code_name": u"manage_product_add"
# 	}, {
# 		"name": u"待售商品管理",
# 		"code_name": u"manage_product_offshelf"
# 	}, {
# 		"name": u"图片管理",
# 		"code_name": u"manage_product_image"
# 	}, {
# 		"name": u"分组管理",
# 		"code_name": u"manage_product_category"
# 	}, {
# 		"name": u"属性管理",
# 		"code_name": u"manage_product_property_and_model_property"
# 	}, {
# 		"name": u"评价管理",
# 		"code_name": u"manage_product_review"
# 	}]	
# }, {
# 	"name": u"订单管理",
# 	"code_name": u"manage_order",
# 	"permissions": [{
# 		"name": u"所有订单",
# 		"code_name": u"manage_order_all"
# 	},{
# 		"name": u"订单设置",
# 		"code_name": u"manage_order_expired_time"
# 	},{
# 		"name": u"财务审核",
# 		"code_name": u"manage_order_audit"
# 	},{
# 		"name": u"批量发货",
# 		"code_name": u"manage_order_batch_delivery"
# 	}]
# }, {
# 	"name": u"应用和营销",
# 	"code_name": u"manage_promotion_all",
# 	"permissions": [{
# 		"name": u"促销管理",
# 		"code_name": u"manage_promotion"
# 	}, {
# 		"name": u"百宝箱",
# 		"code_name": u"manage_apps"
# 	}]
# }, {
# 	"name": u"会员管理",
# 	"code_name": u"manage_member",
# 	"permissions": [{
# 		"name": u"会员列表",
# 		"code_name": u"manage_member_list"
# 	}, {
# 		"name": u"会员分组",
# 		"code_name": u"manage_member_tag"
# 	}, {
# 		"name": u"会员等级",
# 		"code_name": u"manage_member_grade"
# 	}, {
# 		"name": u"推广扫码",
# 		"code_name": u"manage_member_qrcode"
# 	}]
# }, {
# 	"name": u"数据罗盘",
# 	"code_name": u"stats",
# 	"permissions": [{
# 		"name": u"经营报告",
# 		"code_name": u"manage_summary"
# 	}, {
# 		"name": u"销售分析",
# 		"code_name": u"order_summary"
# 	}, {
# 		"name": u"会员分析",
# 		"code_name": u"member_summary"
# 	}]
# }, {
# 	"name": u"配置",
# 	"code_name": u"config",
# 	"permissions": [{
# 		"name": u"运费模板",
# 		"code_name": u"manage_postage_template"
# 	}, {
# 		"name": u"物流名称管理",
# 		"code_name": u"manage_express"
# 	}, {
# 		"name": u"支付方式",
# 		"code_name": u"manage_pay_interface"
# 	}, {
# 		"name": u"运营邮件通知",
# 		"code_name": u"manage_config_mail"
# 	}, {
# 		"name": u"供货商",
# 		"code_name": u"manage_supplier"
# 	}]
# }, {
# 	"name": u"大数据挖掘",
# 	"code_name": u"big_data"
# }]

# class Command(BaseCommand):
# 	help = "init global navbar for all user"
# 	args = ''
	
# 	def process_permissions(self, permissions, parent_permission=None):
# 		parent_id = parent_permission.id if parent_permission else 0
# 		for permission in permissions:
# 			print '[create] permission %s with parent %d' % (permission['name'], parent_id)
# 			db_permission = Permission.objects.create(
# 				parent_id = parent_id,
# 				name = permission['name'],
# 				code_name = permission['code_name']
# 			)

# 			if 'permissions' in permission:
# 				self.process_permissions(permission['permissions'], db_permission)

# 	def handle(self, **options):
# 		permission_count = Permission.objects.all().count()
# 		if permission_count > 0:
# 			print 'Already have %d permissions, Clear it first!!!' % permission_count
# 			return

# 		self.process_permissions(PERMISSIONS)


