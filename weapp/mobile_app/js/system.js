/* This function runs once the page is loaded, but intel.xdk is not yet active */
$.ui.animateHeaders=false;
var search=document.location.search.toLowerCase().replace("?","");
$.ui.useOSThemes=true;
if(search.length>0) //Android fix has too many buggy issues on iOS - can't preview with $.os.android
{
	$.ui.useOSThemes=true;
	if(search=="win8")
		$.os.ie=true;
	$.ui.ready(function(){
		$("#afui").get(0).className=search;
	});
}

//$.ui.autoLaunch = false;
$.ui.openLinksNewTab = false;
$.ui.splitview=false;

//遮盖整个body，使得menu也不可在加载中点击
function show_menu_mask(msg){
	$.ui.showMask(msg);
	$("#content_mask").show();
}

function hide_menu_mask(){
	$.ui.hideMask();
	$("#content_mask").hide();
}

//定时刷新消息函数
var messages_auto_update_interval,push_flag;
var new_message_count = 0; //记录上次消息未读消息个数，用于判断是否提醒
function start_auto_update_messages(){
	messages_auto_update_interval = setInterval(function(){
		stop_auto_update_messages();
		$.jsonP({
			url: HOST_URL + 'mobile_app/api/messages/get_unread_count/',
			success:function(response){
//				$("#error_message").hide();
				var count = response.data.unread_count;
				if(count != 0){
					//弹出通知
					push_flag = $("#push").prop("checked");
					if(push_flag) {
						NotifyMsg.notify(count,$('#new_message_count').text());
					}
					$('#new_message_count').show().text(count);
					//如果上次消息数与本次不同，则给出提示
					if(new_message_count != count) {
						new_message_count = count;
						if (dthMobileOA.getBooleanData("sound")) {
							navigator.notification.beep(1);
						}
						if (dthMobileOA.getBooleanData("vibrator")) {
							navigator.notification.vibrate(1500);
						}
					}
				}else{
					$('#new_message_count').hide().text('');
					new_message_count = 0;
				}
				start_auto_update_messages();
			},error:function(){
				start_auto_update_messages();
			}
		});
	},message_auto_update_time);
}

//停止自动刷新消息函数
function stop_auto_update_messages(){
	clearInterval(messages_auto_update_interval);
}

//下拉刷新
//需传入jquery的css选择器规则css_selector，和刷新时的执行方法fn， 以及一个可选参数arge
function scroll_to_refresh(css_selector,fn,arge){
	var myScroller = $(css_selector).scroller({
		verticalScroll:true,
		horizontalScroll:false,
		autoEnable:true
	});
	myScroller.addPullToRefresh();
	//Here we listen for the user to pull the page down and then let go to start the pull to refresh callbacks.
	$.unbind(myScroller, 'scrollstart');
	$.bind(myScroller, 'scrollstart', function () {
		this.setRefreshContent("下拉刷新");
	});
	$.unbind(myScroller, 'refresh-trigger');
	$.bind(myScroller, "refresh-trigger", function () {
		this.setRefreshContent("释放更新");
	});
	$.unbind(myScroller, "refresh-release"); //先解除绑定以免多次刷新请求
	$.bind(myScroller, "refresh-release", function () {
		this.setRefreshContent("加载中…");
		var that = this;
		$(css_selector+' a').unbind('click');//先解绑，再改变href属性
		$(css_selector+' a').attr('href','javascript:void 0');//防止刷新时点击列表而导致2次jsonp请求从而发生冲突
		$(css_selector+' .init_li').unbind('click');//阻止刷新页面时仍然请求加载更多
		setTimeout(function () {
			that.hideRefresh();
		}, 1000);
		fn(arge);
		return false; //tells it to not auto-cancel the refresh
	});
	$.unbind(myScroller, 'refresh-cancel');
	$.bind(myScroller, "refresh-cancel", function () {
		myScroller.canInfinite = false;
		this.setRefreshContent("取消刷新");
	});
	return myScroller;
}

