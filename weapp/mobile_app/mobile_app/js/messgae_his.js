var mask,current_session_id,current_msg_user,audioPlayer,canPullDown=true;
mui.init({
		swipeBack: false,
		pullRefresh: {
			container: '#pullrefresh',
			down: {
				contentdown : '下拉加载更多',
				contentover : '释放加载',
				contentrefresh : '正在加载...',
				callback: appendLoadedMessage
			}
		}
	});


mui.plusReady(function(){
	//覆盖back方法，按手机返回键后，隐藏消息历史view
//	mui.back = function(){
//		mui.currentWebview.parent().hide();
//	}
	W.init();
	isManager = plus.storage.getItem('isManager')?true : false;
	isSystemMenager = plus.storage.getItem('isSystemMenager')?true : false;
	current_session_id = plus.storage.getItem('CURR_SESSIONID');
	getHisMessagesBySid(current_session_id);
});

function getHisMessagesBySid(s_id){
	message_history_curr_page = 1;
	W.getJsonP(
		HOST_URL + 'mobile_app/api/mui/messages/session_history/?s_id='+s_id+'&count='+message_history_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		function(response){

			if(response.code == 500){
				mui.toast(response.errMsg);
				return;
			}
			//是否显示回复栏
			if(response.is_active){
				document.querySelector('.reply_box').style.display = 'block';
				mask = mui.createMask(maskCallback);//callback为用户点击蒙版时自动执行的回调；
				bindEventsToElements();
			}
			current_msg_user = response.weixin_user_id;
			message_history_curr_page++;
			var msgList = baidu.template('message_history_template');
			var content = msgList(response);
			$("#message_history").html(content);
			window.setTimeout(function(){
				//滑动到底部
				W.scrollToBottom('message_history');
			},500);

			//监听音频加载
			addVoiceListen();

			$(".pic").bind("click", function(){
				pic_url = $(this).attr("src");
				showBigImage(pic_url);
			});
			if (!response.page_info.has_next){
				mui('#pullrefresh').pullRefresh().setStopped(true);
			}
			//关闭等待框
		    plus.nativeUI.closeWaiting();
		    //显示当前页面
		    mui.currentWebview.show();
		},function(){
			mui.toast('加载消息失败，请重试');
		}
	);
}

function appendLoadedMessage(){
	if(!canPullDown){
		return;
	}
	W.getJsonP(
		HOST_URL + 'mobile_app/api/mui/messages/session_history/?s_id='+current_session_id+'&cur_page='+message_history_curr_page+'&count='+message_history_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		function(response){
			var data = response.data;
			if(response.code == 500){
				mui.toast(response.errMsg);
				return;
			}

			message_history_curr_page++;
			var msgList = baidu.template('message_history_template');
			var content = msgList(response);
			$("#message_history").prepend(content);
			addVoiceListen();
			$(".pic").bind("click", function(){
				pic_url = $(this).attr("src");
				showBigImage(pic_url);
			});
			mui('#pullrefresh').pullRefresh().endPulldownToRefresh();
			if (!response.page_info.has_next){
				window.setTimeout(function(){
					mui('#pullrefresh').pullRefresh().setStopped(true);
				},200);//延时200ms以避免正在刷新字样还未收起就被阻止的问题，可能各个手机需要延时的时间不一样
			}

		},function(){
			mui.toast('网络错误，请稍后重试');
			mui('#pullrefresh').pullRefresh().endPulldownToRefresh();
		}
	);
}

//传递给父窗口执行显示大图
function showBigImage(pic_url){
	var curr_view = plus.webview.currentWebview();
	curr_view.hide();
	var parent_view = curr_view.parent();
	parent_view.evalJS("showBigImage('"+pic_url+"')");

}

function addVoiceListen(){
		$('#message_history').find('audio').bind("canplaythrough",function(){
				$(this).parent().find('.voice_duration').text(parseInt(this.duration)?parseInt(this.duration)+' \'\'':'').show();
			});
}

