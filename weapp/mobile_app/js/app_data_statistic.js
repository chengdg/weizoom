//获取一系列的统计数据
$.ui.ready(function(){
	$(".overview-header").bind("click", function(){
		$('.overview-header').removeClass("li_bottom");
		$("li.overview-header").css("color", "");
		$(this).css("color","#0088D1");
		$(this).addClass("li_bottom");
		var li_name = $(this).attr("name");
		switch(li_name){
			case "flow":
				gatGraphData();
				break;

			case "sale":
				var order_url = $(this).attr("data-statistic");
				var orderStatic = baidu.template('order_static_template');
				var select_data = '[{"value":"order_by_day","name":"按天统计"},{"value":"order_by_week","name":"按周统计"},{"value":"order_by_month","name":"按月统计"}]';
				var data={'data':$.parseJSON(select_data)};
				var static_content = orderStatic(data);
				$("#order_static_content").html(static_content);
				getOrderData("order_by_day","sale_statistic_by_day_or_month_template","saleView");
				$("#static_filter").change(function(){
					order_url = $("#static_filter").val().trim();
					if (order_url == "order_by_week"){
						getOrderData(order_url,'sale_statistic_by_week_template',"saleView");
					}else{
						getOrderData(order_url,'sale_statistic_by_day_or_month_template',"saleView");
					}
				});
				break;

			case "order":
				var select_data = '[{"value":"status","name":"状态统计"},{"value":"pay","name":"支付方式统计"},{"value":"product","name":"商品统计"},{"value":"source","name":"来源统计"}]';
				showChange(select_data,"orderView");
				break;

			case "member":
				var select_data = '[{"value":"day","name":"会员来源-按日统计"},{"value":"week","name":"会员来源-按周统计"},{"value":"user","name":"会员统计"}]';
				showChange(select_data,"memberView");
				break;
		}

	});
})

function drew_order_classified_chart(){
	$.ui.showMask("数据加载中...");
	var call_url = $("#orderClassified").attr("data-url");
	var chart_title = $("#orderClassified").attr("data-title");
	$("#flowView").html("");
	$("#saleView").html("");
	$("#memberView").html("");
	$.jsonP({
		url: HOST_URL + call_url,
		success: function(data_json){
			if (data_json.data.dataPoints ==""){
				$("#orderView").html("暂无数据");
				$.ui.hideMask();
				return;
			}
			var chart = new CanvasJS.Chart("chartOrderClassified",{
				title: {
					text: chart_title,
				},
				data: [{
					type: data_json.data.type,
					showInLegend: true,
					toolTipContent: "{legendText}:{y} - #percent %",
					dataPoints: data_json.data.dataPoints,
				}],

			});
			chart.render();
			$("#overview").scroller().scrollToTop();
			$.ui.hideMask();
		},
		error: function(){
			$.ui.hideMask();
		},
	})
}


function getOrderData(url,template,name){
	$.ui.showMask("数据加载中...");
	$("#flowView").html("");
	$("#orderView").html("");
	$("#memberView").html("");
	console.log("bug?");
	$.jsonP({
		url: HOST_URL + 'mobile_app/api/order_statistic/'+ url + '/get/',
		success: function(response){
			if (response.data.data==""){
				$("#"+name).html("暂无数据");
				$.ui.hideMask();
				return;
			}
			renderTemplate(url,template,response,name);
			$.ui.hideMask();
		},
		error: function(){
			$.ui.hideMask();
		},
	});
}
