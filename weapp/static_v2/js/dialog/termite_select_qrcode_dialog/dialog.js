ensureNS('W.dialog.termite');

W.dialog.termite.SelectQrcodeDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectQrcode': 'onSelectCoupon'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#select-qrcode-dialog-tmpl-src').template('select-qrcode-dialog-tmpl');
        return "select-qrcode-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
    },

    beforeShow: function() {
        this.table.reset();
    },

    onShow: function(options) {
        this.enableMultiSelection = false;
        if (options.hasOwnProperty('enableMultiSelection')) {
            this.enableMultiSelection = options.enableMultiSelection;
        }
    },

    afterShow: function(options) {
        this.table.reload();
    },

    onSelectCoupon: function(event) {
        var $checkbox = $(event.currentTarget);
        if (!this.enableMultiSelection) {
            var $label = this.$('label.checked');
            $label.find('input').prop('checked', false);
            $label.removeClass('checked');
            if($checkbox.parent().hasClass('checked')){
                $checkbox.parent('.checked').find('span').text('已选择');
            }else{
                $checkbox.parents('tr').siblings().find('label span').text('选取');
            }
        }
        if ($checkbox.is(':checked')) {
            $checkbox.parent().addClass('checked');
            $checkbox.parent('.checked').find('span').text('已选择');
        } else {
            $checkbox.parent().removeClass('checked');
            $checkbox.parent().find('span').text('选取');
        }
    },

    onGetData: function(options) {
        var data = [];
        var _this = this;

        this.$('tbody tr').each(function() {
            var $tr = $(this);
                console.log($tr);
            if ($tr.find('.xa-selectQrcode').is(':checked')) {
                var qrcodeId = $tr.data('id');
                data.push(_this.table.getDataItem(qrcodeId).toJSON());
            }
        })
        return data;
    }
})