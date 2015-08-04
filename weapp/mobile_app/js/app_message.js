$.ui.ready(function(){
	$('#get_messages_list_btn').click(function(){
		initMessagesTmp();
		scroll_to_refresh('#message',initMessagesTmp);
	});
	window.onhashchange = doHash;
});
var blankDiv = "<div id='blockspace' style='height:45px;'></div>";
var initMessagesTmp_is_busy = false;//阻止频繁刷新
var current_msg_user = '';
var current_session_id = '';
//加载消息列表
function initMessagesTmp(){
	if(initMessagesTmp_is_busy) return;
	initMessagesTmp_is_busy = true;
	$.ui.showMask('加载消息列表...');
	message_list_curr_page = 1; //每次重新加载列表都首先初始化页数
	initHeader();
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/messages/?page='+message_list_curr_page+'&count='+message_count_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		success:function(response){
			$.ui.hideMask();
			if(response.code == 500){
				showErrorMessage(response.errMsg);
				$("#messages_list").html("<div style='text-align:center;margin-top:5px;'>没有消息</div>");
				initMessagesTmp_is_busy = false;
				return;
			}
			message_list_curr_page++;
			$("#error_message").hide();

			var msgList = baidu.template('messages_list_template');
			var content = msgList(response.data);
			$("#messages_list").html(content);
			//加入【点击加载更多】
			if(response.data.page_info.has_next){//如果总页数只有一页，则不需要加载更多
				var loadBtn = new loadNextPageBtn({
					'url' : HOST_URL + 'mobile_app/api/messages/?count='+message_count_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager+'&page=',//page的值会在方法中添加
					'css_id' : 'messages_list',
					'fn' : appendNewMessage,
					'page_name' : 'message_list_curr_page'
				});
				loadBtn.appendToTail();
			}
			alinkClickEvent();
			initMessagesTmp_is_busy = false;
		},
		error:function(){
			$.ui.hideMask();
			showErrorMessage();
			initMessagesTmp_is_busy = false;
		}
	});
}

function appendNewMessage(response){
	message_list_curr_page ++;
	var iterms = response.data.iterms;
	var msgList = baidu.template('messages_list_template');
	var content = msgList(response.data);
	$("#messages_list").append(content);
	alinkClickEvent();
	return response.data.page_info.has_next;
}

function getHisMessagesBySid(s_id){
    $.ui.slideSideMenu = false;
	message_history_curr_page = 1;
	$('#menubadge').hide();
	$('#reply_content').val('');
	$("#message_history").html('');
	$.ui.showMask('加载消息历史...');
	var myScroller = $('#message_his').scroller();
	$("#backButton").unbind();
	$("#backButton").bind("click", function(){
		ReplyBox.cancle_record_audio();
		var audios = $("audio");
		var spans = $("span.playVoice");
		audios.forEach(function(aud){
			aud.pause();
			try{
				aud.currentTime = 0;
			}catch(e){

			}
		});
		spans.forEach(function(span){
			$(span).replaceClass("playVoice", "icoVoice");
		});
	});
	$("#blockspace").remove();
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/messages/session_history/?s_id='+s_id+'&count='+message_history_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		success:function(response){
			$.ui.hideMask();
			if(response.code == 500){
				showErrorMessage(response.errMsg);
				return;
			}
			$("#error_message").hide();

			var msgList = baidu.template('message_history_template');
			var content = msgList(response);
			$("#message_history").html(content);
			//监听音频加载
			addVoiceListen();
			$(".pic").bind("click", function(){
				pic_url = $(this).attr("src");
				showBigImage(pic_url);
			});
			if(response.send_user_name){
				$.ui.setTitle(response.send_user_name);
			}else{
				$.ui.setTitle("消息历史");
			}

			if (!response.page_info.has_next){
				myScroller.refresh = false;
				$("#message_history").prepend("<div class='error_message'><div id='error_message_history'>没有更多消息了</div></div>");
			}else{
				// if(message_history_curr_page * message_history_per_page >= max_message_history_loaded_count){
				if(message_history_curr_page >= max_message_history_loaded_count){
					$("#message_history").prepend("<div class='error_message'><div id='error_message_history'>更多消息请见PC端</div></div>");
				}else{
					scroll_to_refresh('#message_his',getMessage,s_id);
				}
			}
			$("#message_history").parent().prepend(blankDiv);
			initMsgHisTmp(response);
			$("#message_his").scroller().adjustScrollToBottom();
			$('.afScrollPanel').css('transform','translateY(0)');//使最上面不再有10px的空白而导致出现划屏抖动
			$('#backButton').show();
		},error:function(){
			$.ui.hideMask();
			showErrorMessage();
			$('#backButton').show();
		}
	});
}


