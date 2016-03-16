ensureNS('W.dialog.termite');

W.dialog.termite.SelectProductDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectProduct': 'onSelectProduct',
        'click .xa-search': 'onSearch',
        'keypress .xa-query': 'onPressKey'

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
        this.onSearch();
    },
    onSearch: function(event) {
        var query = $.trim(this.$el.find('.xa-query').val());

        this.table.reload({
            name: query
        })
    },
    onPressKey: function(event) {
        var keyCode = event.keyCode;
        if (keyCode == 13) {
            this.onSearch(event);
        }
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
                console.log($tr);
                var productId = $tr.data('id');
                data.push(_this.table.getDataItem(productId).toJSON());
            }
        });
        return data;
    }
})