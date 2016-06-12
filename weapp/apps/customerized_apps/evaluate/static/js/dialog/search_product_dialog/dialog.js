/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 对话框
 */
ensureNS('W.dialog.app.evaluate');
W.dialog.app.evaluate.SearchProductDialog = W.dialog.Dialog.extend({
	events: _.extend({
		'click .xa-select': 'onClickSelect',
		'click .xa-submit-dialog': 'onClickSubmitButton'
	}, W.dialog.Dialog.prototype.events),
	
	templates: {
		dialogTmpl: '#app-evaluate-searchProductDialog-dialog-tmpl'
	},
	
	onInitialize: function(options) {
		this.table = this.$('[data-ui-role="advanced-table"]').data('view');
		product_arr = [];
	},
	
	beforeShow: function(options) {
		this.product_name = options.product_name;
		this.bar_code = options.bar_code;
		this.table.reset();
	},
	
	onShow: function(options) {
	},
	
	afterShow: function(options) {
		this.table.reload({"product_name": this.product_name,"bar_code": this.bar_code});
	},
	
	/**
	 * onGetData: 获取数据
	 */
	onGetData: function(event) {
		return product_arr;
	},

	onClickSelect: function(event){
		var $target = $(event.target);
		var $tr = $target.parents('tr');
		var id = $target.data('id');
		var bar_code = $tr.children('.xa-bar-code').text();
		var product_name = $tr.children('.xa-product-name').text();
		var price = $tr.children('.xa-price').text();
		var evaluate_count = $tr.children('.xa-evaluate-count').text()
		if ($target.text() == '选取') {
			$target.text('已选取').css('background-color', '#c9c9c9');
			product_arr.push({
				'id': id,
				'bar_code': bar_code,
				'product_name': product_name,
				'price': price,
				'evaluate_count': evaluate_count
			})
		} else {
			$target.text('选取').css('background-color', '#30ABF9');
			product_arr.pop({
				'id': id,
				'bar_code': bar_code,
				'product_name': product_name,
				'price': price,
				'evaluate_count': evaluate_count
			})
		}
	},

	/**
     * onClickSubmitButton: 点击“完成选择”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var data = this.onGetData(event);
		var content = $('#selected-products-tmpl').html();
		var template = Handlebars.compile(content);
		var context = {products:data};
		$('.xa-selected-products-table').html(template(context));
		this.$dialog.modal('hide');
    },
});
