/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 白色的大加载图标的配置参数
 * @const
 */
W.BIG_SPIN_OPTS = {
    lines: 12, // The number of lines to draw
    length: 15, // The length of each line
    width: 5, // The line thickness
    radius: 10, // The radius of the inner circle
    corners: 1, // Corner roundness (0..1)
    rotate: 0, // The rotation offset
    direction: 1, // 1: clockwise, -1: counterclockwise
    color: '#FFF', // #rgb or #rrggbb
    speed: 1, // Rounds per second
    trail: 50, // Afterglow percentage
    shadow: false, // Whether to render a shadow
    hwaccel: false, // Whether to use hardware acceleration
    className: 'spinner', // The CSS class to assign to the spinner
    zIndex: 2e9, // The z-index (defaults to 2000000000)
    top: 'auto', // Top position relative to parent in px
    left: 'auto' // Left position relative to parent in px
};

/**
 * 黑色的大加载图标的配置参数
 * @const
 */
W.SMAILL_SPIN_OPTS = {
    lines: 12, // The number of lines to draw
    length: 6, // The length of each line
    width: 2, // The line thickness
    radius: 8, // The radius of the inner circle
    color: '#000', // #rgb or #rrggbb
    speed: 1, // Rounds per second
    trail: 60, // Afterglow percentage
    shadow: false // Whether to render a shadow
};

/**
 * 加载等待提示View
 */
W.LoadingView = Backbone.View.extend({
    el: '#spin-wrapper',

    initialize: function(options) {
        options = options || {};
        this.$el = $(this.el);
        this.$el.css(options);
        this.$el.find('#spin-hint').html('操作进行中...');
        this.spinner = new Spinner(W.BIG_SPIN_OPTS);
        this.visible = false;
    },

    hint: function(hint) {
        this.$el.find('#spin-hint').html(hint);
        return this;
    },

    show: function(callback, timeout, cssOptions) {
        var msg = null;
        if (typeof(callback) === 'string') {
            msg = callback;
            callback = null;
        }
        if (!this.visible) {
            if (msg) {
                this.$el.find('#spin-hint').html(msg);
            }
            this.$el.show();
            this.visible = true;
            this.spinner.spin($('#spin')[0]);
        }

        if (callback) {
            setTimeout(callback, timeout);
        }

        cssOptions = cssOptions || {};
        this.$el.css(cssOptions);
    },

    hide: function() {
        if (this.visible) {
            this.visible = false;
            this.spinner.stop();
            this.$el.hide();
            this.$el.find('#spin-hint').html('操作进行中...');
        }
    }
});

/**
 * 获得Loading的单例实例
 */
W.getLoadingView = function(options) {
    var view = W.registry['loadingView'];
    if (!view) {
        xlog('create W.LoadingView');
        view = new W.LoadingView(options);
        W.registry['loadingView'] = view;
    }

    return view;
};
