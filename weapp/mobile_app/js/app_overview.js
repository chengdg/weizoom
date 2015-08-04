//向后台请求数据渲染“概览”页面的图表
$.ui.ready(function(){
	$("#get_graph_data_btn").click(function(){
		$("#flow").click();
	});
})
function gatGraphData(){
	initHeader();
	$("#pagination").html("");
	var orderStatic = baidu.template('order_static_template');
	var select_data = '[{"value":"order_daily_trend","name":"每日订单数"},{"value":"sale_daily_trend","name":"每日销售额"},{"value":"message_daily_trend","name":"每日接收消息数"},{"value":"visit_daily_trend","name":"每日微站访问数"}]';
	var data={'data':$.parseJSON(select_data)};
	var static_content = orderStatic(data);
	$("#order_static_content").html(static_content);
	var chart_url = $("#static_filter").val().trim()
	var chart_title = $("#static_filter [value="+chart_url+"]").text();
	drawChart(chart_url,chart_title);
	$("#static_filter").change(function(){
		chart_url = $("#static_filter").val().trim()
		chart_title = $("#static_filter [value="+chart_url+"]").text();
		drawChart(chart_url,chart_title);
	});
	var flow_html = $("#flow_part_statistic").text();
	$("#flowView").html(flow_html);
	$("#pagination").html("");
	$("#meun_statistic").show();
	// var chart_divs = $(".chart");
	// chart_divs.forEach(function(div){
	// 	var chart_div = $("#" + div.id);
	// 	var chart_title = chart_div.attr("data-title");
	// 	var chart_url = chart_div.attr("data-url");
	// 	var chart_args = JSON.parse(chart_div.attr("data-args"));
	// 	var chart_id = chart_div.children("div").attr("id");
	// 	$.ui.showMask("正在加载数据,请稍后...");
	// 	$.jsonP({
	// 		url: HOST_URL + chart_url + "?days=" + chart_args["days"],
	// 		success:function(data_json){
	// 			$("#error_message").hide();
	// 			var data = data_json.data.data;
	// 			var labels = data.x_axis.labels.labels;
	// 			var chart_data = []
	// 			for(var k = 0; k < data.elements.length; k++){
	// 				var pointdatas = [];
	// 				var line = {};
	// 				line.color = data.elements[k].colour;
	// 				line.type = "line";
	// 				line.showInLegend = true;
	// 				line.legendText = data.elements[k].text;
	// 				for(var j = 0; j < data.elements[k].values.length; j++){
	// 					data.elements[k].values[j].label = labels[j];
	// 					pointdatas[j] = data.elements[k].values[j];
	// 				}
	// 				line.dataPoints = pointdatas;
	// 				chart_data[k] = line;
	// 			}

	// 			chart_info = {
	// 				title:{
	// 					text: chart_title,
	// 					fontSize: 20,
	// 				},

	// 				axisX:{
	// 					title: "日期",
	// 					titleFontSize: 10,
	// 				},

	// 				axisY:{
	// 					minimum: 0,
	// 				},

	// 				legend: {
	// 					horizontalAlign: "left",
	// 					verticalAlign: "top",
	// 					fontSize: 10,
	// 				}
	// 			};

	// 			chart_info.data = chart_data;

	// 			var chart = new CanvasJS.Chart(chart_id, chart_info);
	// 			chart.render();
	// 			$.ui.hideMask();
	// 			return true;
	// 		},
	// 		error:function(){
	// 			$.ui.hideMask();
	// 			showErrorMessage();
	// 		}
	// 	})
	// });
}


function drawChart(chart_url,chart_title){
		$.ui.showMask("正在加载数据,请稍后...");
		$("#saleView").html("");
		$("#orderView").html("");
		$("#memberView").html("");
		$.jsonP({
			url: HOST_URL +'mobile_app/api/'+chart_url + "/get/?days=7",
			success:function(data_json){
				$("#error_message").hide();
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
						text: chart_title,
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
				$("#overview").scroller().scrollToTop();
				$.ui.hideMask();
				return true;
			},
			error:function(){
				$.ui.hideMask();
				showErrorMessage();
			}
		});
}