function send_msg(){
	var reply_text = document.querySelector('.msg_content').value.trim();
	var ori_text = reply_text;
	if(reply_text == '')return false;
	mui.toast('发送消息...');
	document.querySelector('.msg_content').value = '';
	
	reply_text = encodeURIComponent(reply_text);//处理特殊字符，如#，&等
	var url_content = HOST_URL + 'mobile_app/api/messages/reply/?s_id='+current_session_id+'&r_u='+current_msg_user+'&cont='+reply_text;
	W.getJsonP(url_content,function(response){
		if(response.code == 500){
			mui.toast(response.errMsg);
			return;
		}
		for(var i = 0; i < W.WEIXIN_EMOTIONS.length; i++) {
			if(ori_text.indexOf(W.WEIXIN_EMOTIONS[i].name) >= 0) {
				var sub_str = W.WEIXIN_EMOTIONS[i].name.replace(/]/g, '\\]');
				var re = new RegExp("\\" + sub_str, 'g');
				ori_text = ori_text.replace(re, '<img class="emoji_append" src="../img/weixin/' + W.WEIXIN_EMOTIONS[i].path + '" >');
			}
		}
		var msgList = baidu.template('message_history_template');
		var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":ori_text,"message_type":"text","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
		$("#message_history").append(content);
		//滑动到底部
		W.scrollToBottom('message_history');
		
		var src_str = document.querySelector('#emoji_button img').src;
		if (src_str.search(/_/) > 0) {
			maskCallback();
		}
		mui.toast('消息发送成功');
		//将消息切换到消息列表中的第一个
		var targetView = plus.webview.getWebviewById('message.html');
		targetView.evalJS("moveNewToFirst('text','"+ori_text+"')");

	},function(){
		document.querySelector('.msg_content').value = ori_text;
		mui.toast('消息发送失败，请重试');
	});
}

function getPicFromCamera(){
	plus.camera.getCamera().captureImage(appendImageToTemplate,function(e){
			mui.toast("取消操作");
		});
}

function getPicFromgallery(){
	plus.gallery.pick(appendImageToTemplate);
}

function appendImageToTemplate(path){
	//将图片预览加到页面中
	plus.io.resolveLocalFileSystemURL(path,function(entry){
		var src=entry.toLocalURL();
		var msgList = baidu.template('message_history_template');
		var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":"","pic_url":src,"message_type":"image","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
		$("#message_history").append(content);
		window.setTimeout(function(){
			//滑动到底部
			W.scrollToBottom('message_history');
			//上传图片
			var $pic = $('#message_history').children().eq(-1).children(1).find("img[class='pic']");
			uploadImage(src,$pic);
		},200);
		maskCallback();
		},function(e){
			mui.toast("取消");
		});

}

// 格式化时长字符串，格式为"HH:MM:SS"
function timeToStr(ts){
	if(isNaN(ts)){
		return "00:00:00";
	}
	var h=parseInt(ts/3600);
	var m=parseInt((ts%3600)/60);
	var s=parseInt(ts%60);
	return (ultZeroize(h)+":"+ultZeroize(m)+":"+ultZeroize(s));
}

function ultZeroize(v,l){
	var z="";
	l=l||2;
	v=String(v);
	for(var i=0;i<l-v.length;i++){
		z+="0";
	}
	return z+v;
}

function hideMe(domObj){
	domObj.style.visibility = 'hidden';
}

function showMe(domObj){
	domObj.style.visibility = 'visible';
}

