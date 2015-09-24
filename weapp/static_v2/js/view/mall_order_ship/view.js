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
                logistics = '';
                logisticsOrderId = '';
            }
            var args = {
                'order_id': this.orderId,
                'express_company_name': logistics,
                'express_number': logisticsOrderId,
                'leader_name': leaderName,
                'is_update_express': isUpdateExpress
            }

            W.getApi().call({
                method: 'post',
                app: 'mall2',
                resource: 'delivery',
                args: args,
                success: function(data) {
                    $(".xa-shipDropBox").hide();
                    if($('[data-ui-role="advanced-table"]').length>0){
                        $('[data-ui-role="advanced-table"]').data('view').reload();
                    }
                    else {
                        window.location.reload();
                    }
                    common_interval_check_func();
                },
                error: function(data) {
                    W.getErrorHintView().show(data.errMsg);
                    var t=setTimeout("window.location.reload()",2000)
                    //$('[data-ui-role="advanced-table"]').data('view').reload();
                }
            });

    	} else {
    		$('div.xa-error').text(validate.errMsg);
    	}
    },

    onClickClose: function(event) {
        event.stopPropagation();
        event.preventDefault();
        this.hide(event);
    },





    validate: function() {
        // 是否需要物流
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
    	var logistics = $('select.ua-logistics').val();
    	var logisticsOrderId = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
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
            if (logistics && logisticsOrderId) {
                errMsg = '';
                validate.is_submit = true;
            }
            if (logisticsOrderId == false || !/^\w+$/.test(logisticsOrderId)) {
                errMsg = '请输入正确的快递单号';
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
    		app: 'mall2',
    		resource: 'express_delivery_company',
    		args: {'source':'shipping_express_companies'},
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
