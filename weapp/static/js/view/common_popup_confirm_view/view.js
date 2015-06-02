/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/*
* 下拉弹出式确认框
*/
ensureNS('W.view.common');
W.view.common.ConfirmView = W.view.common.DropBox.extend({
    SUBMIT_EVENT: 'submit',
    
    CLOSE_EVENT: 'close',
    
    isArrow: true,
    
    isTitle: false,
    
    events:{
        'click .tx_submit': 'submit',
        'click .tx_cancel': 'close'
    },
    
    getTemplate: function() {
        return '<dl class="itemDeleteView"><dt class="tx_info"></dt>'
                +'<dd><button type="button" class="tx_submit btn btn-success">确定</button> '
                +'<button type="button" class="tx_cancel btn">取消</button>'
                +'</dd></dl>';
    },

    initializePrivate: function(options) {
        this.$el = $(this.el);
        this.render();
    },
    
    render: function() {
        html = this.getTemplate();
        this.$content.html(html);
    },
    
    showPrivate: function(options) {
        this.$('.tx_info').html(options.info);
        this.$('.tx_submit').focus();
        this.setPosition();
    },
    
    submit: function() {
        this.$('.tx_submit').bottonLoading({status:'show'});
        this.trigger(this.SUBMIT_EVENT);
    },
    
    closePrivate: function() {
        this.$('.tx_submit').bottonLoading({status:'hide'});
        this.trigger(this.CLOSE_EVENT);
    }
});


ensureNS('W.view.fn');
/**
 * 获得ItemDeleteView的单例实例
 */
W.view.fn.requreConfirm = function(options) {
    //获得view
    var view = W.registry['common-popup-confirm-view'];
    if (!view) {
        xlog('create PopupConfirmView');
        view = new W.view.common.ConfirmView(options);
        view.render();
        W.registry['common-popup-confirm-view'] = view;
    }

    if (options.confirm) {
        view.bind(view.SUBMIT_EVENT, options.confirm);
    }

    view.show({
        $action: options.$el,
        info: options.info || '确定删除吗？',
    });
};

W.view.fn.finishConfirm = function() {
    var view = W.registry['common-popup-confirm-view'];
    if (view) {
        view.hide();
    }
}