var startTime,endTime,tc,tl,count=0,recordtime,loading,counting,re,recoder,send_flag = true;
function recording(){
	//停止正在播放的语音
	if(audioPlayer){
		audioPlayer.pause();
		audioPlayer = null;
		$("span.playVoice").removeClass("playVoice").addClass("icoVoice");
	}

	document.querySelector('.multy_selects').style.visibility = 'hidden';
	document.querySelector('.reply_box').style.visibility = 'hidden';
	document.getElementById('recordAni').style.visibility = 'visible';
	loading = document.querySelector('.recording');
	counting = document.querySelector('.counting');
	re = document.querySelector('.mui-icon-mic-filled');
	if(re.classList.contains('button-active')){
		//停止录音
		stopRecording();
	}else{
		startTime = new Date().getTime();
		re.classList.add('button-active');
		showMe(loading);
		showMe(counting);
		doCount();
		//TODO 开始录音
		recoder = recoder || plus.audio.getRecorder();

		recoder.record({filename:"_doc/"},function(path){
			plus.io.resolveLocalFileSystemURL(path,function(entry){
				//TODO 上传语音
				var src = entry.toLocalURL();
				var task=plus.uploader.createUpload(HOST_URL+'mobile_app/api/messages/send_mui_media/',
					{method:"POST",timeout:60},
					function(response,status){ //上传完成
						var data = JSON.parse(response.responseText);
						if(data.code==200){
							mui.toast('发送语音成功');
							var msgList = baidu.template('message_history_template');
							var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":"","audio_url":src,"message_type":"voice","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
							$("#message_history").append(content);
							//显示录音长度
							var audio_obj = $("#message_history").children(-1).find('audio').get(0);
							audio_obj.addEventListener("canplaythrough",function(){
								$(this).parent().find('.voice_duration').text(parseInt(this.duration)+' \'\'').show();
							},false);
							//将消息切换到消息列表中的第一个
							window.setTimeout(function(){
								//滑动到底部
								W.scrollToBottom('message_history');
							},200);
							var targetView = plus.webview.getWebviewById('message.html');
							targetView.evalJS("moveNewToFirst('[语音]','')");
						}else{
							mui.toast('发送语音失败,请重试!');
						}
					}
				);
				task.addData("type","voice");
				task.addData("filename",entry.name);
				task.addData("r_u",current_msg_user);
				task.addData("s_id",current_session_id);
				task.addData("domain",HOST_URL.substr(0,HOST_URL.length-1));
				task.addData("user",plus.storage.getItem('USER_ID'));
				task.addFile(src,{key:'upload_file'});
				if(send_flag){
					task.start();
				}

			},function(e){
				mui.toast('读取语音文件失败：'+e.message);
			});
		},function(e){
			mui.toast('录音失败：'+e.message);
		});
	}
}

function doCount(){
	loading.style.webkitTransition = "all 0.8s ease-in-out";
	loading.style.borderWidth = "0";
	loading.style.borderColor = "rgba(128,128,128,0.9)";
	tc = setTimeout( function(){
		count++;
		loading.style.webkitTransition = "";
		loading.style.borderWidth = "50px";
		loading.style.borderColor = "rgba(255,255,255,0)";
		counting.innerText = timeToStr(count);
		tl = setTimeout(doCount,0);
	}, 1000 );
}

function stopRecording(){
	document.querySelector('.reply_box').style.visibility = 'visible';
	document.getElementById('recordAni').style.visibility = 'hidden';
	maskCallback();
	count = 0;
	re.classList.remove('button-active');
	loading.style.webkitTransition = "";
	loading.style.borderWidth = "25px";
	loading.style.borderColor = "rgba(255,255,255,0)";
	counting.innerText = "00:00:00";
	endTime = new Date().getTime();
	if(endTime - startTime < 2000){
		send_flag = false;
		mui.toast('语音时间过短，取消发送');
	}else{
		mui.toast('发送语音...');
	}
	clearTimeout(tc);
	clearTimeout(tl);
	hideMe(loading);
	hideMe(counting);
	//TODO 上传语音
	if(recoder){
		recoder.stop();
		recoder = null;
	}
}