var getMessage_is_busy = false;//函数执行结束后才能再次执行
function getMessage(s_id){
	if(getMessage_is_busy) return;
	getMessage_is_busy = true;
	message_history_curr_page++;
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/messages/session_history/?s_id='+s_id+'&cur_page='+message_history_curr_page+'&count='+message_history_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		success:function(response){
			$.ui.hideMask();
			var data = response.data;
			if(response.code == 500){
				showErrorMessage(response.errMsg);
				return;
			}
			var msgList = baidu.template('message_history_template');
			var content = msgList(response);
			$("#message_history").prepend(content);
			addVoiceListen();
			$(".pic").bind("click", function(){
				pic_url = $(this).attr("src");
				showBigImage(pic_url);
			});
			var myScroller = $('#message_his').scroller();
			if (!response.page_info.has_next){
				myScroller.refresh = false;
				myScroller.setRefreshContent("");
				$("#message_history").prepend("<div class='error_message'><div id='error_message_history'>没有更多消息了</div></div>");
			}else{
				// if(message_history_curr_page * message_history_per_page >= max_message_history_loaded_count){
				if(message_history_curr_page >= max_message_history_loaded_count){
					myScroller.refresh = false;
					myScroller.setRefreshContent("");
					$("#message_history").prepend("<div class='error_message'><div id='error_message_history'>更多消息请见PC端</div></div>");
				}
			}
			getMessage_is_busy = false;
		},error:function(){
			$.ui.hideMask();
			showErrorMessage();
			getMessage_is_busy = false;
		}
	});
}

function initMsgHisTmp(resp){
	current_msg_user = resp.weixin_user_id;
	$('#backButton').unbind('click');
	$('#backButton').bind('click',function(event){
        $.ui.slideSideMenu = true;
		ReplyBox.clearBox();
		$('#backButton').hide();
		$('#menubadge').show();
		//返回时，回到之前浏览的位置
		var messageScroller = $("#message").scroller();
		var curScrollTop = $("#message").attr('scrollTop');
		event.stopPropagation();
		$.ui.goBack();
		messageScroller.scrollTo({x:0,y:curScrollTop});
	});
	if(resp.is_active){  //可回复
		ReplyBox.createBox();
	}
	$("#message_his").scroller().adjustScrollToBottom();
}

//绑定消息列表的click事件，点击后移除新消息泡泡并记录位置
function alinkClickEvent(){
	$('#message a').unbind('click');
	$('#message a').bind('click',function(){

		var s_id = this.getAttribute('s_id');
		if (!isManager && !isSystemMenager){
			$("#new_message_"+s_id).remove();
		}
		saveLastVisitPosition("#message"); //记录浏览位置
		current_session_id = s_id;
		getHisMessagesBySid(s_id);
	});
}

//设置图片的宽度
function setPicWidth(){
	var w = screen.width;
	if(w>500){
		w = w/2;
	}
	w = w*0.6;
	return w+"px";
}

//显示大图的方法
function showBigImage(pic_url){
	var h = screen.height;
	var w = screen.width;
	if(w>500){
		w = w/2;
		h = h/2
	}
    	h = h - 20;
	$slideView = $("#slideView");
	$slideView.css({
		"min-height" : h+"px",
		"opacity" : "1"
	}).html("<div style='text-align:center;line-height:"+h+"px;transform:translateX(0px);'><div style='width:"+w+"px;height:"+h+"px;'><img class='showbig' src='"+pic_url+"'></div></div>").show();
	
	$slideView.click(function(){
		$slideView.hide().html("");
	})
}

//控制语音播放
function controlVoice(obj,event){
	ReplyBox.cancle_record_audio();
	var audio = $(obj).find('audio')[0];
	var span = $(obj).find('span');
	if (audio.currentTime == 0){
		console.log('in');
		event.stopPropagation();
		var audios = $("audio");
		var spans = $("span.playVoice");
		audios.forEach(function(aud){
			aud.pause();
			try{
				aud.currentTime = 0;
			}catch(e){

			}
		});
		spans.forEach(function(span){
			$(span).replaceClass("playVoice", "icoVoice");
		});
		span.replaceClass("icoVoice", "playVoice");
		audio.play();
		$(obj).find('audio').bind('ended', function() {
			span.replaceClass("playVoice", "icoVoice");
		});
	}else{
		audio.pause();
		span.replaceClass("playVoice", "icoVoice");
		audio.currentTime = 0;
	}
}

//监听hashchange
function doHash(){
	var hash_str = window.location.hash;
	if (hash_str != 'message_his'){
		pauseVoice();
		ReplyBox.cancle_record_audio();
	}
}
//暂停语音播放
function pauseVoice(){
	var audios = $("audio");
	var spans = $("span.playVoice");
	audios.forEach(function(aud){
		aud.pause();
		try{
			aud.currentTime = 0;
		}catch(e){

		}
	});
	spans.forEach(function(span){
		$(span).replaceClass("playVoice", "icoVoice");
	});
}

function addVoiceListen(){
		$('#message_history .container').find('audio').each(function(){
			this.addEventListener("canplaythrough",function(){
				$(this).parent().find('.voice_duration').text(parseInt(this.duration)?parseInt(this.duration)+' \'\'':'').show();
			},false);
		});

}
