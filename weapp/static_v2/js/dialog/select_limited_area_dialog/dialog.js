/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 选择限定区域对话框
 * 
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.SelectLimitedAreaDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-select-limited-area-dialog-tmpl-src').template('mall-select-limited-area-dialog-tmpl');
        return "mall-select-limited-area-dialog-tmpl";
    },
    events: _.extend({
        'click .xa-selectAllProvince': 'onClickSelectAllProvince',
        'click input[type="checkbox"]': 'onClickSelectProvince'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        
    },

    beforeShow: function() {
        // this.$('input[type="checkbox"]').prop('checked', false).prop('disabled', false);
    },

    onShow: function(options) {
        // this.checkedProvinces = options.provinces || [];
        // this.disabledProvinceSet = options.disabledProvinceSet || {};
    },

    afterShow: function(options) {
    },

    onClickSelectAllProvince: function(event) {
        var $checkbox = $(event.target);
        var isChecked = $checkbox.is(":checked");

        var $tr = $checkbox.parents('tr');
        $tr.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            if (!$checkbox.hasClass('xa-selectAllProvince')) {
                $checkbox.prop('checked', isChecked);
            }
        });
    },

    onClickSelectProvince: function(event) {
        var $checkbox = $(event.target);
        if ($checkbox.hasClass('xa-selectAllProvince')) {
            return;
        }

        var $tr = $checkbox.parents('tr');
        var isAllChecked = true;
        var $checkboxes = $tr.find('input[type="checkbox"]');
        var checkboxCount = $checkboxes.length;
        for (var i = 0; i < checkboxCount; ++i) {
            var $checkbox = $checkboxes.eq(i);
            if (!$checkbox.hasClass('xa-selectAllProvince')) {
                if (!$checkbox.is(':checked')) {
                    isAllChecked = false;
                    break;
                }
            }
        }

        $tr.find('.xa-selectAllProvince').prop('checked', isAllChecked);
    },

    onGetData: function(event) {
        var provinces = [];
        this.$('input[type="checkbox"]:checked').each(function() {
            var $checkbox = $(this);
            if (!$checkbox.hasClass('xa-selectAllProvince')) {
                provinces.push({
                    id: $checkbox.val(),
                    name: $checkbox.parent().text()
                });
            }
        });

        provinces = _.sortBy(provinces, function(province) { return province.id; });
        var province_ids = [];
        var province_names = [];
        _.each(provinces, function(province) {
            province_ids.push(province.id);
            province_names.push(province.name);
        })
        return {
            ids: province_ids,
            names: province_names
        };
    }
});