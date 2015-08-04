/**
 * Created by aix on 2014/12/15
 *
 * createBox：生成回复功能区
 * cancle_record_audio：取消录制音频
 * clearBox：清空回复功能区
 * ReplyBox 暴露出的全局对象
 */
(function($){
	var ReplyBox = {
		_record_status : 'done',//录音状态
		_record_media : null,//媒体对象，用于录音和播放
		_record_audio : '',//录音文件
		_record_timer : null,//录音定时器
		createBox : function(){
			var inner_html = "";
			var $el = $('#reply_box');
			$el.html('');//先清空内容，以免重复
			inner_html = "<a id='file_style_shell' class='icon add big add_pic'></a>";//选择图片的图标
			inner_html += "<input type='file' id='file' accept='image/*'/>";
			inner_html += "<textarea id='reply_content' name='reply_content'></textarea>";
			inner_html += "<div class='icon mic big add_audio'></div>";
			inner_html += "<a class='button blue' id='reply_confirm'>发送</a>";
			$el.html(inner_html);
			//绑定事件
			$("#file").bind('change',_bindEventsToFile);
			$('.add_audio').bind('click',_bindEventsToMicIcon);
			$('#reply_confirm').bind('click',_bindEventsToSendBtn);
			_adjustPage();
			$el.show();
		},
		cancle_record_audio : function(){
			if(ReplyBox._record_media && ReplyBox._record_status == 'recording'){
				ReplyBox._record_status = 'done';
				ReplyBox._record_media.stopRecord();
				ReplyBox._record_media = null;
				showErrorMessage('已取消...',2000);
				$('.mic').removeClass('btn_clicked');
				clearInterval(ReplyBox._record_timer);
			}
		},
		clearBox : function(){
			$('#reply_box').hide().html('');
		}
	};
	function _bindEventsToFile(){
		var file_val = this.value;
		file_tail = file_val.substr(file_val.lastIndexOf('.')+1).toUpperCase();
		if(!/(PNG|GIF|JPG|JPEG|BMP)$/.test(file_tail)){
			showErrorMessage("只能发送图片",2000);
			return false;
		}
		var reader = new FileReader();
		var file = this.files[0];
		reader.readAsDataURL(file);
		reader.onload = function(e){
			var pic_src = this.result.replace('data:base64,', 'data:'+file.type+';base64,');
			var msgList = baidu.template('message_history_template');
			var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":"","pic_url":pic_src,"message_type":"image","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
			$("#message_history").append(content);
			var $picMask = $('#message_history .container').eq(-1).find('.pic_mask');
			var $picEl = $picMask.parent().find('img');
			setTimeout(function(){
				$picMask.css({
					'height' : $picEl.height(),
//					'display' : 'block'
				}).show();
				_send_image($picMask);
			},500);
			$("#message_his").scroller().adjustScrollToBottom();
			_recreateFileElement();
		};
	}
	function _bindEventsToMicIcon(){
		var $el = $(this);
		pauseVoice();
		if($el.hasClass('btn_clicked') && ReplyBox._record_media && ReplyBox._record_status=='recording'){
			ReplyBox._record_status = 'sendding';
			$el.removeClass('btn_clicked');
			clearInterval(ReplyBox._record_timer);
			$("#error_message").hide();
			$("#error_message span").html('').css('color','');
			ReplyBox._record_media.stopRecord();
			var ft = new FileTransfer();
			var options = new FileUploadOptions();
			options.fileKey = "file";
			options.fileName = '_audio.amr';
			options.mimeType = "audio/AMR";
			var params = {};
			params.type = 'voice';
			params.user = USER_ID;
			params.s_id = current_session_id;
			params.r_u = current_msg_user;
			params.domain = HOST_URL.substr(0,HOST_URL.length-1);
			params.src = 'test';
			options.params = params;
			showErrorMessage('发送语音...',-1);
			ft.upload(ReplyBox._record_audio, encodeURI(HOST_URL+'mobile_app/api/messages/send_media/'), function(res){
				res = JSON.parse(res.response);
				if(res.code == 200){
					var msgList = baidu.template('message_history_template');
					var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":"","audio_url":ReplyBox._record_audio,"message_type":"voice","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
					$("#message_history").append(content);
					//显示录音长度
					var audio_obj = $("#message_history .container").eq(-1).find('audio').get(0);
					audio_obj.addEventListener("canplaythrough",function(){
						$(this).parent().find('.voice_duration').text(parseInt(this.duration)+' \'\'').show();
					},false);
					//将消息切换到消息列表中的第一个
					var $message_li = $("#message a[s_id='"+current_session_id+"']");
					$message_li.find(".msg").text('[语音]');
					$message_li.find(".time").text('刚刚');
					var cur_li = $message_li.parent();
					$("#messages_list ul").prepend(cur_li);
					$("#message").attr('scrollTop', '0');
					$("#message_his").scroller().adjustScrollToBottom();
					showErrorMessage('语音发送成功',2000);
				}else{
					showErrorMessage('语音发送失败,请重试...',2000);
				}
				ReplyBox._record_status = 'done';
				ReplyBox._record_media.release();
				ReplyBox._record_media = null;
			}, function(error){
				ReplyBox._record_status = 'done';
				ReplyBox._record_media.release();
				ReplyBox._record_media = null;
				showErrorMessage('网络错误，请重试..',2000);
			}, options);
		}else if(ReplyBox._record_status == 'done'){
			ReplyBox._record_status='recording';
			$el.addClass('btn_clicked');
			window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, function(fileSystem){
				fileSystem.root.getDirectory("weizoom_tmp",
		        {create: true, exclusive: false},
		        successCall,function(){
					fileSystem.root.getDirectory("weizoom_tmp",
	                {create: false, exclusive: false},
					successCall,fail);
				});
			}, fail);
		}
		var timer_count;
		var successCall = function(dir){
			timer_count = 0;
			ReplyBox._record_audio = dir.toURL()+'/_audio.amr';
	        ReplyBox._record_media = new Media(ReplyBox._record_audio,function(){
		        $("#error_message").unbind('click');//录制成功后，解绑click，以免触发取消
			},function(error){
		        showErrorMessage('error'+error.message,1000);
			});
			ReplyBox._record_media.startRecord();
			$("#error_message").unbind('click');
			$("#error_message").bind('click',ReplyBox.cancle_record_audio);
			clearInterval(ReplyBox._record_timer);
			ReplyBox._record_timer = setInterval(function(){
				timer_count++;
				if(timer_count >= 60){
					$el.trigger('click');
					return;
				}
				if(timer_count >= 50){
					$("#error_message span").html('开始录音...'+timer_count+'\'').css('color','red');
				}else{
					$("#error_message span").html('开始录音...'+timer_count+'\'');
				}
			},1000);
			clearTimeout(hideErrorTimeout);
			showErrorMessage('开始录音...0\'',-1);
		};
		var fail = function(error){
			console.log('create dir/file fail...'+error.code);
			ReplyBox._record_status = 'done';
			ReplyBox._record_media = null;
		};
	}
	function _bindEventsToSendBtn(){
		var $_this = $(this);
		if($('#reply_content').val().trim() == '')return false;
		$.ui.showMask('消息发送中...');
		var reply_text = $('#reply_content').val();
		$('#reply_content').val('');
		reply_text = encodeURIComponent(reply_text);//处理特殊字符，如#，&等
		var url_content = HOST_URL + 'mobile_app/api/messages/reply/?s_id='+current_session_id+'&r_u='+current_msg_user+'&cont='+reply_text;
		$.jsonP({
			url: url_content,
			success:function(response){
				$.ui.hideMask();
				if(response.code == 500){
					showErrorMessage(response.errMsg);
					return;
				}
				$("#error_message").hide();
				$('#reply_content').val('');
				var msgList = baidu.template('message_history_template');
				var content = msgList({"data":[{"sender_name":"3181","weixin_created_at":"刚刚","content":decodeURIComponent(reply_text),"message_type":"text","is_reply":true,"weixin_message_id":"","id":1138,"sender_icon":"/static/img/user-1.jpg"}]});
				$("#message_history").append(content);
				$("#message_his").scroller().adjustScrollToBottom();
				var decode_reply = decodeURIComponent(reply_text);
				var $li = $("#message a[s_id='"+current_session_id+"']");
				$li.find(".msg").text(decode_reply.length > 10 ? decode_reply.substr(0,10)+'...' : decode_reply);
				$li.find(".time").text('刚刚');
				//将消息切换到消息列表中的第一个
				var cur_li = $li.parent();
				$("#messages_list ul").eq(0).prepend(cur_li);
				$("#message").attr('scrollTop', '0');
			},
			error:function(){
				$('#reply_content').val(reply_text);
				$.ui.hideMask();
				showErrorMessage();
			}
		});

	}
	//发送图片
	function _send_image($a_obj){
        showErrorMessage('发送图片...',-1);
		$a_obj.unbind('click');
		var $pic_mask_text = $a_obj.parent().find('.pic_mask_text');
		$pic_mask_text.hide();
		var pic_src = $a_obj.parent().find('img').attr('src');
		var url_content = HOST_URL + 'mobile_app/api/messages/send_media/';
		var ori_height = $a_obj.height();
		var height_num = parseInt(ori_height);
		var pic_mask_animate_timer = setInterval(function(){
			height_num -= height_num*0.005;
			$a_obj.css('height',height_num+'px');
			if(parseInt($a_obj.height()) <= height_num*0.3) clearInterval(pic_mask_animate_timer);
		},45);
		$.ajax({
				url: url_content,
				type:"POST",
				data:{
					"type" : "image",
					"src" : pic_src,
					"r_u" : current_msg_user,
					"s_id" : current_session_id,
					"domain" : HOST_URL.substr(0,HOST_URL.length-1),
					"user" : USER_ID
				},
				success:function(response){
					response = JSON.parse(response);
					if(response.code == 500){
						$pic_mask_text.show();
						clearInterval(pic_mask_animate_timer);
						$a_obj.css('height',ori_height);
						$a_obj.bind('click',function(){
							 _send_image($a_obj);
						 });
						showErrorMessage(response.errMsg);
						return false;
					}else{
						$pic_mask_text.hide();
						var $message_li = $("#message a[s_id='"+current_session_id+"']");
						$message_li.find(".msg").text('[图片]');
						$message_li.find(".time").text('刚刚');
						//将消息切换到消息列表中的第一个
						var cur_li = $message_li.parent();
						$("#messages_list ul").prepend(cur_li);
						$("#message").attr('scrollTop', '0');
//							$a_obj.replaceClass('loading','check');
					}
					clearInterval(pic_mask_animate_timer);
					$a_obj.css('height',0+'px');
					$a_obj.hide();
					showErrorMessage('图片发送成功..',2000);
					$a_obj.parent().find('img').bind('click',function(){
						showBigImage(pic_src);
					});

					$("#message_his").scroller().adjustScrollToBottom();
				},
				 error: function() {
					 $pic_mask_text.show();
					 clearInterval(pic_mask_animate_timer);
					 $a_obj.css('height',ori_height);
					 $a_obj.bind('click',function(){
						 _send_image($a_obj);
					 });
					 showErrorMessage('网络错误,请重试...',2000);
				}
		});
	}
	//重新生成图片选择标签，修复两次选择同一张图片后不触发change事件的问题
	function _recreateFileElement(){
		var $el = $('#reply_box');
		$('#file').unbind('change');
		$('#file').remove();
		$("<input type='file' id='file' accept='image/*'/>").insertAfter('#file_style_shell');
		$("#file").bind('change',_bindEventsToFile);
	}

	//回复信息时，由于弹出软键盘，故调整页面结构
	function _adjustPage(){
		var $el = $('#reply_content');
		$el.bind('focus',function(){
			$('#header').css('position', 'fixed').css('top', '0');
			setTimeout(function(){
				$("#message_his").scroller().adjustScrollToBottom();
			},1000);
		});
		$el.bind('blur',function(){
			$('#header').css('position', 'relative');
			setTimeout(function(){
				$("#message_his").scroller().adjustScrollToBottom();
			},1000);
		});
	}
	window.ReplyBox = ReplyBox;
})($);