function uploadImage(path,$image_obj){
	var deg = 0;
	var $pic_mask_text = $image_obj.parent().find('.pic_mask_text');
	$pic_mask_text.hide();
	var $pic_mask = $image_obj.parent().find('.pic_mask');
	//用旋转的图标代替进度
	$pic_mask.css({'transform':'rotate(0deg)','visibility':'visible'});
	window.clearInterval(timer);
	var timer = window.setInterval(function(){
		deg += 5;
		$pic_mask.css('transform',"rotate("+deg+"deg)");
	},16.7);
	var url = HOST_URL + 'mobile_app/api/messages/send_mui_media/';
	var filename = path.substr(path.lastIndexOf('/')+1);
	var task=plus.uploader.createUpload(url,
		{method:"POST",timeout:60},
		function(response,status){ //上传完成
			var data = JSON.parse(response.responseText);
			if(data.code==200){
				mui.toast('发送图片成功');
				$pic_mask_text.hide();
				$image_obj.get(0).addEventListener('tap',function(){
					showBigImage(path);
				});
				//将消息切换到消息列表中的第一个
				var targetView = plus.webview.getWebviewById('message.html');
				targetView.evalJS("moveNewToFirst('[图片]','')");
			}else{
				mui.toast('发送图片失败,请重试...');
				$pic_mask_text.show();
				$pic_mask.html('');
				$pic_mask.get(0).style.visibility = 'hidden';

				$image_obj.one('tap',function(){
					 uploadImage(path,$image_obj);
				 });
			}
			window.clearInterval(timer);
			$pic_mask.css('visibility','hidden');
		}
	);
	task.addData("type","image");
	task.addData("filename",filename);
	task.addData("r_u",current_msg_user);
	task.addData("s_id",current_session_id);
	task.addData("domain",HOST_URL.substr(0,HOST_URL.length-1));
	task.addData("user",plus.storage.getItem('USER_ID'));
	task.addFile(path,{key:'upload_file'});
	//上传的进度有问题，暂不实现
//	task.addEventListener('statechanged',function(upload,status){
//		var total = upload.totalSize;
//		console.log('total = '+total);
//		window.clearInterval(timer);
//		var timer = window.setInterval(function(){
//			$pic_mask.html(Math.round(upload.uploadedSize/total)+'%');
//			console.log(upload.uploadedSize);
//		},50);
//
//		if(total == upload.uploadedSize){
//			window.clearInterval(timer);
//			$pic_mask.html('100%');
//		}
//	},false);
	task.start();
}

function bindEventsToElements(){
	document.querySelector('.msg_content').addEventListener('tap',listenerTapMsg);
	document.querySelector('.msg_content').addEventListener('focus',function(){
		document.querySelector('#show_emoji').style.visibility = 'hidden';
		document.querySelector('#mul_sel').style.visibility = 'hidden';
		document.querySelector('.reply_box').style.height = '150px';
		setTimeout(function(){
			W.scrollToBottom('message_history');
		},300);
		document.querySelector('#mul_msg').style.color = '';
		document.querySelector('#emoji_button').querySelector('img').src = "../img/weixin/emoji.png";
	});
	document.querySelector('#mul_msg').addEventListener('tap',function(){
		document.querySelector('#show_emoji').style.visibility = 'hidden';
		document.querySelector('#mul_sel').style.visibility = 'visible';
		document.querySelector('#emoji_button').querySelector('img').src = "../img/weixin/emoji.png";
		document.querySelector('.reply_box').style.height = '150px';
		if(this.style.color == 'green'){
			maskCallback();
			return;
		}
		this.style.color = 'green';
		var that = this;
		setTimeout(function(){
			document.querySelector('.reply_box').style.bottom = '0px';
			mask.show();
			document.getElementById('message_history').style.paddingBottom = '150px';
			W.scrollToBottom('message_history');
		},100);
	});
	document.querySelector('#emoji_button').addEventListener('tap',function(){
		document.querySelector('.msg_content').removeEventListener('tap', listenerTapMsg,false);
		var src_str = this.querySelector('img').src;
		if (src_str.search(/_/) > 0) {
			maskCallback();
			return;
		}
		document.querySelector('#mul_msg').style.color = '';
		this.querySelector('img').src = "../img/weixin/emoji_.png";
		document.querySelector('#mul_sel').style.visibility = 'hidden';

		mask.show();
		setTimeout(function(){
			document.querySelector('.reply_box').style.height = '220px';
			document.querySelector('#show_emoji').style.visibility = 'visible';
			document.querySelector('.reply_box').style.bottom = '0px';
			document.getElementById('message_history').style.paddingBottom = '220px';
			W.scrollToBottom('message_history');
		},100);

		document.querySelector('.msg_content').addEventListener('tap',listenerTapMsg);
	});
	document.querySelector('.msg_send').addEventListener('tap',send_msg);
	document.querySelector('.mui-icon-camera').addEventListener('tap',getPicFromCamera);
	document.querySelector('.mui-icon-image').addEventListener('tap',getPicFromgallery);
	document.querySelector('.mui-icon-mic-filled').addEventListener('tap',recording);
	document.getElementById('recordAni').addEventListener('tap',stopRecording);
	var img_doms = document.getElementsByClassName('one_emoji');
	for(var i = 0; i < img_doms.length; i++ ) {
		img_doms[i].addEventListener('tap', function(){
			var childArr = this.children;
			var title = childArr[0].getAttribute('title');
			if(title == "删除") {
				var msg_string = document.querySelector('.msg_content').value;
				document.querySelector('.msg_content').value = document.querySelector('.msg_content').value.substr(0, msg_string.length - 1);
			} else {
				document.querySelector('.msg_content').value += "["+title+"]";
			}
		})
	}
}


