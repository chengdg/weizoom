/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择轮播图的对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.SelectProductLabelDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-select-product-label-dialog-tmpl-src').template('mall-select-product-label-dialog-tmpl');
        return "mall-select-product-label-dialog-tmpl";
    },

    events: _.extend({
        'click .xa-selectAllFirstLabel': 'onClickSelectAllLabels',
        'click input[type="checkbox"]': 'onClickSelectLabel'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        
    },

    beforeShow: function() {
        this.$('input[type="checkbox"]').prop('checked', false);
    },

    onShow: function(options) {
        this.productLabelIds = options.productLabelIds || [];
        var _this = this;
        this.productLabelIds.map(function(id){
            _this.$('input[value='+ id+']'[0]).trigger('click');
        })
    },

    afterShow: function(options) {
    },

    onClickSelectAllLabels: function(event) {
        var $checkbox = $(event.target);
        var isChecked = $checkbox.is(":checked");

        var $tr = $checkbox.parents('tr');
        $tr.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            if (!$checkbox.hasClass('xa-selectAllFirstLabel')) {
                $checkbox.prop('checked', isChecked);
            }
        });
    },

    onClickSelectLabel: function(event) {
        var $checkbox = $(event.target);
        if ($checkbox.hasClass('xa-selectAllFirstLabel')) {
            return;
        }

        var $tr = $checkbox.parents('tr');
        var isAllChecked = true;
        var $checkboxes = $tr.find('input[type="checkbox"]');
        var checkboxCount = $checkboxes.length;
        for (var i = 0; i < checkboxCount; ++i) {
            var $checkbox = $checkboxes.eq(i);
            if (!$checkbox.hasClass('xa-selectAllFirstLabel')) {
                if (!$checkbox.is(':checked')) {
                    isAllChecked = false;
                    break;
                }
            }
        }

        $tr.find('.xa-selectAllFirstLabel').prop('checked', isAllChecked);
    },

    onGetData: function(event) {
        var labels = [];
        this.$('input[type="checkbox"]:checked').each(function() {
            var $checkbox = $(this);
            if (!$checkbox.hasClass('xa-selectAllFirstLabel')) {
                labels.push({
                    id: $checkbox.val(),
                    name: $.trim($checkbox.parent().text())
                });
            }
        });
        var labels_ids = [];
        var labels_names = [];
        _.each(labels, function(province) {
            labels_ids.push(province.id);
            labels_names.push(province.name);
        })
        return {
            ids: labels_ids,
            names: labels_names
        };
    }
});