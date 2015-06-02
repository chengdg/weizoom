/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.PromotionPriceDialog');
W.dialog.PromotionPriceDialog = Backbone.View.extend({
    events: {
        'click .btn-submit': 'onClickSubmitButton'
    },

    getTemplate: function() {
        $('#promotion-dialog-tmpl-src').template('promotion-dialog-tmpl');
        return "promotion-dialog-tmpl";
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.template = this.getTemplate();
        $('body').append($.tmpl(this.template, {
        }));
        this.el = $('#promotionDialog')[0];
        this.$el = $(this.el);

        this.successCallback = null;
        this.$dialog = this.$el;
    },

    render: function() {
    },

    show: function(options) {
        this.successCallback = options.success;
        this.$dialog.modal('show');

        var task = new W.DelayedTask(function() {
            this.$dialog.find('input[type="text"]').eq(0).focus();    
        }, this);
        task.delay(300);
        
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        var startTime = this.$dialog.find('#promotionDialog_startTime').val();
        var endTime = this.$dialog.find('#promotionDialog_endTime').val();
        var price = this.$dialog.find('#promotionDialog_price').val();
        var data = {
            'start_time': startTime,
            'end_time': endTime,
            'price': price
        }

        this.$dialog.modal('hide');
        if (this.successCallback) {
            //调用success callback
            var _this = this;
            var task = new W.DelayedTask(function() {
                _this.successCallback(data);
                _this.successCallback = null;
            });
          
            task.delay(200);
        }
    }
});