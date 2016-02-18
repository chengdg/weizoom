/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单支付弹出框
 *
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.UpdateOrderDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-order-pay-dialog-tmpl-src').template('mall-order-pay-dialog-tmpl');
        return "mall-order-pay-dialog-tmpl";
    },

    getProductsTemplate: function() {
        $('#mall-order-pay-dialog-products-tmpl-src').template('mall-order-pay-dialog-products-tmpl');
        return "mall-order-pay-dialog-products-tmpl";
    },

    getShipInfoTemplate: function() {
        $('#mall-order-pay-dialog-ship-info-tmpl-src').template('mall-order-pay-dialog-ship-info-tmpl');
        return "mall-order-pay-dialog-ship-info-tmpl";
    },

    onInitialize: function(options) {
        this.productsTemplate = this.getProductsTemplate();
        this.shipInfoTemplate = this.getShipInfoTemplate();
    },

    onShow: function(options) {
        console.log('onShow', options.orderId);
        this.orderId = options.orderId;
        // 是否可以修改价钱
        this.isUpdatePrice = options.isUpdatePrice == true ? true : false;
        console.log('this.isUpdatePrice', this.isUpdatePrice);
        // 更新商品信息
        this.reloadProducts(options.orderId);
        if (this.isUpdatePrice) {
            this.$('.modal-title').html('修改价格');
            this.$('.wui-dialogbtn').html('确认修改');
        }else{
            this.$('.modal-title').html('支付');
            this.$('.wui-dialogbtn').html('确认支付');
        }
    },

    afterShow: function(options) {
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onGetData: function(event) {
        xlog('in get data...');
        if (!W.validate($('.xui-commonOrderPayDialog'))) {
            return false;
        }
        var data = [];
        if (this.isUpdatePrice) {
            var finalPrice = $('input[name="order-final-price"]').val();
            var postage = $('input[name="order-postage"]').val();
            data.push({
                postage: postage,
                finalPrice: finalPrice
            })
        } else {
            return true;
        }
        return data[0];
    },

    reloadProducts: function(orderId){
        W.getApi().call({
            app: 'mall2',
            resource: 'order_product',
            args: {
                order_id: orderId
            },
            scope: this,
            success: function(data) {
                var product_count = data['products'].length;
                var $products = $.tmpl(this.productsTemplate, {
                    'order': data,
                    'productCount': product_count,
                    'isUpdatePrice': this.isUpdatePrice
                });
                this.$('.xa-productTable').empty().append($products);
                var $shipInfo = $.tmpl(this.shipInfoTemplate, {'order': data});
                this.$('.xa-order-ship-info').empty().append($shipInfo);
            },
            error: function(resp) {

            }
        });
    }
});

