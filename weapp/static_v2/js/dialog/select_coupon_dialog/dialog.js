ensureNS('W.dialog.mall');

W.dialog.mall.SelectCouponDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click .xa-selectCoupon': 'onSelectCoupon'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#select-coupon-dialog-tmpl-src').template('select-coupon-dialog-tmpl');
        return "select-coupon-dialog-tmpl";
    },

    onInitialize: function(options) {
        this.table = this.$('[data-ui-role="advanced-table"]').data('view');
        this.is_channel_qrcode = options.is_channel_qrcode || false;
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
        var coupon_id = $checkbox.parents('tr').data('id');
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
        if (this.is_channel_qrcode){
            var search = location.search;
            var index = search.indexOf('=');
            var setting_id = search.substring(index+1);
            W.getApi().call({
                app: 'new_weixin',
                api: 'coupon_can_use',
                args: {
                    coupon_id: coupon_id,
                    setting_id: setting_id
                },
                scope: this,
                success: function(data) {},
                error: function(resp) {
                    W.showHint('warning', resp.errMsg);
                }
            });
        }
    },

    onGetData: function(options) {
        var data = [];
        var _this = this;
        this.$('tbody tr').each(function() {
            var $tr = $(this);
            if ($tr.find('.xa-selectCoupon').is(':checked')) {
                var couponId = $tr.data('id');
                data.push(_this.table.getDataItem(couponId).toJSON());
            }
        })
        return data;
    }
})