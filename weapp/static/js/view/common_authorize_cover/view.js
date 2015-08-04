/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 图片上传View
 */
ensureNS('W.view.common');
W.view.common.AuthorizeCover = Backbone.View.extend({
    el: '',

    events: {
        'click a': 'onClickDocTrigger',
        'click .x-docCloseBtn': 'onClickCloseButton'
    },

    getTemplate: function() {
        $('#common-authorize-cover-tmpl-src').template('common-authorize-cover-tmpl');
        return 'common-authorize-cover-tmpl';
    },


    initialize: function(options) {
        this.$container = options.attachToEl;
        this.template = this.getTemplate();

        //创建内容容器
        var $node = $.tmpl(this.template, {});
        this.computeWidthAndHeight($node);
        this.$container.append($node);
        this.$el = $node;

        var $window = $(window);
        var _this = this;
        $window.resize(function() {
            _this.computeWidthAndHeight(_this.$el);
        });
    },

    /**
     * 计算宽和高
     */
    computeWidthAndHeight: function($node){
        var left = this.$container.offset().left;
        left = (left + 202); //202是左侧导航区域的宽度

        var width = this.$container.outerWidth();
        width = (width-202);

        var $window = $(window);
        var height = $window.outerHeight();

        $node.css({
            left: left+'px',
            height: height+'px',
            width: width+'px'
        });

        $node.find('.x-docContent').css({
            height: (height - 110 + 'px')
        })
    },

    render: function() {
        
    },

    show: function(options) {
        this.$('strong').html(options.hint);
        this.$('.x-docContent').html($('#'+options.doc).html());
    },

    onClickDocTrigger: function(event) {
        this.$('.alert').hide();
        this.$('.x-doc').fadeIn('fast');
    },

    onClickCloseButton: function(event) {
        this.$('.x-doc').hide();
        this.$('.alert').show();
    }
});


W.view.showAuthorizeCover = function(options) {
    if (!W.view._authorizeCover) {
        xlog('[authorize cover]: create');
        W.view._authorizeCover = new W.view.common.AuthorizeCover({
            el: '#main-panel',
            attachToEl: $('#main-panel')
        });
        W.view._authorizeCover.render();
    }
    
    W.view._authorizeCover.show(options);
}