//msg监听Tap事件函数
function listenerTapMsg(){
	var bot = document.querySelector('.reply_box').style.bottom;
	if(bot == '-100px')return;
	setTimeout(function(){
		document.querySelector('.reply_box').style.bottom = '-100px';
		document.getElementById('message_history').style.paddingBottom = '50px';
		this.focus();
	},50);
}

function maskCallback(){
	document.querySelector('#mul_msg').style.color = '';
	document.querySelector('#emoji_button').querySelector('img').src = "../img/weixin/emoji.png";
	document.querySelector('.reply_box').style.height = '150px';
	document.querySelector('.reply_box').style.bottom = '-100px';
	document.getElementById('message_history').style.paddingBottom = '50px';
	mask.close();
}

//控制语音播放
function controlVoice(event,obj){
	event.stopPropagation();
	var spans = $("span.playVoice");
	if(audioPlayer && !audioPlayer.paused){
		audioPlayer.pause();
		spans.removeClass("playVoice").addClass("icoVoice");
		if(audioPlayer.src == $(obj).find('audio').attr('src')){
			audioPlayer = null;
			return;
		}
	}
	audioPlayer = $(obj).find('audio')[0];
	var span = $(obj).find('span');

	span.removeClass("icoVoice").addClass("playVoice");
	audioPlayer.play();
	audioPlayer.addEventListener('ended', function() {
		span.removeClass("playVoice").addClass("icoVoice");
	});
}

/**
 * 增量显示最新的消息
 * 之前加载的消息不会被清除，新消息只会append进去
 */
function loadNewMessage(){
	W.getJsonP(
		HOST_URL + 'mobile_app/api/messages/session_history/?s_id='+s_id+'&cur_page=1&count='+message_history_per_page+'&isManager='+isManager+'&isSystemMenager='+isSystemMenager,
		function(response){

			if(response.code == 500){
				mui.toast(response.errMsg);
				return;
			}
			//是否显示回复栏
			if(response.is_active){
				document.querySelector('.reply_box').style.display = 'block';
				mask = mui.createMask(maskCallback);//callback为用户点击蒙版时自动执行的回调；
				bindEventsToElements();
			}else{
				document.querySelector('.reply_box').style.display = 'none';
			}
			current_msg_user = response.weixin_user_id;
			var msgList = baidu.template('message_history_template');
			var content = msgList(response);
			$("#message_history").append(content);
			window.setTimeout(function(){
				//滑动到底部
				W.scrollToBottom('message_history');
			},500);

			//监听音频加载
			addVoiceListen();

			$(".pic").bind("click", function(){
				pic_url = $(this).attr("src");
				showBigImage(pic_url);
			});

		},function(){
			mui.toast('加载消息失败，请重试');
		}
	);
}
