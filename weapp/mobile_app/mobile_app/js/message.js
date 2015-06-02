var current_msg_user = '',
	current_session_id = '',
	load_msg_url;
mui.ready(function(){
	mui.init({
		swipeBack: false,
		pullRefresh: {
			container: '#pullrefresh',
			down: {
				contentdown : '下拉刷新',
				contentover : '释放刷新',
				contentrefresh : '正在刷新...',
				callback: pulldownRefresh
			}
		}
	});
	mui.plusReady(function(){
		isManager = plus.storage.getItem('isManager')?true : false;
		isSystemMenager = plus.storage.getItem('isSystemMenager')?true : false;
		load_msg_url = HOST_URL + 'mobile_app/api/mui/messages/?page='+message_list_curr_page+'&count='+message_count_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager;

		W.init();
		loadMsg();
	});
});


/**
 * 加载消息列表
 */
function loadMsg(){
	W.getJsonP(load_msg_url,function(response){
		if(response.code == 500){
			showNoMessage('加载消息列表失败，下拉刷新');
			return;
		}
		message_list_curr_page++;
		var msgList = baidu.template('messages_list_template');
		var content = msgList(response.data);
		var list_dom = document.getElementById("messages_list");

		list_dom.innerHTML = '';
		list_dom.innerHTML = content;
		if(response.data.page_info.has_next){
			var loadBtn = new W.loadNextPageBtn({
				'url' : HOST_URL + 'mobile_app/api/mui/messages/?count='+message_count_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager+'&page=',//page的值会在方法中添加,
				'css_id' : 'messages_list',
				'fn' : appLoadedMsg,
				'page_name' : 'message_list_curr_page'
			});
			loadBtn.appendToTail();
		}
	},function(){
		showNoMessage('加载消息列表失败，下拉刷新');
		mui.toast('加载消息列表失败，请稍后重试...');
	});
}

function appLoadedMsg(response){
	if(response.code == 500){
			return true;
		}
	message_list_curr_page++;
	var msgList = baidu.template('messages_list_template');
	var content = msgList(response.data);
	var list_dom = $("#messages_list").append(content);
	return response.data.page_info.has_next;
}


/**
 * 下拉刷新具体业务实现
 */
function pulldownRefresh() {
	setTimeout(function() {
		message_list_curr_page = 1;//初始化当前页数
		loadMsg();
		mui('#pullrefresh').pullRefresh().endPulldownToRefresh(); //refresh completed
	}, 1000);
}

function mainTabFresh(){
	message_list_curr_page = 1;//初始化当前页数
	loadMsg();
}

function openHisWindow(obj){
	current_session_id = obj.getAttribute('s_id');
	var current_sender_name = obj.querySelector('b').innerHTML;
	plus.storage.setItem('CURR_SESSIONID',current_session_id);//存储当前选择的用户的sessionid
	plus.storage.setItem('CURR_CUST_NAME',current_sender_name);//存储当前选择的用户名
	var his_main = plus.webview.getWebviewById('message_his_main.html');
	if(!his_main){
		mui.openWindow({
			url:'message_his_main.html',
			show:{
		      autoShow:false
		    }
		});
	}else{
		his_main.evalJS("loadNewMessage()");
		his_main.show();
	}

	//除去气泡
	var bdgeval = document.querySelector('#new_message_'+current_session_id);
	if(bdgeval && !isManager && !isSystemMenager) bdgeval.remove();//管理员和系统管理员帐号不消除
}

/**
 * 将新消息切换到消息列表中的第一个
 */
function moveNewToFirst(type,decode_reply){

	var $li = $("a[s_id='"+current_session_id+"']");
	if(type == 'text' && decode_reply){
//		decode_reply = decode_reply.length > 10 ? decode_reply.substr(0,10)+'...' : decode_reply;
		$li.find(".msg").html(decode_reply);
	}else{
		$li.find(".msg").html(type);
	}

	$li.find(".time").html('刚刚');
	var cur_li = $li.parent();
	$("#messages_list ul").eq(0).prepend(cur_li);
	$("#message").attr('scrollTop', '0');
}

/**
 * 当消息列表加载失败后，显示错误提示信息
 * @param {String} msg ：当传进msg时，表示加载失败，此时不阻止下拉刷新
 * 		当不传msg，则表示没有消息，此时阻止下拉刷新
 */
function showNoMessage(msg){
	var nomsg = document.getElementById('nomsg');
	msg = msg || '暂无消息';
	nomsg.innerHTML = msg;
	nomsg.style.visibility = 'visible';
	if(!msg){
		window.setTimeout(function(){
			mui('#pullrefresh').pullRefresh().setStopped(true);//阻止下拉刷新
		},200);
	}


}
