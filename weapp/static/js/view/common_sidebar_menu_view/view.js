/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 图片上传View
 */
ensureNS('W.view.common');
W.view.common.SideBarMenu = Backbone.View.extend({
    el: '',

    events: {
        'click .wui-sidebarMenu-handler': 'onClickSideMenuHandler'
    },

    getTemplate: function() {
        $('#side-menu-view-tmpl-src').template('side-menu-view-tmpl');
        return 'side-menu-view-tmpl';
    },

    initialize: function(options) {
        this.$el = $(this.el);
    },


    render: function() {
        xlog('[sidebar-menu]: render now!');
        this.$el.addClass('wui-sidebarMenu');
        this.$el.append('<div class="wui-sidebarMenu-handler"><img src="/static/img/sidebar_menu_handler.png"></img></div>');
        this.$el.show();
    },

    onClickSideMenuHandler: function(event) {
        var cls = 'wui-inner-expand';
        if (this.$el.hasClass(cls)) {
            this.$el.removeClass('wui-inner-expand');
        } else {
            this.$el.addClass('wui-inner-expand');
        }
    }
});


W.registerUIRole('[data-ui-role="sidebar-menu"]', function() {
    var $el = $(this);
    var view = new W.view.common.SideBarMenu({
        el: $el.get()
    });
    $el.data('view', view);
    view.render();
});