//列表末尾加载更多的按钮
//params是一个对象，格式为
//{
//	'url' : ..., 请求的地址，但page暂不需要给数值，也会作为参数传进来
//	'css_id' : ..., id，不能包含#
//	'fn' : ...   该函数在jsonp的success中执行，所以需要一个参数接收response
//	'page' : ... 自定义的当前页的变量名
//}
var loadNextPageBtn = (function(){
	var startLoading = function(obj){
		$('#'+obj.el_id+' b').text('加载中....');
		$.jsonP({
			url : obj.url+getCurrPage(obj),//此处加上请求的页数
			success : function(response){
				obj.hasNext = obj.innerFn(response);//执行传入的函数，将返回状态赋值给属性
				finishLoding(obj);
			},
			error : function(){
				alert("网络或服务器错误，请稍后再试");
				finishLoding(obj);
			}
		});
	};
	var finishLoding = function(obj){
		removeBtn(obj);
		if(obj.hasNext ){
			obj.appendToTail();
		}
	};
	var removeBtn = function(obj){
		$('#'+obj.el_id).remove();
	};
	var getCurrPage = function(obj){
		return window[obj.page];
	};
	var appendElement = function(obj) {
		var el;
		var elId = obj.el_id;
		var css_id = obj.el_id.substring(0,obj.el_id.lastIndexOf('_btn'));
		if(elId.indexOf('message') != -1){
			// if(message_count_per_page * (message_list_curr_page-1) >= max_message_list_loaded_count){
			if((message_list_curr_page-1) >= max_message_list_loaded_count){
				el = "<li id='"+elId+"' style='border:0px !important;'><p class='init_li'>更多消息请见PC端</p></li>";
			}else{
				el = "<li id='"+elId+"' style='border:0px !important;'><b class='init_li'>点击加载更多</b></li>";
			}
			$('#'+css_id).append(el);
		}else if(elId.indexOf('order') != -1){
			// if(order_count_per_page * (order_count_curr_page-1) >= max_order_list_loaded_count){
			if((order_count_curr_page-1) >= max_order_list_loaded_count){
				el = "<ul style='list-style: none;'><li id='"+elId+"'><p class='init_li'>更多订单请见PC端</p></li></ul>";
			}else{
				el = "<ul style='list-style: none;'><li id='"+elId+"'><b class='init_li'>点击加载更多</b></li></ul>";
			}
			$('#'+css_id).append(el);
		}
	};
	return function(params){
		this.hasNext = true;
		this.url = params.url;
		this.el_id = params.css_id+"_btn";
		this.innerFn = params.fn;
		this.page = params.page_name;
		this.appendToTail = function(){
			appendElement(this);
			var that = this;
			$('#'+this.el_id+' b').one('click',function(){
				startLoading(that);
			});
		};
	};
})();

//每次进入一个新的页面都初始化下Header，
//可以包括后退按钮、退出按钮、title以及消息中回复按钮的显示与隐藏
function initHeader(){
	//隐藏后退按钮
	$('#backButton').hide();
	//隐藏消息回复框
	ReplyBox.clearBox();
	//隐藏订单搜索
	$('#search_order').hide();
	//显示菜单按钮
	$('#menubadge').show();
	//隐藏统计菜单
	$('#meun_statistic').hide();
	//TODO 其他的初始设置
}

//定义本地存储的函数和存取对应数据的函数
LocalMobelInfo = function() {
};
LocalMobelInfo.prototype.putStringData = function(key, value) {
	localStorage.setItem(key, value + "");
};
LocalMobelInfo.prototype.putBooleanData = function(key, value) {
	localStorage.setItem(key, value + "");
};
LocalMobelInfo.prototype.putIntData = function(key, value) {
	localStorage.setItem(key, value + "");
};
LocalMobelInfo.prototype.updateUser = function(name, password) {
	localStorage.setItem("WZ_USERNAME", name + "");
	localStorage.setItem("WZ_PASSWORD", password + "");
}
LocalMobelInfo.prototype.updateManager = function(name, password) {
	localStorage.setItem("WZ_USERNAME", name + "_manager");
	localStorage.setItem("WZ_PASSWORD", password + "");
}
LocalMobelInfo.prototype.getBooleanData = function(key) {
	return "true" == localStorage.getItem(key) ? true : false;
};
LocalMobelInfo.prototype.getStringData = function(key) {
	return localStorage.getItem(key);
};
LocalMobelInfo.prototype.getIntData = function(key) {
	if (!isNullOrUndefined(localStorage.getItem(key))) {
		return parseInt(localStorage.getItem(key));
	} else {
		return 0;
	}
};
LocalMobelInfo.prototype.getUserName = function() {
	return localStorage.getItem("WZ_USERNAME");
};
LocalMobelInfo.prototype.getUserPassword = function() {
	return localStorage.getItem("WZ_PASSWORD");
};

// 错误提示定时消失
var hideErrorTimeout;
//time:如果time为-1，则提示不会隐藏，如果为undefined，则按默认5秒后隐藏
function showErrorMessage(msg,time){
	clearTimeout(hideErrorTimeout);
	if(!msg){
		msg = '网络或服务器错误,请稍后再试 ';
	}
	$("#error_message span").html(msg);
	$("#error_message").show();
	if(time != -1){
		hideErrorTimeout = setTimeout(function() {
			$("#error_message").hide();
		}, time?time:5000);
	}
}

