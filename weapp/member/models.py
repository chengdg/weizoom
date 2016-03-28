#coding:utf-8


from django.db import models
from django.contrib.auth.models import User

#
#
#
#
#
#status:0,1 0未完成，1完成
#type:0,1 0会员，1订单
#
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
	param = models.CharField(max_length=256)
	file_path = models.CharField(max_length=256)
	create_time = models.DateTimeField(verbose_name='创建时间')

	class Meta(object):
		db_table = 'export_job'