//本地存储的初始化
var dthMobileOA = null;
function initLocalStore() {
	dthMobileOA = new LocalMobelInfo();
	var _username = dthMobileOA.getUserName();
	var _password = dthMobileOA.getUserPassword();
	$("#username").val(_username);
	$("#password").val(_password);
	if (_password) {
		$("#recordPwd").prop("checked", true);
		//处理自动登录
		if (dthMobileOA.getBooleanData("autologin")) {
			$("#autologin").prop("checked", true);
			$("#login_btn").click();
		}
	}
	else {
		$("#recordPwd").prop("checked", false);
	}
	// 获取左侧设置栏
	if (dthMobileOA.getBooleanData("sound")) {
		$("#sound").prop("checked", true);
	}else{
		$("#sound").prop("checked", false);
	}
	if (dthMobileOA.getBooleanData("vibrator")) {
		$("#vibrator").prop("checked", true);
	}else {
		$("#vibrator").prop("checked", false);
	}
	if (dthMobileOA.getBooleanData("push")) {
		$("#push").prop("checked", true);
	}else {
		$("#push").prop("checked", false);
	}
}

$.ui.ready(function() {
	$("#login_btn").one("click", loginFunction);
	initLocalStore();
	$("#logout").one("click", logoutFunction);
});

// 登出
function logoutFunction(){
	$.jsonP({
		url: HOST_URL +'mobile_app/api/logout/get/',
		success:function(data){
			$("#search_order").hide();
			$("#error_message").hide();
			ReplyBox.clearBox();
			$("#account_content").hide();
			$("#meun_statistic").hide();
			$("#order_static_content").html("");
			$("#statisticsView").html("");
			USER_ID = 0;
			isManager = false;
			$('#get_login_page').click();
			$("#login_btn").one("click", loginFunction);
			//停止自动刷新消息
			stop_auto_update_messages();
			//清空内容，以免不同用户切换时数据会乱
			$('#messages_list').html('');
			$('#order_list_content').html('');
			$("#filter").val("-1");
			//清空搜索框
			$("#search_order_id").val("");
			$.ui.slideSideMenu = false;
		},
		error:function(){
			showErrorMessage();
		}
	});
}

// 登录
function loginFunction(){
	$('#username,#password').blur(function(){
			$("#login_btn").one("click", loginFunction);
		});

	var username = trim($('#username').val());
	var password = trim($('#password').val());
	password = encodeURIComponent(password);//处理特殊字符，如#，&等
	if (!(username&&password)) {
		$('#login_error_message').html("请输入用户名或密码");
	}
	else{
		//判断是否包含_manager,不包含则不作操作
		if (username.indexOf("_manager") > 0) {
			username = username.split("_manager",1);
			isManager = true;
		}else{}
		$.jsonP({
			url: HOST_URL + 'mobile_app/api/login/get/?username='+username+'&password='+password+'&account_id='+ACCOUNTS[0]['id'],
			success:function(data){
				$.ui.slideSideMenu = true;
				$("#error_message").hide();
				$("#account_content").hide();
				if (data.code == 200) {
					var isRecondPwd = $("#recordPwd").prop("checked");
					if (isRecondPwd) {
						if(isManager){
							dthMobileOA.updateManager(username, password);
						}else{
							dthMobileOA.updateUser(username, password);
						}
					} else {
						if(isManager){
							dthMobileOA.updateManager(username, "");
						}else{
							dthMobileOA.updateUser(username, "");
						}
					}
					var isAutoLogin = $("#autologin").prop("checked");
					dthMobileOA.putBooleanData("autologin", isAutoLogin);
					$("#get_graph_data_btn").click();
					$("#logout").one("click", logoutFunction);
					$('#login_error_message').empty();
					//检查更新
					login_check_new();
					USER_ID = data.data.user_id;
					username = data.data.username;
					isSystemMenager = data.data.isSystemMenager;
					//根据身份显示用户名
					if(isManager){
						$("#show_username").html(username+'_manager');
					}else{$("#show_username").html(username);}
					if(isSystemMenager){
						$("#show_username").html('系统管理员');
					}
					//开始定时刷新消息任务
					start_auto_update_messages();
					//系统管理员显示项
					if (isSystemMenager){
						showSystemMenager();
						$('#account_list :first-child a' ).addClass("changecolor");
					}
				} else {
					$('#login_error_message').html(data.errorMsg);
				}
			},
			error:function(){
				showErrorMessage();
			}
		});
	}
}

// 获取用户ID
function getUserId(){
	if (USER_ID) {
		return USER_ID;
	}
	else {
		$('#get_login_page').click();
	}
}

// 如果是管理员则显示以下信息
function showSystemMenager(){
	$("#account_content").show();
	var str ="";
	for (var i=0;i<ACCOUNTS.length;i++){
		account = ACCOUNTS[i];
		str +='<div class="account"><a id="'+account.id+'">'+account.name+'</a></div>';
	}
	$("#account_list").html(str);
	$('#account_list a').on("click",function(){
		var account_id = this.getAttribute('id');
		changeUser(account_id);
		$('#account_list div a' ).removeClass("changecolor");
		$('#'+account_id).addClass("changecolor");
	});
}

// 管理员切换查看的用户
function changeUser(account_id){
	//停止自动刷新消息
	stop_auto_update_messages();
	hide_menu_mask();
	show_menu_mask("正在切换账号...");
	var username = SYSTEMUSERNAME;
	var password = STSTEMPW;
	$.jsonP({
			url: HOST_URL +'mobile_app/api/logout/get/',
			success:function(data){

				$("#search_order").hide();
				$("#error_message").hide();
				ReplyBox.clearBox();
				//清空内容，以免不同用户切换时数据会乱
				$('#messages_list').html('');
				$('#order_list_content').html('');
                $("#filter").val("-1");
                //清空搜索框
                $("#search_order_id").val("");
				$.jsonP({
					url: HOST_URL + 'mobile_app/api/login/get/?username='+username+'&password='+password+'&account_id='+account_id,
					success:function(data){
						hide_menu_mask();
						show_menu_mask("切换成功");
						if (data.code == 200) {
							//开始定时刷新消息任务
							start_auto_update_messages();
							window.setTimeout(function(){
						        hide_menu_mask();
						    },1000);
							if($('#get_order_list_btn').hasClass("pressed")){
								showOrderList();
							}
							if($('#get_graph_data_btn').hasClass("pressed")){
								$("#get_graph_data_btn").click();
							}
							if($('#get_messages_list_btn').hasClass("pressed")){
								initMessagesTmp();
							}
						} else {
							hide_menu_mask();
							showErrorMessage(data.error_msg);
						}
					},
					error:function(){
						hide_menu_mask();
						showErrorMessage();
					}
				});
			},
			error:function(){
				hide_menu_mask();
				showErrorMessage();
			}
		});
}
