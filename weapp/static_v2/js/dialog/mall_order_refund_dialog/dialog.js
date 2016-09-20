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
        'keyup .xui-commonOrderRefundDialog input': 'onKeyUpRefundItem',
        'change .xui-commonOrderRefundDialog input': 'onChangeRefundItem',
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
    // 显示在退款对话框中
    __fetchOrdersInfos: function() {
        var _this = this;
        var allData = JSON.parse($('#origin-data').text());
        var orders = allData.items;

        // 新建带key的object所有订单数据，便于查找
        this.allOrders = {};
        orders.map(function(order){
            _this.allOrders[order.id] = order;
        });

        // 找出母订单中支付金额, 微众卡，等信息并保存
        var allOrders = this.allOrders;
        var mainOrder = allOrders[this.orderId];
        var mainRefundInfo = {
            cash: mainOrder.origin_final_price,
            weizoomCardMoney: mainOrder.origin_weizoom_card_money,
            couponMoney: mainOrder.coupon_money,
            integral: mainOrder.integral
        };

        // 找出其它子订单的已支付的金额、微众卡等信息, 然后合并之
        var subRefundInfo = [];
        var targetRefundInfo = {};
        var mergeSubOrder = {
            cash: 0,
            weizoomCardMoney: 0,
            couponMoney: 0,
            integral: 0
        };
        mainOrder.groups.map(function(subOrder){
            var _subOrder = subOrder.fackorder;
            var _subRI = _subOrder.refund_info;
            if ((_subOrder.order_status == 6 || _subOrder.order_status == 7) && !_.isEmpty(_subOrder.refund_info)) {
                // 找出退款中, 退款完成的订单, 并合计
                mergeSubOrder.cash += _subRI.cash;
                mergeSubOrder.weizoomCardMoney += _subRI.weizoom_card_money,
                mergeSubOrder.couponMoney += _subRI.coupon_money,
                mergeSubOrder.integral += _subRI.integral_money
                mergeSubOrder.totalMoney = mergeSubOrder.cash + mergeSubOrder.weizoomCardMoney + mergeSubOrder.couponMoney + mergeSubOrder.integral;

            } else if (_subOrder.id == _this.deliveryItemId && !_.isEmpty(_subOrder.refund_info)) {
                // 找出当前编辑的子订单
                targetRefundInfo = {
                   shouldTotal: _subOrder.refund_info.should_total 
                }
            }
        }); 

        // 将合计后的子订单放入this.mainOrderData
        if (mergeSubOrder && mergeSubOrder.totalMoney > 0) {
            subRefundInfo.push(mergeSubOrder);
        }

        // 保存mall_type属性，兼容非自营
        var mallType = allData.mall_type;

        this.dialogMainData = {
            'mallType': mallType,               // 全部数据，包括订单和其它内容
            'mainOrder': mainOrder,             // 字母订单
            'mainRefundInfo': mainRefundInfo,   // 母订单
            'subRefundInfo': subRefundInfo,     // 子订单
            'targetRefundInfo': targetRefundInfo// 当前订单
        };

        // 校验并提示信息
        this.__validate(false);

        console.log( '订单信息：%o', this.dialogMainData);
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
        var integralMoney = integralCount/integralPerYuan * 1;

        // 不能为负数
        var cash = cash > 0? cash : 0;
        var weizoomCardMoney = weizoomCardMoney > 0? weizoomCardMoney : 0;
        var couponMoney = couponMoney > 0? couponMoney : 0;
        var integralMoney = integralMoney > 0? integralMoney : 0;

        var totalMoney = cash + weizoomCardMoney + couponMoney + integralMoney;

        // 保存至this.dialogMainData
        var targetRefundInfo = {
            "cash": cash,
            "weizoomCardMoney": weizoomCardMoney,
            "couponMoney": couponMoney,
            "integral": integralMoney,
            "integralCount": integralCount,
            "totalMoney": totalMoney.toFixed(2)
        };
        this.dialogMainData.targetRefundInfo = _.extend(this.dialogMainData.targetRefundInfo, targetRefundInfo);
        
        // 处理提示信息
        this.__validate(false);
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
            this.dialogMainData.mainRefundInfo.orderType = '母订单支付金额';
            this.dialogMainData.mainRefundInfo.totalMoney = mainRITotal;
            var $tmplTopTip = $('#mall-order-refund-dialog-top-tips-tmpl-src').tmpl(mainRI);
            $('.xa-i-refund-info-show', $dialog).html("");
            $('.xa-i-refund-info-show', $dialog).html($tmplTopTip);
        }

        // 子订单支付信息
        var _this = this;
        var subRIs = data.subRefundInfo;
        subRIs.map(function(subRI){
            if (subRI && !_.isEmpty(subRI)) {
                var subRITotal = subRI.cash*1 
                    + subRI.weizoomCardMoney*1 
                    + subRI.couponMoney*1 
                    + subRI.integral*1;
                subRI.orderType = '已录入退款金额';
                subRI.totalMoney = subRITotal;
                var $subRITip = $('#mall-order-refund-dialog-top-tips-tmpl-src').tmpl(subRI);
                $('.xa-i-refund-info-show', $dialog).append($subRITip);
            }
        });

        // 当前退款订单的: 退款总额
        if (data.targetRefundInfo && data.targetRefundInfo.totalMoney > 0) {
            var totalMoney = data.targetRefundInfo.totalMoney;
            $('.xui-i-total-sum', $dialog).text(totalMoney);
        } else {
            $('.xui-i-total-sum', $dialog).text('0.00');
        }

        // 当前退款订单的: 标题上的应退金额
        if (data.targetRefundInfo && data.targetRefundInfo.shouldTotal > 0) {
            var shouldTotal = data.targetRefundInfo.shouldTotal;
            $('.xui-i-should-total', $dialog).text(shouldTotal.toFixed(2));
        } else {
            $('.xui-i-should-total', $dialog).text(0.00);
        }

        // 当前退款订单的: 积分后面的金额自动计算
        if (data.targetRefundInfo && data.targetRefundInfo.integral > 0) {
            $('.xa-i-integral-money').text(data.targetRefundInfo.integral.toFixed(2));
        } else {
            $('.xa-i-integral-money').text('0.00');
        }

        // 最终的校验，不符合应退金额时，将焦点定到cash对话框里
        if (data.tips.totalMoney.length > 0) {
            $('[name=cash]').focus();
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

    // 判断提交的金额等数值是否符合要求
    // isSumit: 提交时校验:true, 否则:false
    __validate: function(isSubmit) {
        var mainRI = this.dialogMainData.mainRefundInfo;
        var subRIs = this.dialogMainData.subRefundInfo;
        var target = this.dialogMainData.targetRefundInfo? this.dialogMainData.targetRefundInfo : {};

        // 计算最多可退金额
        var limitCash = 0;
        subRIs.map(function(subRI){
            limitCash += subRI.cash;
        });
        limitCash = mainRI.cash - limitCash;

        // 计算最多可退微众卡
        var limitCard = 0;
        subRIs.map(function(subRI){
            limitCard += subRI.weizoomCardMoney;
        });
        limitCard = mainRI.weizoomCardMoney - limitCard;

        // 计算必须满足的总退款金额合计，可由优惠券和积分补充，提交前必须满足
        var limitTotal = 0;
        limitTotal = target.shouldTotal;

        // 开始判断金额部分
        var tipCash = "";
        var tipTotalError = "";
        if (target.cash && target.cash*1 > 0 && target.cash*1 <= limitCash) {
            tipCash = "";
        } else if (target.cash && target.cash*1 > 0 && target.cash*1 > limitCash) {
            // 金额部分不能大于 “可退部分”
            if (target.cash > 0) {
                tipCash = "最多可退" + limitCash.toFixed(2) + "元";
            } else {
                tipCash = "无可退金额";
            }
        } else if (target.cash && target.cash*1 < 0) {
            // 输入为负数
            tipCash = "请输入正确的金额";
        }

        // 微众卡金额不能大于 “可退部分”
        var tipCard = "";
        if (target.weizoomCardMoney && target.weizoomCardMoney*1 > 0 && target.weizoomCardMoney*1 <= limitCard) {
            tipCard = "";

        } else if (target.weizoomCardMoney && target.weizoomCardMoney*1 > 0 && target.weizoomCardMoney*1 > limitCard) {
            if (target.weizoomCardMoney > 0) {
                tipCard = "最多可退" + limitCard + "元";
            } else {
                tipCard = "无可退微众卡";
            }

        } else if (target.weizoomCardMoney && target.weizoomCardMoney*1 < 0) {
            // 输入为负数
            tipCard = "请输入正确的金额";
        }

        // 计算最后提交前的退款金额
        if (target.totalMoney && target.totalMoney*1 > 0 && target.totalMoney*1 === limitTotal*1) {
            tipTotalError = "";

        } else if (target.totalMoney && target.totalMoney*1 >= 0 && target.totalMoney*1 !== limitTotal*1) {
            tipTotalError = "退款金额不等于"+limitTotal+"元";

        } else if (_.isUndefined(target.totalMoney)) {
            tipTotalError = "退款金额不等于"+limitTotal+"元";
        }

        // 保存提示信息，等待页面刷新
        this.dialogMainData['tips'] = {
            'cash': tipCash,
            'weizoomCardMoney': tipCard,
            'totalMoney': isSubmit? tipTotalError : ''
        };

        this.__renderDialog();

        if (tipCash.length == 0 && tipCard.length == 0 && tipTotalError.length == 0) {
            return true;
        } else {
            return false;
        }

    },

    __initDialog: function() {
        var $dialog = this.$dialog;
        $('[name="cash"]', $dialog).val('').focus();
        $('[name="weizoom_card_money"]', $dialog).val('');
        $('[name="coupon_money"]', $dialog).val('');
        $('[name="integral"]', $dialog).val('');
    },

    onChangeRefundItem: function() {
        var $dialog = this.$dialog;

        // 转换当前对话框中的退款信息
        var $cash = $('[name="cash"]', $dialog);
        var $weizoomCardMoney = $('[name="weizoom_card_money"]', $dialog);
        var $couponMoney = $('[name="coupon_money"]', $dialog);
        var $integralCount = $('[name="integral"]', $dialog);

        var cash = $cash.val() * 1;
        var weizoomCardMoney = $weizoomCardMoney.val() * 1;
        var couponMoney = $couponMoney.val() * 1;
        var integralCount = $integralCount.val() * 1;

        var regNum =/^[0-9]+([.]\d{1,2})?$/;
        var regInt =/^[0-9]\d*$/;
        var errTip = '';
        if(!regNum.test(cash)){
            errTip = '现金: 须非负数，保留两位小数';
            $('.xui-i-total-error').text(errTip);
            $cash.addClass('form-control-error');
            return false;
        } else {
            $cash.removeClass('form-control-error');
        }

        if (!regNum.test(weizoomCardMoney)) {
            errTip = '微众卡: 须非负数，保留两位小数';
            $('.xui-i-total-error').text(errTip);
            $weizoomCardMoney.addClass('form-control-error');
            return false;
        } else {
            $weizoomCardMoney.removeClass('form-control-error');
        } 

        if (!regNum.test(couponMoney)) {
            errTip = '优惠券: 须非负数，保留两位小数';
            $('.xui-i-total-error').text(errTip);
            $couponMoney.addClass('form-control-error');
            return false;
        } else {
            $couponMoney.removeClass('form-control-error');
        }  

        if (!regInt.test(integralCount)) {
            errTip = '积分: 须非负整数';
            $('.xui-i-total-error').text(errTip);
            $integralCount.addClass('form-control-error');
            return false;
        } else {
            $integralCount.removeClass('form-control-error');
        }  

        if (errTip == '') {
            $cash.removeClass('form-control-error');
            $weizoomCardMoney.removeClass('form-control-error');
            $couponMoney.removeClass('form-control-error');
            $integralCount.removeClass('form-control-error');
        }

        $('.xui-i-total-error').text(errTip);
        return true;
    },

    onKeyUpRefundItem: function() {
        var $dialog = this.$dialog;
        // 实时计算
        this.__calcCurrentOrderRefund();

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
        this.__initDialog();
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
                cash: cash? cash : 0,
                weizoom_card_money: weizoomCardMoney? weizoomCardMoney : 0,
                coupon_money: couponMoney? couponMoney : 0,
                integral: integralCount? integralCount : 0 
            };

        // TODO: 
        if (this.__validate(true) && this.onChangeRefundItem()) {
            W.getApi().call({
                app: 'mall2',
                resource: 'refunding_order',
                args: params,
                method: 'put',
                success: function(data) {
                    console.log("W.getApi(): ", data, params);
                    _this.$dialog.modal('hide');
                    $('[data-ui-role="advanced-table"]').data('view').reload();
                },
                error: function(resp) {
                    console.log('mall2/refunding_order: %o', resp);
                }
            });
        }

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

