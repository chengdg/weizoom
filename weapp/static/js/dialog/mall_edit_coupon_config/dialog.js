/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 编辑商城优惠券配置的对话框
 */
ensureNS('W.dialog.mall');
W.dialog.mall.EditMallCouponCofnigDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click input[value="depend_to_price"]': 'onClick'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#mall-coupon-config-dialog-tmpl-src').template('mall-coupon-config-dialog-tmpl');
        return "mall-coupon-config-dialog-tmpl";
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
        W.getLoadingView().hint('加载数据...').show();
        W.getApi().call({
            app: 'mall',
            api: 'coupon_config/get',
            args: {},
            success: function(data) {
                W.getLoadingView().hide();
                $('input[value="' + data.useType + '"]').attr('checked', 'checked');
                $('input[value="' + data.overflowType + '"]').attr('checked', 'checked');

                if (data.useType === 'depend_to_price') {
                    $('input[name="activate_price"]').val(data.activatePrice);
                }
            },
            error: function(resp) {
                W.getLoadingView().hide();
                W.getErrorHintView().show('加载优惠券配置失败！');
            }
        });
    },

    onGetData: function(options) {
        var useType = $('input[name="use_type"]:checked').val();
        var overflowType = $('input[name="overflow_type"]:checked').val();
        var activatePrice = $.trim($('input[name="activate_price"]').val());

        if (useType === 'depend_to_price') {
            if (!activatePrice) {
                alert('请输入价格');
                return false;
            }
        }

        var data = {
            'use_type': useType,
            'overflow_type': overflowType,
            'activate_price': activatePrice
        }
        return data;
    },

    onClick: function(event) {
        var $radio = $(event.currentTarget);
        $radio.parent().find('input[type="text"]').focus();
    }
});