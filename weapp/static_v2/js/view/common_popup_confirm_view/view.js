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
        'click .xa-confirm': 'submit',
        'click .xa-cancel': 'hide'
    },
    //横向提示
    getTemplate1: function() {
        var template = '<dl class="wui-confirmView">'
                +'<dd>'
                +  '<div class="xa-icon"><i></i></div>'
                +  '<div class="xui-i-msg xa-msg"><%=msg%></span></div>'
                +  '<div><button type="button" class="xa-confirm btn xui-confirm">确定</button></div> '
                +  '<div><button type="button" class="xa-cancel  xui-cancel btn">取消</button></div>'
                +'</dd>'
                +'</dl>'
                +'<%=warning_msg%>';
        return _.template(template);
    },
    //纵向提示
    getTemplate2: function(){
        var template = '<div class="wui-confirmView v">'
                +'<div class="xui-msgBox">'
                +  '<div class="xa-icon"><i></i></div>'
                +  '<div class="xui-i-msg xa-msg"><%=msg%></span></div>'
                +'</div>'
                +  '<div class="tc mb15"><button type="button" class="xa-confirm btn xui-confirm">确定</button><button type="button" class="xa-cancel  xui-cancel btn">取消</button></div> '
                +'</div>'
                +'<%=warning_msg%>';
        return _.template(template);
    },
    initializePrivate: function(options) {
        this.isTitle = options.isTitle;
        this.position = options.position || 'top';
        this.$el = $(this.el);
        this.render();
        this.template = (options.templateAlign && options.templateAlign == 'vertical') ? this.getTemplate2():this.getTemplate1();
        this.privateContainerClass = options.privateContainerClass;
        this.$el.addClass(this.privateContainerClass);
        this.viewName = options.viewName;
        xlog(options.show_icon)
        this.show_icon = options.show_icon;
        if(this.show_icon == undefined)
            this.show_icon = true;
        xlog(this.show_icon)
    },

    render: function() {
    },

    showPrivate: function(options) {
        this.$('.xa-msg').html(options.msg);
        this.$('.xa-submit').focus();
        var html = this.template(options);
        this.$content.html(html);
        if(!this.show_icon){
            this.$content.find('.xa-icon').hide();
        }
    },

    submit: function() {
        this.$('.xa-submit').bottonLoading({status:'show'});
        this.trigger(this.SUBMIT_EVENT);
    },

    closePrivate: function() {
        this.$('.xa-submit').bottonLoading({status:'hide'});
        this.trigger(this.CLOSE_EVENT);
    }
});


/**
 * 获得ItemDeleteView的单例实例
 */
W.isRequireConfirmViewDisplayed = false;
W.requireConfirm = function(options) {
    //获得view
    var view = W.registry['common-popup-confirm-view'];
    // if (!view) {
        xlog('create PopupConfirmView');
        view = new W.view.common.ConfirmView(options);
        view.render();
        W.registry['common-popup-confirm-view'] = view;
    // }
    if (options.confirm) {
        view.bind(view.SUBMIT_EVENT, options.confirm);
    }
    if(options.cancel){
       view.bind(view.CLOSE_EVENT, options.cancel);
    }
    view.show({
        width:options.width,
        height:options.height,
        $action: options.$el,
        templateAlign: options.templateAlign,
        msg: options.msg || '确定删除吗？',
        warning_msg: options.warning_msg || '',
        minClickTime: options.minClickTime
    });
    W.isRequireConfirmViewDisplayed = true;
};

W.finishConfirm = function() {
    var view = W.registry['common-popup-confirm-view'];
    if (view) {
        view.hide();
    }
};
