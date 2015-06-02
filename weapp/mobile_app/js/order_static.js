function changeSelect(name){
	$("#pagination").html("");
	var static_name = $("#static_filter").val().trim();
	var url = "";
	var template_name = "";
	if(static_name == 'status'){
		var order_info  = $("#order_classified").text();
		$("#"+name).html(order_info);
		drew_order_classified_chart();
	}
	if(static_name == 'pay'){
		url = "order_by_pay_type";
		template_name = "order_pay_template";
		staticJsonp(url,template_name,name);
	}
	if(static_name == 'product'){
		url = "order_by_product";
		template_name = "products_list_template";
		staticJsonp(url,template_name,name);
	}
	if(static_name == 'source'){
		url = "order_by_source";
		template_name = "order_source_template";
		staticJsonp(url,template_name,name);
	}
	if(static_name == 'day'){
		url = "user_source_by_day";
		template_name = "user_source_day_template";
		staticJsonp(url,template_name,name);
	}
	if(static_name == 'week'){
		url = "user_source_by_week";
		template_name = "user_source_week_template";
		staticJsonp(url,template_name,name);
	}
	if(static_name == 'user'){
		url = "user_static";
		template_name = "user_source_template";
		staticJsonp(url,template_name,name);
	}
}
function staticJsonp(url,template_name,name){
	$.ui.showMask("数据加载中...");
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order_statistic/'+url+'/get/',
		success:function(response){
			renderTemplate(url,template_name,response,name);
			$.ui.hideMask();
		},
		error:function(){
			$.ui.hideMask();
			showErrorMessage();
		}
	});
}
function showChange(select_data,name){
	var orderStatic = baidu.template('order_static_template');
	var select={'data':$.parseJSON(select_data)};
	var static_content = orderStatic(select);
	$("#order_static_content").html(static_content);
	changeSelect(name);
	$("#static_filter").change(function(){
		changeSelect(name);
	});
}
function goToPage(url,template_name,page,name){
	$.jsonP({
		url:HOST_URL+'mobile_app/api/order_statistic/'+url+'/get/?page='+page+'&count_per_page='+count_per_page,
		success:function(response){
			renderTemplate(url,template_name,response,name);
			$.ui.hideMask();
		},
		error:function(){
			$.ui.hideMask();
			showErrorMessage();
		}
	});
}
function renderTemplate(url,template_name,response,name){
	$("#flowView").html("");
	$("#saleView").html("");
	$("#orderView").html("");
	$("#memberView").html("");
	if (response.data.data==""){
		$("#"+name).html("暂无数据");
		return;
	}
	if (url == 'order_by_day'){
		console.log(response.data.data[0]);
		console.log(template_name);
		for(var i=0; i < response.data.data.length; i++){
			response.data.data[i][0] = response.data.data[i][0].split("-");
		}
	}
	var orderPay = baidu.template(template_name);
	var order_pay_content = orderPay(response.data);
	$("#"+name).html(order_pay_content);
	var pageinfo = baidu.template("pagination_template");
	if(template_name == "user_source_template"){
		if (response.data.table_data.data_lines == ""){
			$("#"+name).html("暂无数据");
			return;
		}
		var pageinfo_content = pageinfo(response.data.table_data.pageinfo);
		$("#pagination").html(pageinfo_content);
		$("#pagination li a").bind("click",function(){
			if($(this).parent().attr("class") != "disabled"){
				page = $(this).attr('page');
				goToPage(url,template_name,page,name);
			}
		});
	}else{
		var pageinfo_content = pageinfo(response.data.page_info);
		$("#pagination").html(pageinfo_content);
		$("#pagination li a").bind("click",function(){
			if($(this).parent().attr("class") != "disabled"){
				page = $(this).attr('page');
				goToPage(url,template_name,page,name);
			}
		});
	}
	$("#overview").scroller().scrollToTop();

}
