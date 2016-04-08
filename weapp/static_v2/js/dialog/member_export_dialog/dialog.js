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

		$loading = $('#spin-wrapper');
		var zIndex = $loading.css('z-index');
		$loading.css('z-index', '-10000');
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
						$loading.css('z-index', zIndex);
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
		"<div class='exportProgress_msg'>0%</div>" +
		"<div id='exportProgress_bar'><div class='exportProgress_progress'></div></div>" +
		"</div>" +
		"<a id='downloadLink' class='btn fr btn-default mr20' href='#'>下载导出文件</a>";

ensureNS('W.dialog.member.ExportFileView');
W.dialog.member.ExportFileView = Backbone.View.extend({
	el: '.div_export',
	events: {
		'click #downloadLink': 'download',
	},
	
	initialize: function(options) {
		xlog('export file view initialize');
		if ($(this.el)) {
			this.$el = $(this.el);
		} else {
			this.$el = options["this"];
		}
		var _this = this.$el;
		
		this.jobId = options.jobId;
		this.url = options.url;
		this.filter_value = options.filter_value;
		this.exportLink = _this.find('.xa-export');
		if(_this.find("#exportProgress_bar").length == 0){
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
		var filter_value = this.filter_value
		W.getApi().call({
			app: 'member',
			resource: 'export_file_param',
			method: 'get',
			args: {
				filter_value: filter_value,
			},
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

		W.getApi().call({
			app: 'member',
			resource: 'export_process',
			method: 'get',
			args: {
				id: this.jobId
			},
			success: function(data) {
				var url = data["download_url"];
				console.log("url over!",url);
				window.open(url);
			},
			error: function(response) {
				var url = "/static/upload/excel/member_"+this.jobId+".xls";
				console.log("url,but push database fail!",url);
				window.open(url);
			}
			
		});
		
		
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
		//创建导出view
		this.loadingView = W.getLoadingView();
		
		this.exportFile();
		
	},

	exportFile: function() {
		//创建导出数据的view
		this.exportFileView = new W.dialog.member.ExportFileView({type:'customer', "url": this.options.url, "filter_value":this.options.filter_value});
		
		if(this.options.isAlreadyExport) {
			this.exportFileView.doExport();
		}
	},
});