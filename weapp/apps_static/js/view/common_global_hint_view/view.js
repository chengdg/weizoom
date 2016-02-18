ensureNS('W.view.common');
W.view.common.GlobalHintView = Backbone.View.extend({
    el: '#globalErrorPanel',

    initialize: function(options) {
        if ($('#globalErrorPanel').length === 0) {
            $('body').prepend('<div id="globalErrorPanel" class="alert wui-globalErrorPanel"><center><span></span></center></div>')
        }
        this.$el = $('#globalErrorPanel');
        this.el = this.$el.get(0);
        this.$hint = this.$el.find('span');
        this.isPositioned = false;
        this.$window = $(window);
    },

    render: function() {
    },

    show: function(errorHint) {
        this.$hint.html(errorHint);
        if (!this.isPositioned) {
            this.$el.animate({top: '101px', opacity:1}, 400);
        }
        this.$el.show();
        var _this = this;
        setTimeout(function (){_this.hide()}, 2000);
        // this.hide();
    },

    hide: function() {
        this.$el.animate({opacity:0},1000).animate({top: 0});
    },

    /**
     * setMode: 设置显示模式
     *   error: 错误信息模式
     *   success: 成功信息模式
     *   info: 提示信息模式 
     */ 
    setMode: function(mode) {
        this.$el.removeClass('alert-danger alert-success alert-info').addClass('alert-'+mode);
    }
});

/**
 * 获得ErrorHint的单例实例
 */
W.getErrorHintView = function(options) {
    var view = W.registry['globalHintView'];
    if (!view) {
        xlog('create W.view.common.GlobalHintView');
        view = new W.view.common.GlobalHintView(options);
        view.render();
        W.registry['globalHintView'] = view;
    }

    view.setMode('danger');
    return view;
};

W.getSuccessHintView = function(options) {
    var view = W.registry['globalHintView'];
    if (!view) {
        xlog('create W.view.common.GlobalHintView');
        view = new W.view.common.GlobalHintView(options);
        view.render();
        W.registry['globalHintView'] = view;
    }

    view.setMode('success');
    return view;
};

W.getInfoHintView = function(options) {
    var view = W.registry['globalHintView'];
    if (!view) {
        xlog('create W.view.common.GlobalHintView');
        view = new W.view.common.GlobalHintView(options);
        view.render();
        W.registry['globalHintView'] = view;
    }

    view.setMode('info');
    return view;
};

W.showHint = function(type, hint) {
    if (type === 'error') {
        W.getErrorHintView().show(hint);
    } else if (type === 'info') {
        W.getInfoHintView().show(hint);
    } else {
        W.getSuccessHintView().show(hint);
    }
}