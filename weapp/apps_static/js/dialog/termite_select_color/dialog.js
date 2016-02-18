/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 促销价对话框
 */
ensureNS('W.dialog.workbench');
W.dialog.workbench.SelectColorDialog = W.dialog.Dialog.extend({
    /*
    events: _.extend({
        'click .selectNavIconDialog_iconBox': 'onClickIcon'
    }, W.dialog.Dialog.prototype.events),
*/

    getTemplate: function() {
        $('#user-select-color-dialog-tmpl-src').template('user-select-color-dialog-tmpl');
        return "user-select-color-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.isColorPickerInitialized = false;
    },

    onShow: function(options) {
        var $triggerButton = options.$button;
        var cid = $triggerButton.parents('div[data-dynamic-cid]').attr('data-dynamic-cid');
        var component;
        if(cid)
            component = W.component.getComponent(parseInt(cid));
        else
            component = options.component;
        var modelField = $triggerButton.parents('div.propertyGroup_property_input').eq(0).find('input[type="hidden"]').attr('data-field');
        var targetValue = component.model.get(modelField);

        var $colorPicker = this.$dialog.find(".x-colorPicker");
        if (targetValue === 'none') {
            this.$dialog.find('input[value="0"]').attr('checked', 'checked');
        } else {
            this.$dialog.find('input[value="1"]').attr('checked', 'checked');
            $colorPicker.val(targetValue);
        }

        if (!this.isColorPickerInitialized) {
            this.isColorPickerInitialized = true;
            $colorPicker.pickAColor({
                showSpectrum : true,
                showSavedColors : false,
                saveColorsPerElement    : false,
                fadeMenuToggle          : false,
                showAdvanced            : false,
                showHexInput            : true,
                showBasicColors         : true,
                allowBlank              : true
            });
        }
    },

    /**
     * onGetData: 获取数据
     */
    onGetData: function(event) {
        var $radio = this.$dialog.find('input[type="radio"]:checked');
        var color = $radio.val();
        if (color === '0') {
            color = 'none';
        } else {
            color = this.$dialog.find('.x-colorPicker').val();
        }
        return color;
    }
});