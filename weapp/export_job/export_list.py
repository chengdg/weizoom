#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib.auth.decorators import login_required
from core.jsonresponse import JsonResponse, create_response
from core import resource
from export_job.models import ExportJob
import time

class ExportGetProcess(resource.Resource):
	"""
	获取导出进度
	"""
	app = "export_job"
	resource ="export_process"
	
	@login_required
	def api_get(request):
		exportjob_id = int(request.GET.get('id', 0))
		
		exportjob = ExportJob.objects.get(id=exportjob_id)
		if exportjob.status == 1:
			response = create_response(200)
			response.data = {
				'process':100,
				'status':1,
				'download_url': exportjob.file_path,
			}
			return response.get_response()
		elif exportjob.status == 0:
			if exportjob.processed_count > 0 and exportjob.count >0:
				process = exportjob.processed_count*100/exportjob.count
			else:
				process = 0 
			timeArray = time.strptime(str(exportjob.update_at),"%Y-%m-%d %H:%M:%S",)
			timeStamp = float(time.mktime(timeArray))
			time2 = time.time()
			if time2 - timeStamp > 60:
				exportjob.status = 2
				exportjob.is_download = 1
				exportjob.save()
		else:
			notify_message = u"获取会员导出进度失败，exportjob_id:{},status:{}".format(exportjob_id, exportjob.status)
			watchdog_error(notify_message)
		response = create_response(200)
		response.data = {
			'process':process,
			'status':0}
		return response.get_response()


class ExportGetDownloadOver(resource.Resource):
	"""
	下载完后通知后台，存储到数据库
	"""
	app = "export_job"
	resource ="export_download_over"
	
	@login_required
	def api_get(request):
		exportjob_id = int(request.GET.get('id', 0))
		if exportjob_id > 0:
			try:
				ExportJob.objects.filter(id=exportjob_id).update(is_download=True)
			except:
				pass
		response = create_response(200)
		response.data={"over":exportjob_id}
		return response.get_response()



class ExportListIsDownload(resource.Resource):
	"""
	判断是否有未完成的下载
	"""
	app = "export_job"
	resource ="export_is_download"

	@login_required
	def api_get(request):
		woid = request.GET.get('woid', 0)
		type = request.GET.get('type', 0)
		
		try:
			export_jobs = ExportJob.objects.filter(woid=woid,type=type,is_download=0).order_by("-id")
			response = create_response(200)
			if export_jobs:
				response.data={
					"woid":export_jobs[0].woid,
					"status":1 if export_jobs[0].status else 0,
					"is_download":1 if export_jobs[0].is_download else 0,
					"id":export_jobs[0].id,
					"file_path":export_jobs[0].file_path,
				}
				return response.get_response()
		except:
			pass 
		response = create_response(200)
		response.data={
			"is_download":1,
			"status":1,
			}
		return response.get_response()