/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.view.termite');
ensureNS('W.model.termite');



/**
 * 用于嵌入到页面中的微信模拟器
 * @class
 */
W.view.termite.EmbededPhoneView = Backbone.View.extend({
    el: '',

    events: {
        'mouseenter .xa-i-news-message': 'onShowActionBar',
        'mouseleave .xa-i-news-message': 'onHideActionBar',
        'click li.xa-i-news-message': 'onSelectNews',
        'click .xa-add-news-btn': 'onCreateNews',
        'click .xa-i-delete-news-btn': 'onDeleteNews',
        'click .xa-simulator-back-btn': 'onClickBackBtn',
        'click .xa-simulator-screen a': 'onClickLink'
    },

    compileTemplate: function() {
        $('#termite-edit-simulator-tmpl-src').template('termite-edit-simulator-tmpl');
     
    },

    initialize: function(options) {
        this.$el = $(this.el);
         console.log('uuuuuuuuu');
        this.compileTemplate();
    },


    /**
     * 渲染html结果
     */
    render: function() {
        //创建html
        this.$el.html($.tmpl('termite-edit-simulator-tmpl', {
            title: '',
        }));
        console.log('uuuuuuuuu');
    },


});

