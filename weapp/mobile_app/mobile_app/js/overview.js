//加载概览页
function drawChart(url, title) {
	var itemDOM = $("#item1mobile");
	if(!itemDOM.find('.mui-loading')) {
		itemDOM.find('.mui-scroll').append('<div class="mui-loading"><div class="mui-spinner"></div></div>');
	}
	var chartDOM = '<div id="drewChart" style="width: 100%;height: 300px;"></div>';
	plus.nativeUI.closeWaiting();
	plus.navigator.closeSplashscreen();
}

//根据url的不同采取不同的操作
function url2action(url, name) {
	switch(url){
		case ('order_by_day'|| 'order_by_month'):
			template_name = "sale_statistic_by_day_or_month_template";
			getOrderData(url, template_name, name);
			break;
		case 'order_by_week':
			template_name = "sale_statistic_by_week_template";
			getOrderData(url, template_name, name)
			break;
		case 'order_by_status':
			drewOrderClassified(url);
			break;
		case'order_by_pay_type':
			template_name = "order_pay_template";
			getOrderData(url, template_name, name);
			break;
		case 'order_by_product':
			template_name = "products_list_template";
			getOrderData(url, template_name, name);
			break;
		case 'order_by_source':
			template_name = "order_source_template";
			getOrderData(url, template_name, name);
			break;
		case 'user_source_by_day':
			template_name = "user_source_day_template";
			getOrderData(url, template_name, name);
			break;
		case 'user_source_by_week':
			template_name = "user_source_week_template";
			getOrderData(url, template_name, name);
			break;
		case 'user_static':
			template_name = "user_source_template";
			getOrderData(url, template_name, name);
			break;
		}
	}
//	if(url == 'order_by_day'|| url == 'order_by_month') {
//		template_name = "sale_statistic_by_day_or_month_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'order_by_week') {
//		template_name = "sale_statistic_by_week_template";
//		getOrderData(url, template_name, name)
//	}
//	if(url == 'order_by_status') {
//		drewOrderClassified(url);
//	}
//	if(url == 'order_by_pay_type') {
//		template_name = "order_pay_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'order_by_product') {
//		template_name = "products_list_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'order_by_source') {
//		template_name = "order_source_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'user_source_by_day') {
//		template_name = "user_source_day_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'user_source_by_week') {
//		template_name = "user_source_week_template";
//		getOrderData(url, template_name, name);
//	}
//	if(url == 'user_static') {
//		template_name = "user_source_template";
//		getOrderData(url, template_name, name);
//	}
//}

function getOrderData(url,template,name) {
	var dom = $('#'+name).find(".mui-scroll");
	W.getJsonP(
		HOST_URL + 'mobile_app/api/order_statistic/'+ url + '/get/',
		function(response) {
			dom.html("");
			if (response.data.data==""){
				dom.html("暂无数据");
				return;
			}
			renderTemplate(url,template,response,name);//渲染模板
		},
		function(){
			mui.toast("网络或服务器错误，请稍后重试！");
		}
	)
}

function renderTemplate(url,template_name,response,name) {
	var dom = $('#'+name).find(".mui-scroll");
	if (response.data.data==""){
		return;
	}
	if (url == 'order_by_day'){
		for(var i=0; i < response.data.data.length; i++){
			response.data.data[i][0] = response.data.data[i][0].split("-");
		}
	}
	var orderPay = baidu.template(template_name);
	var order_pay_content = orderPay(response.data);
	dom.html(order_pay_content);
	mui('.mui-scroll-wrapper').scroll()[name[4]-1].scrollTo(0,0);
	//翻页展示
	var pageinfo = baidu.template("pagination_template");
	if(template_name == "user_source_template"){
		if (response.data.table_data.data_lines == "") {
			dom.html("暂无数据");
			return;
		}
		var pageinfo_content = pageinfo(response.data.table_data.pageinfo);
		dom.append(pageinfo_content);
		$(".mui-content-padded li a").bind("click",function() {
			plus.nativeUI.showWaiting();
			if($(this).parent().attr("class") != "mui-disabled") {
				page = $(this).attr('page');
				goToPage(url,template_name,page,name);
			}
			plus.nativeUI.closeWaiting();
		});
	}else{
		var pageinfo_content = pageinfo(response.data.page_info);
		dom.append(pageinfo_content);
		$(".mui-content-padded li a").bind("click",function(){
			plus.nativeUI.showWaiting();
			if($(this).parent().attr("class") != "mui-disabled") {
				page = $(this).attr('page');
				goToPage(url,template_name,page,name);
			}
			plus.nativeUI.closeWaiting();
		});
	}
}

