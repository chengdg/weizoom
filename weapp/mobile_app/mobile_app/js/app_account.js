
// 登出
function logoutFunction(){
		$.getJSON( HOST_URL +'mobile_app/api/logout/get/?callback=?',
			function(data,status){
				if (data.code == 200) {
					plus.storage.removeItem('USER_ID');
		    		plus.storage.removeItem('isManager');
		    		plus.storage.removeItem('isSystemMenager');
		    		plus.storage.removeItem('currentUser');
		    		plus.storage.setItem('isLogout','true');
		    		plus.webview.getWebviewById('tab').evalJS("stop_auto_update_messages()");
		    		plus.push.clear();//退出登录后清楚所有通知栏消息
		    		plus.webview.getWebviewById('tab').close();
				}else {
					mui.toast('网络错误，请重试...');
				}
		});
}

//本地存储的初始化
function initLocalStore() {
	var _username = plus.storage.getItem('username');
	var _password = plus.storage.getItem('password');
	$("#username").val(_username);
	$("#password").val(_password);
	if (_password) {
		$("#recordPwd").prop("checked", true);
	}
	else {
		$("#recordPwd").prop("checked", false);
	}
}

// 如果是管理员则显示以下信息
function showSystemMenager(){
	mui.plusReady(function(){
	$("#account_content").show();
	var str ="";
	for (var i=0;i<ACCOUNTS.length;i++){
		account = ACCOUNTS[i];
		str +='<li class="mui-table-view-cell"><a id="'+account.id+'">'+account.name+'</a></li>';
	}
	$("#account_list").html(str);
	$('#account_list a').on("click",function(){
			var account_id = this.getAttribute('id');
			for (var i=0;i<ACCOUNTS.length;i++){
				account = ACCOUNTS[i];
				if(account.id==account_id)
				plus.storage.setItem('currentUser',account.name+'');
			}
			changeUser(account_id);
			plus.nativeUI.showWaiting('正在切换账号...');
	});
});
}

// 管理员切换查看的用户
function changeUser(account_id){
	var username = SYSTEMUSERNAME;
	var password = STSTEMPW;
	$.getJSON( HOST_URL +'mobile_app/api/logout/get/?callback=?',function(data,status){
		if (data.code == 200) {
			$.getJSON( HOST_URL +'mobile_app/api/login/get/?username='+username+'&password='+password+'&account_id='+account_id+'&callback=?',
			function(data,status){
				if (data.code == 200) {
					plus.webview.getWebviewById('tab').reload();
					mui.toast('切换成功');
					}else {
						mui.toast(data.errorMsg);
				}
			});
		}else {
			mui.toast('网络错误');
		}
	});
}