var mask = mui.createMask(mycallback);//callback为用户点击蒙版时自动执行的回调；
var query="";
var filter_value="";
mui.ready(function(){
mui.init({
		pullRefresh: {
			container: '#orders',
			down: {
				contentdown : '下拉刷新',
				contentover : '释放刷新',
				contentrefresh : '正在刷新...',
				callback: pulldownRefresh
			}
		}
	});
/**
 * 下拉刷新具体业务实现
 */
function pulldownRefresh() {
	setTimeout(function() {
		order_count_curr_page = 1;
		showOrderList();
		mui('#pullrefresh').pullRefresh().endPulldownToRefresh(); //refresh completed
	}, 1000);
}
mui.plusReady(function(){
	W.init();
	showOrderList();

});
//加载订单列表
function showOrderList(){
	query = document.getElementById('query').value.trim();
	filter_value = $('#orderstatus').attr('filter_value');
	W.getJsonP(HOST_URL+'mobile_app/api/order_list/get/?cur_page='+order_count_curr_page+'&count='+order_count_per_page+'&query='+query+'&filter_value='+filter_value,
		function(response){
			if (response.code == 500 || query == "&"){
//				window.setTimeout(function(){
//					mui('#pullrefresh').pullRefresh().setStopped(true);
//				},200);
				$("#order_list_content").html("<div style='margin-top:10px;text-align:center;'>没有订单</div>");
				return;
			}
			$('#orderstatus').unbind('click');
			$('#orderstatus').bind('click',function(){
				if($('#select_values').attr('class') == "mui-popover mui-bar-popover"){
					$('#select_values').addClass('mui-active');
					mui('.mui-scroll-wrapper').scroll();
					mask.show();//显示遮罩
				}
				else{
					$('#select_values').removeClass('mui-active');
				}
			})
			var orderList = baidu.template('order_list_template');
			var content = orderList(response);
			$("#order_list_content").html(content);
			clickToOrderInfo();
			if (response.data.page_info.has_next){
				order_count_curr_page++;
				addLoadNextPage(order_count_per_page,query);
			}
			searchOrder();
		},function(){
			mui.toast('订单列表加载失败！');
		}
		);
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
		str +='<div class="mui-card"><ul class="mui-table-view"><li class="mui-table-view-cell">'+
			'<a class="order_id_link mui-navigate-right" order_id="'+order.id+'" ><b>订单号：'+order.order_id+'</b>'+
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
		str += '</a></li></ul></div>';
	});
	$("#order_list_content").append(str);


	clickToOrderInfo();

	searchOrder();

	order_count_curr_page ++;
	return response.data.page_info.has_next;


}

//显示加载更多
function addLoadNextPage(order_count_per_page,query){
	var load = new W.loadNextPageBtn({
		'url' : HOST_URL + 'mobile_app/api/order_list/get/?count='+order_count_per_page+'&query='+query+'&filter_value='+filter_value+'&cur_page=',
		'css_id' : 'order_list_content',
		'fn' : addOrderList,
		'page_name' : 'order_count_curr_page'
	});
	load.appendToTail();
}
function showOrderInfo(order_id){
	$("#order_content").html('');
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
			$('#cancel').bind("click",function(){
				changeStatus(order_id,'cancel');
			});
		},
		function(){
		}
	);
}
//按订单号进行搜索订单
function searchOrder(){
	$('.status_values').unbind('click');
	$('.status_values').bind('click',function(){
		filter_value = $(this).attr('filter_value');
		$('#orderstatus').attr('filter_value',filter_value);
		$('#orderstatus').html($(this).text());
		$('#select_values').removeClass('mui-active');
		order_count_curr_page=1;
		showOrderList();
		mask.close();//关闭遮罩
	})
	$('#order_id_search').unbind('click');
	$('#order_id_search').bind('click',function(){
		mask.close();
		$('#input_search').css('margin-left','0px');
		$('#input_search').width('55%');
		$('#filter_orderstatus').show();
		$('#filter').css('z-index','4');
		order_count_curr_page=1;
		showOrderList();
	});
}
//点击进入详情
function clickToOrderInfo(){
	$("#orders a").unbind("click");
	$("#orders a").bind("click",function(){
		var id = plus.webview.currentWebview().parent();
		var order_id = this.getAttribute('order_id');
        mui.openWindow({
		    url:'order_detail.html',
		    extras:{
		    	order_id:order_id
		    	//自定义扩展参数，可以用来处理页面间传值
		    },
		    show:{
		      autoShow:true,//页面loaded事件发生后自动显示，默认为true
		    },
		    waiting:{
		      autoShow:true,//自动显示等待框，默认为true
//		      title:'正在加载...',//等待对话框上显示的提示内容
		      options:{
		      }
		    }
		});
	});
}
document.querySelector('#query').addEventListener('focus',function(){
	$('#filter_orderstatus').hide();
	$('#input_search').css('margin-left','5px');
	$('#input_search').width('80%');
	$('#filter').css('z-index','999');
	mask.show();
});
});
function mycallback(){
	$('#select_values').removeClass('mui-active');
	$('#main_info').css('display','none');
	$('#input_search').css('margin-left','0px');
	$('#input_search').width('55%');
	$('#filter_orderstatus').show();
	$('#filter').css('z-index','4');
}

