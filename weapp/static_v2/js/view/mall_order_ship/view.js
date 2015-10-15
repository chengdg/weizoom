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
        'click .xa-is-need-logistics': 'onClickIsNeedLogistics',
        'change .xa-logistics': 'showExpressName'

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
            var logisticsOtherExpressName = $('input[name="logistics_other_express_name"]').val();
    		$el.bottonLoading({status: 'show'});

            
            var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
            var is_100 = true;
            if(isNeedLogistics === '0'){
                // 不需要物流
                logistics = '';
                logisticsOrderId = '';
                is_100 = false;
            } else if('other' == logistics){
                // 如果是其他 则修改为用户自己填写的快递
                logistics = logisticsOtherExpressName;
                is_100 = false;
            }
            var args = {
                'order_id': this.orderId,
                'express_company_name': logistics,
                'express_number': logisticsOrderId,
                'leader_name': leaderName,
                'is_update_express': isUpdateExpress,
                'is_100': is_100
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
    showExpressName: function(event) {
        var logistics = $('select.ua-logistics').val();
        // 如果是其他 则显示物流名称的选项框
        if ('other' == logistics){
            $(".xui-logistics-other-express-name").css("display","block");
        }else{
            $(".xui-logistics-other-express-name").css("display","none");
        }
    },
    validate: function() {
        // 是否需要物流
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
    	var logistics = $('select.ua-logistics').val();
    	var logisticsOrderId = $('input[name="logistics_order_id"]').val().replace(/(^\s*)|(\s*$)/g, "");
        var logisticsOtherExpressName = $('input[name="logistics_other_express_name"]').val();
        var logistics = $('select.ua-logistics').val();
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
            //校验选择了其他后是否输入了物流名称
            if ('other' == logistics && logisticsOtherExpressName == ''){
                errMsg = '请输入正确的物流名称';
                validate.is_submit = false;
                $('div.xa-error').removeClass('hidden').text(errMsg);
            }
            if (logisticsOrderId == false || !/^\w+$/.test(logisticsOrderId)) {
                errMsg = '请输入正确的快递单号';
                validate.is_submit = false;
                $('div.xa-error').removeClass('hidden').text(errMsg);
            }
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
                var flag = false;
    			var $container = $('.ua-logistics');
    			for (var i=0; i<data.length; i++ ) {
    				var $option = $.tmpl(_this.getOneTemplate(), data[i]);
                    if(data[i]['value'] === _this.expressCompanyValue){
                        $option.attr('selected','selected');
                        flag = true;
                    }
    				$container.append($option);
    			};
                // 添加其他快递的选项，选择后显示物流名称
                var data_last = {"id": "00000", "value": "other", "name": "\u5176\u4ed6"}

                var $option = $.tmpl(_this.getOneTemplate(), data_last);
                if(!flag){
                    $option.attr('selected','selected');
                    $(".xui-logistics-other-express-name").css("display","block");
                    $('input[name="logistics_other_express_name"]').val(_this.expressCompanyValue);
                }
                $container.append($option);
                console.log(_this.expressCompanyValue);
                if(_this.expressCompanyValue == -1){
                    $('select.xa-logistics option:last-child').removeAttr('selected');
                    $('select.xa-logistics option:first-child').attr('selected','selected');
                    $(".xui-logistics-other-express-name").css("display","none");
                    $('input[name="logistics_other_express_name"]').val("");
                }

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
