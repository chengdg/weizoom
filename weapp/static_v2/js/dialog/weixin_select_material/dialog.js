/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.weixin');
W.dialog.weixin.SelectMaterialDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectMaterial': 'onSelectMaterial',
        'click .xa-search': 'onSearch',
        'keypress .xa-query': 'onPressKey'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#weixin-select-material-dialog-tmpl-src').template('weixin-select-material-dialog-tmpl');
        return "weixin-select-material-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.materialId = options.materialId || 0;
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        console.log('dialog, onShow', options);
        this.materialId = options.materialId || this.materialId;
        // 清空搜索框
        $('.xa-query').val("");
    },

    afterShow: function(options) {
        this.table.reload({
            selected_material_id: this.materialId
        });
    },

    onPressKey: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            this.onSearch(event);
        }
    },

    onSearch: function(event) {
        var query = $.trim($('.xa-query').val());
        this.table.reload({
            selected_material_id: this.materialId,
            query: query
        })
    },

    onSelectMaterial: function(event) {
        var $checkbox = $(event.currentTarget);
        $checkbox.prop('checked', true);

        if (!this.enableMultiSelection && $checkbox.is(':checked')) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选取');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
            $checkbox.prop('checked', true);
        }

        $checkbox.prop('checked', true);

        if ($checkbox.is(':checked')) {
            console.log(1212, $checkbox.is(':checked'))
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选取');
        } else {
            // $checkbox.parent().removeClass('checked');
            // $checkbox.parent().find('span').text('选取');
        }
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        var materialId = null;
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectMaterial').is(':checked')) {
                materialId = $tr.data('id');
            }
        })

        return this.table.getDataItem(materialId).toJSON();
    }
});