/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 错误提示view
 */
W.common.ErrorHintView = Backbone.View.extend({
    el: '#globalErrorPanel',

    initialize: function(options) {
        this.$el = $(this.el);
        this.$hint = null;
        this.isPositioned = false;
    },

    render: function() {
        this.$el.html('<center><strong></strong></center>');
        this.$hint = this.$('strong');

    },

    show: function(errorHint) {
        /*
        if (!this.isPositioned) {
            var contentPanel = $('#phonePanel');
            this.$el.css('left', contentPanel.offset().left+'px');
        }
        */
        this.$hint.html(errorHint);
        this.$el.show();
        var _this = this;
        setTimeout(function (){_this.hide()}, 3000);
    },

    hide: function() {
        this.$el.hide();
    },

    /**
     * setMode: 设置显示模式
     *   error: 错误信息模式
     *   success: 成功信息模式
     *   info: 提示信息模式 
     */ 
    setMode: function(mode) {
        this.$el.removeClass('alert-error alert-success alert-info').addClass('alert-'+mode);
    }
});

/**
 * 获得ErrorHint的单例实例
 */
W.getErrorHintView = function(options) {
    var view = W.registry['errorHintView'];
    if (!view) {
        xlog('create W.common.ErrorHintView');
        view = new W.common.ErrorHintView(options);
        view.render();
        W.registry['errorHintView'] = view;
    }

    view.setMode('error');
    return view;
};

W.getSuccessHintView = function(options) {
    var view = W.registry['errorHintView'];
    if (!view) {
        xlog('create W.common.ErrorHintView');
        view = new W.common.ErrorHintView(options);
        view.render();
        W.registry['errorHintView'] = view;
    }

    view.setMode('success');
    return view;
};

W.getInfoHintView = function(options) {
    var view = W.registry['errorHintView'];
    if (!view) {
        xlog('create W.common.ErrorHintView');
        view = new W.common.ErrorHintView(options);
        view.render();
        W.registry['errorHintView'] = view;
    }

    view.setMode('info');
    return view;
};
