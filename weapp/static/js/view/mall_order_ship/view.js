/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 登录的对话框
 * 
 * author: robert
 */
ensureNS('W.view.mall');
W.view.mall.MallOrderShipView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#logistics-info-view').template('logistics-info-view-dialog-tmpl');
        return "logistics-info-view-dialog-tmpl";
    },
    
    getOneTemplate: function() {
    	$('#single-logistics-info-view').template('single-logistics-info-view-dialog-tmpl');
        return "single-logistics-info-view-dialog-tmpl";
    },
    
     events:{
     	'click .tx_logistics_submit': 'submit'
    },

    initializePrivate: function(options) {
    },
    
    submit: function(event) {
    	var $el = $(event.currentTarget);
    	var validate = this.validate();
    	if(validate.is_submit) {
            // true为修改物流信息，只修改，不改变状态
            var is_update_express = this.express_company_value === -1 ? false : true;
            var logistics = $('select.ua-logistics').val();
    		var logistics_order_id = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
            var leader_name = $('input[name="leader_name"]').val();
    		$el.bottonLoading({status: 'show'});
    		window.location.href = '/mall/editor/order_express/add/?order_id=' + this.order_id + '&express_company_name=' + logistics + '&express_number=' + logistics_order_id + '&leader_name=' + leader_name+ '&is_update_express='+is_update_express;
    	} else {
    		$('div.error').text(validate.errMsg);
    	}
    },
    
    validate: function() {
    	var logistics = $('select.ua-logistics').val();
    	var order_id = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
    	var leader_name = $('input[name="leader_name"]').val(); 
        var validate = {};
        var errMsg = '';
    	if (logistics && order_id && leader_name) {
    		errMsg = '';
    		validate.is_submit = true;
    	}
        if (order_id == false) {
    		errMsg = '请输入定单号';
    		validate.is_submit = false;
            $('div.logistics_error').text(errMsg);
    	}
        if (leader_name.trim() == '') {
            errMsg = '请输入负责人';
            validate.is_submit = false;
            $('div.leader_name_error').text(errMsg);
        }
        validate.errMsg = errMsg;
    	return validate;
    	
    },
    
    getLogisticsInfo: function() {
    	var _this = this;
    	W.getApi().call({
    		app: 'tools',
    		api: 'express/companies/get',
    		args: {},
    		success: function(data) {
    			_this.render();
    			var $container = $('.ua-logistics');
    			for (var i=0; i<data.length; i++ ) {
    				var $option = $.tmpl(_this.getOneTemplate(), data[i]);
                    if(data[i]['value'] === _this.express_company_value){
                        $option.attr('selected','selected');
                    }
    				$container.append($option);
    			};

    		},
    		error: function() {
    		}
    	})
    },
    
    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
        $('input[name="logistics_order_id"]').val(this.express_number);
        $('input[name="leader_name"]').val(this.leader_name);
	},

    onShow: function(options) {
    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0'
    	})
    },
    
    showPrivate: function(options) {
    	this.order_id = options.order_id;
        this.express_company_value = options.express_company_value;
        this.express_number = options.express_number;
        this.leader_name = options.leader_name;
    	this.getLogisticsInfo();
	},

});


W.getMallOrderShipView = function(options) {
	var dialog = W.registry['W.view.mall.MallOrderShipView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.MallOrderShipView');
		dialog = new W.view.mall.MallOrderShipView(options);
		W.registry['W.view.mall.MallOrderShipView'] = dialog;
	}
	return dialog;
};