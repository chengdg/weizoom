/**
 * 用于显示导出数据进度的view
 *
 */
ensureNS('W.dialog.member.ExportFileJobView');
W.dialog.member.ExportFileJobView = Backbone.Model.extend({
	initialize: function(options) {
		this.jobId = options; 
		this.saveUrl = '/member/export/file_param/';
		this.statusUrl = '/member/export/process/?exportjob_id=' + this.jobId;
		this.updateProgressEvent = 'updateProgress';
		this.finishEvent = 'finish';
	},

	url: function() {
		return this.statusUrl;
	},

	checkStatus: function() {
		var count = 1;
		var statusUrl = this.statusUrl;
		var job = this;
		var jobId = this.jobId;

		var inner_func = function() {
			var thisFunction = arguments.callee;
			W.getApi().call({
				app: 'member',
				resource: 'export_process',
				method: 'get',
				args: {
					id: jobId
				},
				success: function(data) {
					var process = Number(data["process"]);
					
					var status = Number(data["status"]);
					if (status === 1) {
						process = 0;
						download_url = data["download_url"];
						job.trigger(job.finishEvent);
						job.trigger(job.updateProgressEvent, process);
						xlog('finish');
					}
					else {
						job.trigger(job.updateProgressEvent, process);
						setTimeout(thisFunction, 1000);
					}
				},
				error: function(response) {
					console.log("get export process fail!");
				}
			});
		};

		return inner_func;
	},

	startMonitorStatus: function() {
		setTimeout(this.checkStatus(), 1000);
	}
});

EXPORT_PGOGRESS_TMPL = "<div id='exportProgress'>" +
		"<div class='exportProgress_msg'></div>" +
		"<div id='exportProgress_bar'><div class='exportProgress_progress'></div></div>" +
		"</div>" +
		"<a id='downloadLink' class='btn fr' href='#'><i class='icon-arrow-down'></i>下载导出文件</a>";

ensureNS('W.dialog.member.ExportFileView');
W.dialog.member.ExportFileView = Backbone.View.extend({
	el: '.div_export',
	events: {
		'click #downloadLink': 'download',
		'click #export_data_file': 'doExport'
	},
	
	initialize: function(options) {
		xlog('export file view initialize');
		if ($(this.el)) {
			this.$el = $(this.el);
		} else {
			this.$el = options["this"];
		}
		// this.$el = options["this"]
		var _this = this.$el;
		
		this.jobId = options.jobId;
		this.url = options.url;

		this.exportLink = _this.find('.xa-export');
		if(_this.find("#exportProgress_bar").length == 0){
			// alert(111)
			_this.append(EXPORT_PGOGRESS_TMPL);
		}
		this.progressDiv = _this.find('#exportProgress');
		this.progressMsg = _this.find('.exportProgress_msg');
		this.progressBar = _this.find('.exportProgress_progress');
		this.downloadLink = _this.find('#downloadLink');
	},

	doExport: function(event) {
		var view = this;
		this.exportLink.hide();
		this.progressDiv.show();
		this.downloadLink.hide();
		var url = this.url;

		W.getApi().call({
			app: 'member',
			resource: 'export_file_param',
			method: 'get',
			success: function(data) {
				view.jobId = data["exportjob_id"];
				view.job = new W.dialog.member.ExportFileJobView(view.jobId);
				view.job.bind(view.job.updateProgressEvent, view.updateProgress, view);
				view.job.bind(view.job.finishEvent, view.finish, view);
				view.job.startMonitorStatus();
			},
			error: function(response) {
				console.log("export file param fail!");
			}
		});
		// return false;
	},
	
	doExportAfterApi: function() {
		var view = this;
		this.exportLink.hide();
		this.progressDiv.show();
		this.downloadLink.hide();
		view.job = new W.dialog.member.ExportFileJobView(view.jobId);
		view.job.bind(view.job.updateProgressEvent, view.updateProgress, view);
		view.job.bind(view.job.finishEvent, view.finish, view);
		view.job.startMonitorStatus();
	},

	updateProgress: function(process) {
		xlog('update to ' + process);
		this.progressBar.css('width', process+'px');
		this.progressMsg.text(process+'%');
	},

	finish: function() {
		this.exportLink.hide();
		this.progressDiv.hide();
		this.downloadLink.show();
	},

	download: function(event) {
		this.progressDiv.hide();
		this.downloadLink.hide();
		this.exportLink.show();

		var url = "http://weappstatic.b0.upaiyun.com/upload/excel/member_"+this.jobId+".xls"
		window.open(url)
		var download_url = '/member/export/download_over/?id='+this.jobId;
		W.getApi().call({
			app: 'member',
			resource: 'export_download_over',
			method: 'get',
			args: {
				id: this.jobId
			},
			success: function(data) {
				console.log("download over!");
			},
			error: function(response) {
				console.log("download over,but push database fail!");
			}
		});
		event.stopPropagation();
		event.preventDefault();
	}
});

W.CustomersView = Backbone.View.extend({
	el: '.panel-body',

	initialize: function(options) {
		this.options = options;
		this.$el = $(this.el);
		// this.collection = this.getCollection();
		//创建导出view
		this.loadingView = W.getLoadingView();
		
		this.exportFile();
		
	},

	exportFile: function() {
		//创建导出数据的view
		this.exportFileView = new W.dialog.member.ExportFileView({type:'customer', "url": this.options.url});
		
		if(this.options.isAlreadyExport) {
			this.exportFileView.doExport();
		}
	},
});