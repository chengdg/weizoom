ensureNS('W.dialog.termite');

W.dialog.termite.SelectProductDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectProduct': 'onSelectProduct'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#select-product-dialog-tmpl-src').template('select-product-dialog-tmpl');
        return "select-product-dialog-tmpl";
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

    onSelectProduct: function(event) {
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
            if ($tr.find('.xa-selectProduct').is(':checked')) {
                console.log('MMMMDMDMMD&&&&&&&*****************??');
                console.log('=========');
                console.log($tr);
                var productId = $tr.data('id');
                data.push(_this.table.getDataItem(productId).toJSON());
            }
        })
        return data;
    }
})