function eventBackButton(){
	var slide = $("#slideView");
	if(slide.css("display") != "none"){
		slide.css("display","none");
		slide.html("");
	}else{
		var hash_str = window.location.hash;
		switch(hash_str) {
			case "#message_his":
				$("#backButton").trigger("click");
				break;
			case "#order_co":
				$("#backButton").trigger("click");
				break;
			default :
				showErrorMessage('再按一次退出');
				document.removeEventListener("backbutton", eventBackButton, false); // 注销返回键
				document.addEventListener("backbutton", exitApp, false);//绑定退出事件
				// 3秒后重新注册
				var intervalID = window.setInterval(function() {
					window.clearInterval(intervalID);
					document.removeEventListener("backbutton", exitApp, false); // 注销返回键
					document.addEventListener("backbutton", eventBackButton, false); // 再次绑定返回键
				}, 3000);
		}
	}
}

function exitApp(){
	logoutFunction();
	navigator.app.exitApp();
}

//记录浏览位置
function saveLastVisitPosition(el_id){
	var messageScroller = $(el_id).scroller();
	var curScrollTop = messageScroller.scrollTop;
	$(el_id).attr('scrollTop', curScrollTop);
}

function trim(str){
	str = str.replace(/^(\s|\u00A0)+/,'');
	for(var i=str.length-1; i>=0; i--){
		if(/\S/.test(str.charAt(i))){
			str = str.substring(0, i+1);
			break;
		}
	}
	return str;
}

//设置Menubadge Button的点击事件
function aMenubadgeClickEvent(){
	$('#menubadge').bind('click',function(){
		$("span.min-badge").hide();
	});
}

//检查更新
function login_check_new() {
	$("#show_current_version").text("当前版本: V"+VERSION_ID);
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/version/check/?version_id=' + VERSION_ID,
		success: function(response){
			if (response.is_update) {
				$("span.min-badge").show();
				aMenubadgeClickEvent();
				$('#check_new').html("<span>新版更新(V"+response.version+")&nbsp;<img src='img/newIcon.gif'></span>");
				$('#check_new').unbind('click');
				$('#check_new').bind('click', check_new_version);
			}else{
				$("#check_new").remove();
			}
		},error:function(){
			$('#check_new').html('<span>检查更新(当前&nbsp;V'+VERSION_ID+')</span>');
			$('#check_new').unbind('click');
			$('#check_new').bind('click', check_new_version);
		}
	});
}

//检测新版本
function check_new_version(){
	$.ui.showMask('正在检测新版本...');
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/version/check/?version_id=' + VERSION_ID,
		success: function(response){
			$.ui.hideMask();
			if(response.is_update) {
				$.ui.popup({
					title:"版本更新",
					message:"是否下载新版本?",
					cancelText:"取消",
					cancelCallback: function(){
						$('#check_new').html("<span>新版更新(V"+response.version+")&nbsp;<img src='img/newIcon.gif'></span>");
					},
					doneText:"确定",
					doneCallback: function(){
						downloadNewVersionAPK(response.url);
					},
					cancelOnly:false
				});
			}else{
				$.ui.popup({
					title:"版本更新",
					message:"已经是最新版本",
					cancelText:"确定",
					cancelOnly:true
				});
			}

		},error:function(){
			$.ui.hideMask();
			console.log("更新失败!");
		}
	});
	setTimeout($.ui.hideMask(),5000);
}


//下载新的apk文件
function downloadNewVersionAPK(url) {
	var str_arr = url.split("/");
	var filename = str_arr[str_arr.length - 1];
	var fileTransfer = new FileTransfer();
	//显示下载进度
	fileTransfer.onprogress = function(progressEvent) {
		if (progressEvent.lengthComputable) {
			var perc = Math.floor(progressEvent.loaded / progressEvent.total * 100);
			$.ui.showMask('正在下载 '+perc+'% ...');
		} else {
			loadingStatus.increment();
			$.ui.hideMask();
		}
	};
	//下载文件
	var uri = encodeURI(url);
	var filePath = "/sdcard/" + filename;
	fileTransfer.download(
		uri,
		filePath,
		function(entry) {
			$.ui.hideMask();
			//执行apk
			promptForUpdateAndroid(entry);
		},
		function(error) {
			$.ui.hideMask();
			alert("下载失败!");
		},
		false,
		{
		}
	);
}

//执行apk文件函数
function promptForUpdateAndroid(entry) {
	window.plugins.webintent.startActivity({
			action: window.plugins.webintent.ACTION_VIEW,
			url: entry.toURL(),
			type: 'application/vnd.android.package-archive'
		},
		function () {
		},
		function () {
			alert('Failed to open URL via Android Intent.');
			console.log("Failed to open URL via Android Intent. URL: " + entry.fullPath);
		}
	);
}

