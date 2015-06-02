/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 发货的对话框
 *
 * author: liupeiyu
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
        'click .xa-submit': 'onClickSubmit',
     	'click .xa-close': 'onClickClose',
        'click .xa-is-need-logistics': 'onClickIsNeedLogistics'
    },

    initializePrivate: function(options) {
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    },

    onClickSubmit: function(event) {
    	var $el = $(event.currentTarget);
    	var validate = this.validate();
    	if(validate.is_submit) {
            // true为修改物流信息，只修改，不改变状态
            var isUpdateExpress = this.expressCompanyValue === -1 ? false : true;
            var logistics = $('select.ua-logistics').val();
    		var logisticsOrderId = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
            var leaderName = $('input[name="leader_name"]').val();
    		$el.bottonLoading({status: 'show'});

            // 是否需要物流
            var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
            if(isNeedLogistics === '0'){
                // 不需要物流
                var args = {
                    'order_id': this.orderId,
                    'express_company_name': '0',
                    'express_number': -1,
                    'leader_name': -1,
                    'is_update_express': isUpdateExpress
                }
                window.location.href = '/mall/order/update/?order_id='+this.orderId+'&action=finish';
            }else{
                // 需要物流
                var args = {
                    'order_id': this.orderId,
                    'express_company_name': logistics,
                    'express_number': logisticsOrderId,
                    'leader_name': leaderName,
                    'is_update_express': isUpdateExpress
                }
                this.submitSendApi(args);
            }
    		// window.location.href = '/mall/editor/order_express/add/?order_id=' +
      //       this.orderId + '&=' + logistics + '&express_number=' + logisticsOrderId +
      //        '&leader_name=' + leaderName+ '&is_update_express='+isUpdateExpress;
    	} else {
    		$('div.xa-error').text(validate.errMsg);
    	}
    },

    onClickClose: function(event) {
        event.stopPropagation();
        event.preventDefault();
        this.hide(event);
    },

    submitSendApi: function(args){
        W.getApi().call({
            app: 'mall',
            api: 'order_delivery/update',
            args: args,
            success: function(data) {
                window.location.reload();
            },
            error: function() {
            }
        })
    },

    validate: function() {
        // 是否需要物流
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
    	var logistics = $('select.ua-logistics').val();
    	var orderId = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
    	//var leaderName = $('input[name="leader_name"]').val();
        var validate = {};
        var errMsg = '';
        if(isNeedLogistics === '0'){
            // 不需要物流
            return {
                errMsg: errMsg,
                is_submit : true
            }
        }else{
            // 需要物流
            if (logistics && orderId) {
                errMsg = '';
                validate.is_submit = true;
            }
            if (orderId == false) {
                errMsg = '请输入快递单号';
                validate.is_submit = false;
                $('div.xa-error').removeClass('hidden').text(errMsg);
            }
            // if (leaderName.trim() == '') {
            //     errMsg = '请输入负责人';
            //     validate.is_submit = false;
            //     $('div.xa-error').text(errMsg);
            // }
            validate.errMsg = errMsg;
            return validate;
        }
    },

    getLogisticsInfo: function() {
    	var _this = this;
    	W.getApi().call({
    		app: 'mall',
    		api: 'shipping_express_companies/get',
    		args: {},
    		success: function(data) {
    			_this.render();
    			var $container = $('.ua-logistics');
    			for (var i=0; i<data.length; i++ ) {
    				var $option = $.tmpl(_this.getOneTemplate(), data[i]);
                    if(data[i]['value'] === _this.expressCompanyValue){
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
        if (this.expressCompanyValue === '0') {
            this.expressCompanyValue = ''
            this.expressNumber = ''
            this.leaderName = ''
            $('[name="is_need_logistics"]')[0].checked = false
            $('[name="is_need_logistics"]')[1].checked = true
            $('.xa-ship-detail-from').hide();
        }else{
            $('[name="is_need_logistics"]')[0].checked = true
            $('[name="is_need_logistics"]')[1].checked = false
            $('.xa-ship-detail-from').show();
        }
        $('input[name="logistics_order_id"]').val(this.expressNumber);
        $('input[name="leader_name"]').val(this.leaderName);
        this.updateInfo();
	},

    onShow: function(options) {
    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0'
    	})
    },

    showPrivate: function(options) {
    	this.orderId = options.orderId;
        this.expressCompanyValue = options.expressCompanyValue;
        this.expressNumber = options.expressNumber;
        this.leaderName = options.leaderName;
    	this.getLogisticsInfo();
        // this.$content.html($.tmpl(this.getTemplate()));
	},

    updateInfo: function(){
        if(this.expressCompanyValue == -1 || this.expressCompanyValue == 0){
            $('.xa-spetialState').show();
        }else{
            $('.xa-spetialState').hide();
        }
    },

    onClickIsNeedLogistics: function(event){
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
        if (isNeedLogistics === '1') {
            $('.xa-ship-detail-from').show();
            $('.xa-error').addClass('hidden');
        }else{
            $('.xa-ship-detail-from').hide();
        }
    }

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
