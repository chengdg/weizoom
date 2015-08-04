$.ui.ready(function(){
	var change_status ="";//订单状态
	var color = "";//订单状态的颜色
	var query = "";//搜索的订单号
	var filter_value = $("#filter").val().trim();//订单状态的筛选值
	$('#get_order_list_btn').bind('click',function(){
		$("#filter").val("-1");
		$('#search_order_id').val("");
		showOrderList();
		scroll_to_refresh('#orders',showOrderList);
	});
	//绑定click清空搜索框的内容
	$('#clear_order_id').bind('click',function(){
		$("#search_order_id").val("");
	});
	//订单的状态的筛选
	$('#filter').bind('change',function(){
		showOrderList();
	})
});

//显示订单列表
function showOrderList(){
	order_count_curr_page = 1;
	query = trim($('#search_order_id').val());
	filter_value = $("#filter").val().trim();
	initHeader();
	$("#search_order").css("display","block");
	$.ui.showMask('加载订单列表...');
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order_list/get/?cur_page='+order_count_curr_page+'&count='+order_count_per_page+'&query='+query+'&filter_value='+filter_value,
		success:function(response){
			$.ui.hideMask();
			if (response.code == 500){
				$("#order_list_content").html("<div style='margin-top:10px;text-align:center;'>没有订单</div>");
				return;
			}
			$("#error_message").hide();
			var orderList = baidu.template('order_list_template');
			var content = orderList(response);
			$("#order_list_content").html(content);
			$("#orders").scroller().scrollToTop();
			clickToOrderInfo();

			if (response.data.page_info.has_next){
				order_count_curr_page++;
				addLoadNextPage(order_count_per_page,query);
			}

			searchOrder();
		},
		error:function(){
			$.ui.hideMask();
			showErrorMessage();
		}
	});
}

//按订单号进行搜索订单
function searchOrder(){
	$('#order_id_search').bind('click',function(){
		$('#order_id_search').unbind('click');
		initHeader();
		$("#search_order").css("display","block");
		query = trim($('#search_order_id').val());
		filter_value = $("#filter").val().trim();
		$.ui.showMask('加载订单...');
		$("#order_list_content").html('');
		$("#orders").scroller().scrollToTop();
		order_count_curr_page =1;
		$.jsonP({
			url:HOST_URL+'mobile_app/api/order_list/get/?cur_page='+order_count_curr_page+'&count='+order_count_per_page+'&query='+query+'&filter_value='+filter_value,
			success:function(response){
				$.ui.hideMask();
				if (response.code == 500 || query == "&"){
					$("#order_list_content").html("<div style='margin-top:10px;text-align:center;'>没有订单</div>");
					return;
				}
				$("#error_message").hide();
				var orderList = baidu.template('order_list_template');
				var content = orderList(response);
				$("#order_list_content").html(content);
				clickToOrderInfo();

				if (response.data.page_info.has_next){
					order_count_curr_page++;
					addLoadNextPage(order_count_per_page,query);
				}
			},
			error:function(){
				$.ui.hideMask();
				showErrorMessage();
			}
		});
		searchOrder();
	});
}

//显示加载更多
function addLoadNextPage(order_count_per_page,query){
	var load = new loadNextPageBtn({
		'url' : HOST_URL + 'mobile_app/api/order_list/get/?count='+order_count_per_page+'&query='+query+'&filter_value='+filter_value+'&cur_page=',
		'css_id' : 'order_list_content',
		'fn' : addOrderList,
		'page_name' : 'order_count_curr_page'
	});
	load.appendToTail();
}

//执行加载更多
function addOrderList(response){
	var str="";
	$.each(response.data.orders,function(i,order){
		var style="",come = "";
		if (order.status == "待支付" || order.status == "待发货"){
			style ='style="color:#FF0000;"';
		}
		else if (order.status == "已发货" || order.status == "已完成"){
			style ='style="color:green;"';
		}
		else if (order.status == "已取消") {
			style ='style="color:#AFAFAF;"';
		}
		str +='<ul class="list inset" style="margin-bottom:10px;background-color:#f6f9fe;"><li>'+
			'<a class="order_id_link" href="#order_co" order_id="'+order.id+'" ><b>订单号：'+order.order_id+'</b>'+
			'<div class="tab">金额：￥'+order.total_price+'</div><div class="tab">购买人：'+order.buyer_name+'</div>'+
			'<div class="tab">下单时间：'+order.created_at+'</div><div class="tab">支付方式：'+order.pay_interface_name+'</div>'+
			'<div class="tab order_status">订单状态：<span '+style+'>'+order.status+'</span></div><div class="tab">付款时间：'+order.payment_time+'</div>'
		if (response.data.is_show_source){
			str +='<div class="tab">来源：';
			if (order.come == "weizoom_mall"){
				str += '商户';
			}else {
				str +='本店';
			}
			str +='</div>';
		}
		str += '</a></li></ul>';
	});
	$("#order_list_content").append(str);
	// $("#orders").scroller().scrollToBottom();

	clickToOrderInfo();

	searchOrder();

	$.ui.hideMask();
	order_count_curr_page ++;
	return response.data.page_info.has_next;


}

