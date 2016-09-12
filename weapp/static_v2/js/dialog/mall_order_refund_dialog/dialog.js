/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 订单退款弹出框
 *
 * author: robert
 */
ensureNS('W.dialog.mall');

W.dialog.mall.RefundOrderDialog = W.dialog.Dialog.extend({
    getTemplate: function() {
        $('#mall-order-refund-dialog-tmpl-src').template('mall-order-refund-dialog-tmpl');
        return "mall-order-refund-dialog-tmpl";
    },

    events: _.extend({
        'click .xa-close': 'onClickCloseButton',
        'keyup .xui-commonOrderRefundDialog input': 'onChange',
        'click .xa-submit': 'onClickSubmitButton'
    }, W.dialog.Dialog.prototype.events),

    onInitialize: function(options) {
        this.refundTemplate = this.getTemplate();
    },

    onClickCloseButton: function(event) {
        this.$dialog.modal('hide');
    },

    // 获得页面中的所有订单信息，并筛选出字母订单的信息
    // 放入 this.dialogMainData
    __fetchOrdersInfos: function() {
        var _this = this;
        var allData = JSON.parse($('#origin-data').text());
        var orders = allData.items;

        // 新建带key的object所有订单数据，便于查找
        this.allOrders = {};
        orders.map(function(order){
            _this.allOrders[order.id] = order;
        });

        // 找出母订单中支付金额
        var allOrders = this.allOrders;
        var mainOrder = allOrders[this.orderId];
        var mainRefundInfo = {
            cash: mainOrder.pay_money,
            weizoomCardMoney: mainOrder.weizoom_card_money,
            couponMoney: mainOrder.save_money,
            integral: mainOrder.integral
        };

        // 找出母订单中的其它子订单的退款信息
        var subRefundInfo = [];
        mainOrder.groups.map(function(subOrder){
            var _subOrder = subOrder.fackorder;
            if (_subOrder.id == _this.deliveryItemId && !_.isEmpty(_subOrder.refund_info)) {
                subRefundInfo.push(_subOrder.refund_info);
            }
        }); 

        this.dialogMainData = {
            'mainOrder': mainOrder,
            'mainRefundInfo': mainRefundInfo,
            'subRefundInfo': subRefundInfo
        };

        // 校验并提示信息
        this.__validate();

        console.log( '订单信息：%o', this.dialogMainData.mainOrder);
    },

    // 实时计算退款总额
    __calcCurrentOrderRefund: function() {
        var $dialog = this.$dialog;
        var orderId = this.orderId;
        var allOrders = this.allOrders;

        var deliveryItemId = this.deliveryItemId;
        var integralPerYuan =  parseFloat(this.integralPerYuan);
        integralPerYuan =  integralPerYuan > 0? integralPerYuan : 1;

        // 转换当前对话框中的退款信息
        var cash = $('[name="cash"]', $dialog).val() * 1;
        var weizoomCardMoney = $('[name="weizoom_card_money"]', $dialog).val() * 1;
        var couponMoney = $('[name="coupon_money"]', $dialog).val() * 1;
        var integralCount = $('[name="integral"]', $dialog).val() * 1;
        var integral = integralCount/integralPerYuan * 1;

        // 不能为负数
        var cash = cash > 0? cash : 0;
        var weizoomCardMoney = weizoomCardMoney > 0? weizoomCardMoney : 0;
        var couponMoney = couponMoney > 0? couponMoney : 0;
        var integral = integral > 0? integral : 0;

        var totalMoney = cash + weizoomCardMoney + couponMoney + integral;

        // 保存至this.dialogMainData
        var targetOrder = {
            "cash": cash,
            "weizoomCardMoney": weizoomCardMoney,
            "couponMoney": couponMoney,
            "integral": integral,
            "totalMoney": totalMoney.toFixed(2)
        };
        this.dialogMainData['targetOrder'] = targetOrder;
        
    },

    // 申请退款对话框，刷新退款总额，错误信息等实时信息
    __renderDialog: function() {
        var $dialog = this.$dialog;
        var data = this.dialogMainData;
        var mainRI = data.mainRefundInfo;

        // 母订单支付信息
        if (mainRI) {
            var mainRITotal = mainRI.cash*1 
                + mainRI.weizoomCardMoney*1 
                + mainRI.couponMoney*1 
                + mainRI.integral*1;
            this.dialogMainData.mainRefundInfo.orderType = '母订单';
            this.dialogMainData.mainRefundInfo.totalMoney = mainRITotal;
            var $tmplTopTip = $('#mall-order-refund-dialog-top-tips-tmpl-src').tmpl(mainRI);
            $('.xa-i-refund-info-show', $dialog).html("");
            $('.xa-i-refund-info-show', $dialog).html($tmplTopTip);
        }

        // 子订单支付信息
        var subRI = data.subRefundInfo;
        if (subRI && !_.isEmpty(subRI)) {
            var subRITotal = subRI.cash*1 
                + subRI.weizoomCardMoney*1 
                + subRI.couponMoney*1 
                + subRI.integral*1;
            this.dialogMainData.subRefundInfo.orderType = '子订单';
            this.dialogMainData.subRefundInfo.totalMoney = subRITotal;
            var $tmplTopTip = $('#mall-order-refund-dialog-top-tips-tmpl-src').tmpl(subRI);
            $('.xa-i-refund-info-show', $dialog).append($("<p>").text(subRITip));
        }

        // 当前退款订单的: 退款总额
        if (data.targetOrder && data.targetOrder.totalMoney > 0) {
            var totalMoney = data.targetOrder.totalMoney;
            $('.xui-i-total-sum', $dialog).text(totalMoney);
        } else {
            $('.xui-i-total-sum', $dialog).text('0.00');
        }

        // 当前退款订单的: 积分后面的金额自动计算
        if (data.targetOrder && data.targetOrder.integral > 0) {
            $('.xa-i-integral-money').text(data.targetOrder.integral);
        } else {
            $('.xa-i-integral-money').text('0.00');
        }

        // 显示提示信息
        if (data.tips) {
            // 现金提示
            $('.xui-i-tips', $('#cash').parent()).text(data.tips.cash) 
            // 微众卡提示
            $('.xui-i-tips', $('#weizoom_card_money').parent()).text(data.tips.weizoomCardMoney) 
            // 总额提示
            $('.xui-i-total-error', $dialog).text(data.tips.totalMoney) 
        
        }

    },

    // 判断是否正确
    __validate: function() {
        var mainRI = this.dialogMainData.mainRefundInfo;
        var target = this.dialogMainData.targetOrder? this.dialogMainData.targetOrder : {};

        var tipCash = "";
        var tipTotalError = "";
        if (target.cash && target.cash*1 > 0 && target.cash*1 > mainRI.cash) {
            // 金额部分不能大于 “可退部分”
            if (mainRI.cash > 0) {
                tipCash = "最多可退" + mainRI.cash + "元";
                tipTotalError = "退款金额不等于"+target.cash+"元";
            } else {
                tipCash = "无可退金额";
                tipTotalError = ""
            }
        } else if (target.cash && target.cash*1 < 0) {
            // 输入为负数
            tipCash = "请输入正确的金额";
            tipTotalError = "输入的金额有误，请重新输入";
        }

        // 微众卡金额不能大于 “可退部分”
        var tipCard = "";
        if (target.weizoomCardMoney 
            && target.weizoomCardMoney*1 > 0 && target.weizoomCardMoney*1 > mainRI.weizoomCardMoney) {
            if (mainRI.weizoomCardMoney > 0) {
                tipCard = "最多可退" + mainRI.weizoomCardMoney + "元";
            } else {
                tipCard = "无可退金额";
            }
        } else if (target.weizoomCardMoney && target.weizoomCardMoney*1 < 0) {
            // 输入为负数
            tipCard = "请输入正确的金额";
        }

        // 保存提示信息，等待页面刷新
        this.dialogMainData['tips'] = {
            'cash': tipCash,
            'weizoomCardMoney': tipCard,
            'totalMoney': tipTotalError
        };

    },

    onChange: function() {
        console.log('changed');
        var $dialog = this.$dialog;
        // 实时计算
        this.__calcCurrentOrderRefund();

        // 处理提示信息
        this.__validate();

        // 刷新对话框
        this.__renderDialog();
    },

    onShow: function(options) {
        var $dialog = this.$dialog;
        this.orderId = options.orderId; 
        this.deliveryItemId = options.deliveryItemId;
        this.integralPerYuan = options.integralPerYuan;

        // 根据页面中的所有订单数据，整理出所需的当前订单的“子母订单”数据
        this.__fetchOrdersInfos();

        // 渲染对话框中的子母订单信息
        this.__renderDialog();

    },

    afterShow: function(options) {
    },

    onClickSubmitButton: function(event) {
        var _this = this;
        var $dialog = this.$dialog;
        var orderId = this.orderId;
        var deliveryItemId = this.deliveryItemId;
        var integralPerYuan =  parseFloat(this.integralPerYuan);
        integralPerYuan =  integralPerYuan > 0? integralPerYuan : 1;

        var cash = parseFloat($('[name="cash"]', $dialog).val());
        var weizoomCardMoney = parseFloat($('[name="weizoom_card_money"]', $dialog).val());
        var couponMoney = parseFloat($('[name="coupon_money"]', $dialog).val());
        var integralCount = parseFloat($('[name="integral"]', $dialog).val());
        var integral = integralCount/integralPerYuan;

        var params = {
                order_id: orderId,
                delivery_item_id: deliveryItemId,
                cash: cash,
                weizoom_card_money: weizoomCardMoney,
                coupon_money: couponMoney,
                integral: integral 
            };

        //////////////////////////////
        // 调试时，暂时关闭提交
        alert(JSON.stringify(params));
        return;
        //////////////////////////////

        W.getApi().call({
            app: 'mall2',
            resource: 'refunding_order',
            args: params,
            method: 'put',
            success: function(data) {
                console.log("W.getApi(): ", data, params);
                _this.renderDialog(params);
            },
            error: function(resp) {
            }
        });

    },

    onGetData: function(event) {
        xlog('in get data...');
    },

    renderDialog: function(options){
        var $dialog = $.tmpl(this.refundTemplate, options);
        var $content = $('.xui-commonOrderRefundDialog', $dialog);
        this.$('.xui-commonOrderRefundDialog').empty().append($content);
    }
});

