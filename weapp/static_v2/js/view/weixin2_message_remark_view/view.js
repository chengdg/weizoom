/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 发货的对话框
 * 
 * author: liupeiyu
 */
ensureNS('W.view.mall');
W.view.mall.Weixin2MessageRemarkView = W.view.common.DropBox.extend({
    getTemplate: function() {
        $('#message_remark_info_view').template('remark-info-view-dialog-tmpl');
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
        this.message_id = options.message_id;
        this.session_id = options.session_id;
    },
    
    submit: function(event) {
    	var $el = $(event.currentTarget);
        
        // $('.xa-i-remark-text-detail').html('备注:' + $('input[name="message_remark"]').val() );
        // $('.xa-i-remark').show();
        var args = {};
        args['message_id'] = this.message_id;
        args['session_id'] = this.session_id;
        args['message_remark'] = (this.$('input[name="message_remark"]').val()).replace(/\s/gi,'');
        args['status'] = "1";
        this.submitSendApi(args,event);
    },

    submitSendApi: function(args,event){
        var _this = this;
        this.close();
        W.getApi().call({
            method:'post',
            app: 'new_weixin',
            api: 'msg_memo',
            args: args,
            success: function(data) {
                window.location.reload();
                // $botton = $('[data_message_id="'+_this.message_id+'"]')
                // $botton.attr('status', '0');
                // $botton.addClass('xui-i-sessionsIcon-remarkActive');
                // $botton.attr('title', '添加备注成功');     
            },
            error: function() {
                is_editing = false;
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

    
    showPrivate: function(options) {
        this.message_remark = options.message_remark;
        this.$content.html($.tmpl(this.getTemplate()));
        $('input[name="message_remark"]').attr('value', this.message_remark);
        is_editing = true;
	},

    clickIsNeedLogistics: function(event){
        var isNeedLogistics = $('[name="is_need_logistics"]:checked').val();
        if (isNeedLogistics === '1') {
            $('.xa-ship-detail-from').show();
        }else{
            $('.xa-ship-detail-from').hide();
        }
    },
    close: function(event) {
        // console.log('close',this.$el)
        this.$html.trigger('click.dropdown');
        is_editing = false;
    }

});


W.getWeixin2MessageRemarkView = function(options) {
	var dialog = W.registry['W.view.mall.Weixin2MessageRemarkView'];
	if (!dialog) {
		//创建dialog
		xlog('create W.view.mall.Weixin2MessageRemarkView');
		dialog = new W.view.mall.Weixin2MessageRemarkView(options);
		W.registry['W.view.mall.Weixin2MessageRemarkView'] = dialog;
	}
	return dialog;
};