//点击进入详情
function clickToOrderInfo(){
	$("#orders a").unbind("click");
	$("#orders a").bind("click",function(){
        $('#menubadge').hide();
        $.ui.slideSideMenu = false;
		var order_id = this.getAttribute('order_id');
		saveLastVisitPosition(orders);
		showOrderInfo(order_id);
	});
}

//订单详情
function showOrderInfo(order_id){
	$("#backButton").show();
	$("#search_order").css("display","none");
	$('#backButton').unbind('click');
	$('#backButton').bind('click',function(event){
        $.ui.slideSideMenu = true;
		$("#search_order").css("display","block");
		$('#backButton').hide();
        $('#menubadge').show();
		//返回时，回到之前浏览的位置
		var ordersScroller = $("#orders").scroller();
		var curScrollTop = $("#orders").attr('scrollTop');
		event.stopPropagation();
		$.ui.goBack();
		ordersScroller.scrollTo({x:0,y:curScrollTop});
	});
	$("#order_content").html('');
	$.ui.showMask('刷新订单详情...');
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order/get/?id='+order_id,
		success:function(response){
			$("#error_message").hide();
			$("#search_order").css("display","none");
			var order = baidu.template('order_template');
			var order_detail= order(response.data);
			$("#order_content").html(order_detail);
			$.ui.hideMask();
			$("#backButton").show();
			shipOrder(order_id);
			$('#pay').one("click",function(){
				changeStatus(order_id,'pay');
			});
			$('#finish').one("click",function(){
				changeStatus(order_id,'finish');
			});
			$('#cancel').bind("click",function(){
				changeStatus(order_id,'cancel');
			});
		},
		error: function(){
			$.ui.hideMask();
			showErrorMessage();
		}
	});
}
function showHide(objToHide) {
    var el = $("#" + objToHide)[0];
    $(el).toggle();
}

//发货
function shipOrder(order_id){
	$('#ship').unbind();
	$('#ship').bind("click",function(){
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order_express_name/get/',
		success:function(response){
			var express = baidu.template('order_express');
			var express_name= express(response);
			$("#main_info").html(express_name);
			showHide("main_info");
			$("#express_submit").bind("click",function(){
				var express_company_name = $("#express_select").val();
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
				$.jsonP({
					url:HOST_URL+'mobile_app/api/express_info/add/?order_id='+order_id+'&express_company_name='+express_company_name+'&express_number='+express_number+'&leader_name='+leader_name+'&is_update_express='+is_update_express,
					success:function(response){
						showHide("main_info");
						$("#express_info").html('物流信息：<a>【'+express_company_name+'】'
							+express_number+'&nbsp;&nbsp;&nbsp;'+leader_name+'</a>');
						change_status ="已发货";
						color = "color:green";
						changeText(order_id,change_status,color);
						$("#order_action").html('<span id="finish" class="finish button  green" >完成</span>');
						$('#finish').one("click",function(){
							changeStatus(order_id,'finish');
						});
					},
					error:function(){
					}
				});
			})
		},
		error: function(){
		}
	});
});
}
//更新订单状态
function changeStatus(order_id,status){
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order_status/update/?order_id='+order_id+'&action='+status,
		success:function(){
			if(status == 'pay'){
				change_status ="待发货";
				color = "color:#FF0000";
				changeText(order_id,change_status,color);
				$("#order_action").html('<span id="ship" class="ship button  green" >发货</span>');
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
			}
		},
		error:function(){
		}
	});
}
//更新订单时改变文字
function changeText(order_id,change_status,color){
	$("#order_action").html("");
	$("#express_order_statu").text("订单状态："+change_status);
	$("#orders a[order_id='"+order_id+"'] .order_status").html('订单状态：<span style='+color+'>'+change_status+'</span>');
}
