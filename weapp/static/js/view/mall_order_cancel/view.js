/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单取消
 * 
 * author: bert
 */
ensureNS('W.view.mall');
W.view.mall.MallOrderCancelView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#order_cancel_reason').template('order_cancel_reason-dialog-tmpl');
        return "order_cancel_reason-dialog-tmpl";
    },
    
    getOneTemplate: function() {
    	$('#single-order_cancel_reason').template('single-order_cancel_reason-dialog-tmpl');
        return "single-order_cancel_reason-dialog-tmpl";
    },
    
    events:{
     	'click .tx_logistics_submit': 'submit'
    },

    initializePrivate: function(options) {
        this.render();
    },
    
    submit: function(event) {
    	var $el = $(event.currentTarget);
        var reason = $.trim($("#reason").val());
        this.close();
        W.getLoadingView().show();
        window.location.href = '/mall/editor/order_status/update/?action=cancel&order_id=' + this.order_id + '&reason='+reason;
    	/*var validate = this.validate();
    	if(validate.is_submit) {
            var reason = $('input[name="reason"]').val();
    		$el.bottonLoading({status: 'show'});
          
    		window.location.href = '/mall/editor/order_status/update/?order_id=' + this.order_id + '&express_company_name=' + logistics + '&express_number=' + logistics_order_id + '&leader_name=' + leader_name+ '&is_update_express='+is_update_express;
    	} else {
    		$('div.error').text(validate.errMsg);
    	}*/
    },
    
  /*  validate: function() {
    	var reason = $('#reason').val(); 
        var validate = {};
        var errMsg = '';
        validate.is_submit = true;
        if ($.trim(reason) == '') {
            errMsg = '请输入原因';
            validate.is_submit = false;
            $('div.reason_error').text(errMsg);
        }
        validate.errMsg = errMsg;
    	return validate;
    	
    },
    */
    
    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},

    onShow: function(options) {
    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0',
    	})
    },
    
    showPrivate: function(options) {
    	this.order_id = options.order_id;
    //    this.leader_name = options.leader_name;
   // 	this.getLogisticsInfo();
	},

});


W.getMallOrderCancelView = function(options) {
	var dialog = W.registry['W.view.mall.MallOrderCancelView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.MallOrderCancelView');
		dialog = new W.view.mall.MallOrderCancelView(options);
		W.registry['W.view.mall.MallOrderCancelView'] = dialog;
	}
	return dialog;
};