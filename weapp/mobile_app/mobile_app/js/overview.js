//绘制流量统计图函数
function drawChart(url, title) {
	var itemDOM = $("#item1mobile");
	if(!itemDOM.find('.mui-loading')) {
		itemDOM.find('.mui-scroll').append('<div class="mui-loading"><div class="mui-spinner"></div></div>');
	}
	var chartDOM = '<div id="drewChart" style="width: 100%;height: 300px;"></div>';
	W.getJsonP(
		HOST_URL + url,
		function(data_json){
			var dom = $("#item1mobile").find('.mui-scroll');
			dom.html(chartDOM);
			//.dom.innerHTML = html;
			var data = data_json.data.data;
			var labels = data.x_axis.labels.labels;
			var chart_data = []
			for(var k = 0; k < data.elements.length; k++){
				var pointdatas = [];
				var line = {};
				line.color = data.elements[k].colour;
				line.type = "line";
				line.showInLegend = true;
				line.legendText = data.elements[k].text;
				for(var j = 0; j < data.elements[k].values.length; j++){
					data.elements[k].values[j].label = labels[j];
					pointdatas[j] = data.elements[k].values[j];
				}
				line.dataPoints = pointdatas;
				chart_data[k] = line;
			}

			chart_info = {
				title:{
					text: title,
					fontSize: 20,
				},

				axisX:{
					title: "日期",
					titleFontSize: 10,
				},

				axisY:{
					minimum: 0,
				},

				legend: {
					horizontalAlign: "left",
					verticalAlign: "top",
					fontSize: 10,
				}
			};

			chart_info.data = chart_data;

			var chart = new CanvasJS.Chart("drewChart", chart_info);
			chart.render();
			plus.nativeUI.closeWaiting();
			plus.navigator.closeSplashscreen();
			return true;
		},
		function(){
			plus.nativeUI.closeWaiting();
			plus.navigator.closeSplashscreen();
			mui.toast("网络或服务器错误，请稍后重试！");
		}
	);

}

//根据url的不同采取不同的操作
function url2action(url, name) {
	if(url == 'order_by_day'|| url == 'order_by_month') {
		template_name = "sale_statistic_by_day_or_month_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'order_by_week') {
		template_name = "sale_statistic_by_week_template";
		getOrderData(url, template_name, name)
	}
	if(url == 'order_by_status') {
		drewOrderClassified(url);
	}
	if(url == 'order_by_pay_type') {
		template_name = "order_pay_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'order_by_product') {
		template_name = "products_list_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'order_by_source') {
		template_name = "order_source_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'user_source_by_day') {
		template_name = "user_source_day_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'user_source_by_week') {
		template_name = "user_source_week_template";
		getOrderData(url, template_name, name);
	}
	if(url == 'user_static') {
		template_name = "user_source_template";
		getOrderData(url, template_name, name);
	}
}

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