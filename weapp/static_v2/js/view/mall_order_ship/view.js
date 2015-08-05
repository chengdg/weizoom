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
                // 不需要物流
                // 向order发送finish
                var args = {
                    'order_id': this.orderId,
                    'action': 'finish'
                }
                //window.location.href = '/mall/order/update/?order_id='+this.orderId+'&action=finish';
                W.getApi().call({
                    method: 'post',
                    app: 'mall2',
                    resource: 'order',
                    args: args,
                    success: function(data) {
                        $(".xa-shipDropBox").hide();
                        $('[data-ui-role="advanced-table"]').data('view').reload();
                    },
                    error: function() {
                    }
                })

            }else{
                    // 需要物流
                    // 向order_deliver发送信息
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
                            //$el = $(".xa-order-delivery[data-order-id=" + args['order_id'] + "]");
                            //if (typeof($el.attr("data-express-number"))=="undefined")
                            //{
                            //    $el.parent().prev().text("已发货");
                            //    $el.parent().html('<a class="xa-markFinish" href="javascript:void(0);">标记完成</a> \
                            //            <a class="xa-cancelOrder" href="javascript:void(0);">取消订单</a> \
                            //            <a class="xa-order-delivery" \
                            //            data-leader-name="' + args["leader_name"] +  '" \
                            //            data-express-number="' + args["express_number"] +  '" \
                            //            data-express-company-name="' + args["express_company_name"] +  '" \
                            //            data-is-update="true" \
                            //            data-order-id="' + args["order_id"] +  '" \
                            //            href="javascript:void(0);">修改物流</a> \
                            //    ')
                            //
                            //
                            //}
                            //else
                            //{
                            //    $el.attr({
                            //        "data-express-number" : args["express_number"],
                            //        "data-express-company-name" : args["express_company_name"],
                            //        "data-leader-name": args["leader_name"]
                            //      })
                            //}
                            //
                            //$(".xa-shipDropBox").hide();
                            $(".xa-shipDropBox").hide();
                            if($('[data-ui-role="advanced-table"]').length>0)
                                $('[data-ui-role="advanced-table"]').data('view').reload();
                            else
                                window.location.reload();


                        },
                        error: function() {

                        }
                    })

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
