mui.init();

mui.ready(function(){
	mui.plusReady(function(){
		document.getElementById("show_current_version").innerHTML = "当前版本: V"+VERSION_ID;
		if(plus.storage.getItem("is_update")=='true'){
			$("#isUpdate").show();
			$('#isUpdate').on('tap',function(){
				check_new_version();
			});
			var newVersion = plus.storage.getItem("newVersion");
			document.getElementById("newVersion").innerHTML = "最新版本: V"+newVersion;
		}
	});
	//检测新版本
	function check_new_version(){
		mui.toast('正在检测新版本...');
		$.getJSON(HOST_URL + 'mobile_app/api/version/check/?version_id=' + VERSION_ID+'&callback=?',
		function(response){
			if (response.code == 200){
				if(response.is_update) {
					var btnArray = ['是','否'];
				  	mui.confirm('是否下载新版本?','版本更新',btnArray,function(e){
				  		if(e.index==0){
							var dtask = plus.downloader.createDownload( response.url, {}, function(d, status) {
								// 下载完成
								var per = parseInt((d.downloadedSize/d.totalSize)*100);
								plus.nativeUI.showWaiting("　　 正在下载...　　 \n"+per+"%...");
								if ( status == 200 ) {
									plus.runtime.install(d.filename);
									mui.toast('下载完成');
									plus.storage.setItem('is_update','flase');
								} else {
									mui.toast('下载失败!');
								}
								plus.nativeUI.closeWaiting();
							});
							dtask.start();
				  		}
				  	});
				}else{
					mui.toast('已经是最新版本');
				}
			}else{
				mui.toast('更新失败!');
			}
		});
	}

});