//绘制订单分类详情统计图
function drewOrderClassified(url) {
	W.getJsonP(
		HOST_URL + 'mobile_app/api/order_statistic/'+ url + '/get/',
		function(response){
			if (response.data.dataPoints ==""){
				$("#item3mobile").find('.mui-scroll').html("暂无数据");
				return;
			}else{
				$("#item3mobile").find('.mui-scroll').html('<div id="chartOrderClassified" style="height: 300px; width: 100%;"></div>');
				var chart = new CanvasJS.Chart("chartOrderClassified",{
					title: {
						text: "订单分类详情",
					},
					data: [{
						type: response.data.type,
						showInLegend: true,
						toolTipContent: "{legendText}:{y} - #percent %",
						dataPoints: response.data.dataPoints,
					}],

				});
				chart.render();
			}
		},
		function() {
			mui.toast("网络或服务器错误，请稍后重试！");
		}
	)
}
function goToPage(url,template_name,page,name) {
	W.getJsonP(
		HOST_URL+'mobile_app/api/order_statistic/'+url+'/get/?page='+page+'&count_per_page='+count_per_page,
		function(response) {
			renderTemplate(url,template_name,response,name);
		},
		function() {
			mui.toast("网络或服务器错误，请稍后重试！");
		}
	);
}

var brandChart;
var saleChart;
var orderChart;
var message_count = 0;
var message_interval;
function getFirstTabData(){
	overview_board();
	getBrandData();
	getSalesData();
	getOrderData();
}

function overview_board(){
	window.clearInterval(message_interval);
	W.getJsonP(
		HOST_URL + 'mobile_app/api/stats/overview_board/',
		function(resp){
			if(resp.code == 200){
				var data = resp.data;
				document.getElementById('brand_value').innerText = data ? (data.brand_value || 0) : 0;
				document.getElementById('subscribed_member_count').innerText = data.subscribed_member_count || 0;
				document.getElementById('all_deal_order_money').innerText = data.all_deal_order_money || 0;
				document.getElementById('all_deal_order_count').innerText = data.all_deal_order_count || 0;
				document.getElementById('today_deal_money').innerText = data.today_deal_money || 0;
				document.getElementById('today_deal_order_count').innerText = data.today_deal_order_count || 0;
				document.getElementById('total_to_be_shipped_order_count').innerText = data.total_to_be_shipped_order_count || 0;
				document.getElementById('total_refunding_order_count').innerText = data.total_refunding_order_count || 0;
				//从本地存储中获取未读消息数
				message_interval = window.setInterval(function(){
					message_count = plus.storage.getItem('message_count');
					if(message_count || message_count == 0){
						W('#today_unread_message_count').innerText = message_count;
					}
				},message_auto_update_time);
			}else{
				mui.toast("网络或服务器错误，请稍后重试！");
			}
		}
	);

}
//微品牌价值趋势
function getBrandData(freq_type) {
	freq_type = freq_type || 'W';
	brandChart = brandChart || echarts.init(document.getElementById('brandChart'));
	W.getJsonP(
		HOST_URL + 'mobile_app/api/stats/brand_value/?freq_type='+freq_type,
		function(resp){
			if(resp.code == 200){
				formatChartDisplay(brandChart, resp.data, '微品牌价值趋势图');
			}else{
				mui.toast("网络或服务器错误，请稍后重试！");
			}
		}
	);
}


//订单价值趋势图
function getOrderData(freq_type){
	var btn = W('.xa-order-chart-btn');
	freq_type = freq_type || 'W';
	orderChart = orderChart || echarts.init(document.getElementById('orderChart'));
	W.getJsonP(
		HOST_URL + 'mobile_app/api/stats/order_value/?freq_type='+freq_type,
		function(resp){
			if(resp.code == 200){
				formatChartDisplay(orderChart, resp.data, '订单趋势图');
				btn.style.display = 'none';
			}else{
				mui.toast("网络或服务器错误，请稍后重试！");
			}
		}
	);
}

//销售价值趋势图
function getSalesData(freq_type) {
	var btn = W('.xa-sale-chart-btn');
	freq_type = freq_type || 'W';
	saleChart = saleChart || echarts.init(document.getElementById('saleChart'));
	W.getJsonP(
		HOST_URL + 'mobile_app/api/stats/sales_chart/get/?freq_type='+freq_type,
		function(resp){
			if (resp.code == 200){
				formatChartDisplay(saleChart, resp.data, '销售趋势图');
				btn.style.display = 'none';
			}else{
				mui.toast("网络或服务器错误，请稍后重试！");
			}

		}
	);
}

function formatChartDisplay(chart,chartData,title){
	chart.clear();
//	chartData.title = {text: title};
	chartData.grid = {
		x: '13%',
		x2: '4%',
		y: '12%',
		y2: '8%'
	};
	chartData.xAxis.splitLine = {show :false};
	delete chartData.legend;
	delete chartData.toolbox;
	delete chartData.calculable;
	chart.setOption(chartData);
	plus.nativeUI.closeWaiting();
}

