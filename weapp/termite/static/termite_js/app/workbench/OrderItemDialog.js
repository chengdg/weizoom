/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * order item的对话框
 */
W.workbench.dialog.OrderItemDialog = Backbone.View.extend({
    events: {
        'click .orderItemDialog_submitBtn': 'onClickSubmitButton',
    },

    getTemplate: function() {
        $('#order-item-dialog-tmpl-src').template('order-item-dialog-tmpl');
        return "order-item-dialog-tmpl";
    },

    getItemsTemplate: function() {
        $('#order-item-dialog-items-tmpl-src').template('order-item-dialog-items-tmpl');
        return "order-item-dialog-items-tmpl";
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.template = this.getTemplate();
        this.itemsTemplate = this.getItemsTemplate();
        $('body').append($.tmpl(this.template, {}));
        this.el = $('#orderItemDialog')[0];
        this.$el = $(this.el);

        this.$items = this.$('.orderItemDialog_body .controls');
        this.$items.sortable({
            axis: 'y'
        });

        this.successCallback = null;
        this.id2columnInfo = {};
    },

    render: function() {
    },

    show: function(options) {
        this.successCallback = options.success;

        var $items = $.tmpl(this.itemsTemplate, {itemInfos: options.orderedColumnInfos});
        this.$items.empty().html($items);
        this.$el.modal('show');

        this.id2columnInfo = {};
        _.each(options.orderedColumnInfos, function(columnInfo) {
            this.id2columnInfo[columnInfo.id] = columnInfo;
        }, this);
    },

    /**
     * onClickSubmitButton: 点击确定按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        this.$el.modal('hide');

        var itemInfos = [];
        var index = 1;
        var _this = this;
        this.$el.find('.orderItemDialog_item').each(function() {
            var $item = $(this);
            var id = parseInt($item.attr('data-item-id'));
            var is_checked = $item.find('input[type="checkbox"]')[0].checked;
            var columnInfo = _this.id2columnInfo[id];
            columnInfo.index = index;
            columnInfo.is_checked = is_checked;
            columnInfo.width = $item.find('input[type="text"]').val();
            index += 1;
        });

        if (this.successCallback) {
            //调用success callback
            var _this = this;
            var task = new W.DelayedTask(function() {
                _this.successCallback(JSON.stringify(_.values(_this.id2columnInfo)));
                _this.successCallback = null;
            });
          
            task.delay(500);            
        }
    }
});