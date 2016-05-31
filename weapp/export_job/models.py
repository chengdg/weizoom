# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
#status: 0未完成,1完成,2失败
#type: 0会员,1所有订单 2商品评价导出 3财务审核
#########################################################################
# ExportJob: 导出任务
#########################################################################
class ExportJob(models.Model):
	woid = models.IntegerField(max_length=256)
	type = models.IntegerField(default=0)
	status = models.BooleanField(default=False)
	processed_count = models.IntegerField(max_length=256)
	count = models.IntegerField(max_length=256)
	is_download = models.BooleanField(default=False, verbose_name='是否下载')
	param = models.CharField(max_length=1024)
	file_path = models.CharField(max_length=256)
	update_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)
	created_at = models.DateTimeField(verbose_name='创建时间')

	class Meta(object):
		db_table = 'export_job'