/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 发货的对话框
 *
 * author: liupeiyu
 */
ensureNS('W.view.mall');
W.view.mall.MallOrderRemarkView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#remark-info-view').template('remark-info-view-dialog-tmpl');
        return "remark-info-view-dialog-tmpl";
    },

    getOneTemplate: function() {
    	$('#single-logistics-info-view').template('single-logistics-info-view-dialog-tmpl');
        return "single-logistics-info-view-dialog-tmpl";
    },

    events:{
     	'click .xa-submit': 'submit',
    },

    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.position = options.position;
        this.privateContainerClass = options.privateContainerClass;
        this.$content.parent().addClass(this.privateContainerClass);
    },

    submit: function(event) {
    	var $el = $(event.currentTarget);
        //var orderId = options.orderId;
        args = {};
        args['order_id'] = this.orderId;
        args['remark'] = $('input[name="remark"]').val();
        this.submitSendApi(args);
    	/*var validate = this.validate();
    	if(validate.is_submit) {
            // true为修改物流信息，只修改，不改变状态


            // 是否需要物流

    		// window.location.href = '/mall/editor/order_express/add/?order_id=' +
      //       this.orderId + '&=' + logistics + '&express_number=' + logisticsOrderId +
      //        '&leader_name=' + leaderName+ '&is_update_express='+isUpdateExpress;
    	} else {
    		$('div.error').text(validate.errMsg);
    	}*/
    },

    submitSendApi: function(args){
        W.getApi().call({
            method:'post',
            app: 'mall2',
            resource: 'order',
            args: args,
            success: function(data) {
                order_id = args['order_id'];
                remark = args['remark'];
                $el = $("li[data-order-id=" + order_id + "] table tbody");
                if($el.find(".xa-remark").length>0)
                    $el.find(".xa-remark").html('<img src="/static_v2/img/editor/attention.jpg"> 卖家备注：'+ remark);
                else
                {
                    $el.append('<tr> <td class="xui-remark xa-remark" colspan="8"> <img src="/static_v2/img/editor/attention.jpg"> 卖家备注：'+ remark +'</td> </tr>');
                }

                $(".xa-remarkDropBox").hide();
            },
            error: function() {
            }
        })
    },

    validate: function() {

    },

    getLogisticsInfo: function() {
    },

    render: function() {
    	this.$content.html($.tmpl(this.getTemplate()));
	},

    onShow: function(options) {
        this.$content.html($.tmpl(this.getTemplate()));
        this.position = options.position;

    	$('.modal-backdrop').css({
    		 'background-color': '#fff',
    		 'opacity': '0'
    	})
    },

    showPrivate: function(options) {
    	this.orderId = options.orderId;
        //this.expressCompanyValue = options.expressCompanyValue;
        ///this.expressNumber = options.expressNumber;
        //this.leaderName = options.leaderName;
    	//this.getLogisticsInfo();
        this.message = options.message;
        this.$content.html($.tmpl(this.getTemplate()));
        $('input[name="remark"]').attr('value', this.message);
	},

    clickIsNeedLogistics: function(event){
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
        if (isNeedLogistics === '1') {
            $('.xa-ship-detail-from').show();
        }else{
            $('.xa-ship-detail-from').hide();
        }
    }

});


W.getMallOrderRemarkView = function(options) {
	var dialog = W.registry['W.view.mall.MallOrderRemarkView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.MallOrderRemarkView');
		dialog = new W.view.mall.MallOrderRemarkView(options);
		W.registry['W.view.mall.MallOrderRemarkView'] = dialog;
	}
	return dialog;
};