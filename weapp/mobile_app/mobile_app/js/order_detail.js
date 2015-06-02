var mask = mui.createMask(mycallback);//callback为用户点击蒙版时自动执行的回调；
mui.init();
var curr_view,order_id,reason;
mui.plusReady(function(){
	//重写back
	mui.back = function(){
		mui.currentWebview.close();
	};
	W.init();
	curr_view = plus.webview.currentWebview();
	order_id = curr_view.order_id;
	orderInfo(order_id);
})
function orderInfo(order_id){
	W.getJsonP(HOST_URL+'mobile_app/api/order/get/?id='+order_id,
			function(response){
				var order = baidu.template('order_template');
				var order_detail= order(response.data);
				$("#order_content").html(order_detail);
				shipOrder(order_id);
				$('#pay').one("click",function(){
					changeStatus(order_id,'pay');
				});
				$('#finish').one("click",function(){
					changeStatus(order_id,'finish');
				});
				//取消
//				document.querySelector('#cancel').addEventListener("tap",function(){
//					mask.show();
////					changeStatus(order_id,'cancel');
//				});
				$('#cancel_submit').bind('click',function(){
					changeStatus(order_id,'cancel');
				});
			},
			function(){
				mui.toast('获取订单详情失败，请重试...');
			}
	);
}
//发货
function shipOrder(order_id){
	var express_company_name = "";
	$('#ship').unbind();
	$('#ship').bind("click",function(){
	W.getJsonP(HOST_URL+'mobile_app/api/order_express_name/get/',
		function(response){
			mask.show();
			var express = baidu.template('order_express');
			var express_name= express(response);
			$("#main_info").html(express_name);

			showHide("main_info");
			$('#express_values').bind('click',function(){
				if($('#express_select').css('display') == 'none'){
					$('#express_select').css('display','block');
				}
				else{
					$('#express_select').css('display','');
				}
				mui('.mui-scroll-wrapper').scroll();
				$('.express_li').bind('click',function(){
					company_name = $(this).attr('express_value');
					$('#express_values').html(company_name);
					$('#express_select').css('display','');
				})
			});
			$("#express_submit").bind("click",function(){
				express_company_name = $('#express_values').text();
				var express_number = $("#express_id").val().trim();
				var leader_name = $("#leader_name").val().trim();
				var is_update_express = false;
				$('#express_id_error').text("");
				$('#leader_name_error').text("");
				if(express_number == "" || leader_name == ""){
					if (express_number == ""){
						$('#express_id_error').text("请输入快递单号！");
						shipOrder(order_id);
					}
					if (leader_name == ""){
						$('#leader_name_error').text("请输入发货人！");
						shipOrder(order_id);
					}
					return;
				}
				W.getJsonP(HOST_URL+'mobile_app/api/express_info/add/?order_id='+order_id+'&express_company_name='+express_company_name+'&express_number='+express_number+'&leader_name='+leader_name+'&is_update_express='+is_update_express,
					function(response){
						showHide("main_info");
						$("#express_info").removeClass('display_none');
						$("#express_info").html('物流信息：<div style="margin-left:65px;margin-top:-18px;word-break: break-all;">【'+express_company_name+'】'
							+express_number+'&nbsp;&nbsp;&nbsp;'+leader_name+'</a>');
						change_status ="已发货";
						color = "color:green";
						changeText(order_id,change_status,color);
						$("#order_action").html('<span id="finish" class="finish mui-btn mui-btn-success" >完成</span>');
						$('#finish').one("click",function(){
							changeStatus(order_id,'finish');
						});
					},
					function(){
					}
				);
				mask.close();
			})

		},
		function(){
		}
	);
});
}
function showHide(objToHide) {
    var el = $("#" + objToHide)[0];
    $(el).toggle();
}
//更新订单状态
function changeStatus(order_id,status){
	reason = $('#reason').val();
	if(status == 'cancel' && reason.trim() == '')return;
	W.getJsonP(HOST_URL+'mobile_app/api/order_status/update/?order_id='+order_id+'&action='+status+'&reason='+reason,
		function(){
			if(status == 'pay'){
				change_status ="待发货";
				color = "color:#FF0000";
				changeText(order_id,change_status,color);
				$("#order_action").html('<span id="ship" class="ship mui-btn mui-btn-success" >发货</span>');
				shipOrder(order_id);
			}
			if(status == 'finish'){
				change_status ="已完成";
				color = "color:green";
				changeText(order_id,change_status,color);
			}
			if(status == 'cancel'){
				change_status ="已取消";
				color = "color:#AFAFAF";
				changeText(order_id,change_status,color);
				$('#cancel_order').removeClass('mui-active');
				$('#cancel_action').html("");
//				$('#cancel_reason').html('取消原因：'+reason);
				//显示取消原因节点
				var cancle_dom = document.getElementById('cancle_reason');
				cancle_dom.style.display = 'block';
				cancle_dom.innerHTML = '取消原因：'+reason.trim();
			}
		},
		function(){
		}
	);
}
//更新订单时改变文字
function changeText(order_id,change_status,color){
	$("#order_action").html("");
	$("#express_order_statu").text("订单状态："+change_status);
	var orderView = plus.webview.getWebviewById('order.html');
	orderView.evalJS("changeText('"+order_id+"','"+color+"','"+change_status+"')");
}
function mycallback(){
	$('#select_values').removeClass('mui-active');
	$('#main_info').css('display','none');
	$('#cancel_order').css('display','none');
}
