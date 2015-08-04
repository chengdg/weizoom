/**
 * OrderDetailPage: 订单详情页面
 */
W.page.OrderDetailPage = BackboneLite.View.extend({
    events: {
        'click #cancelOrderButton': 'onClickConfirmCancel',
        'touchstart .xui-cover': 'onClickCover',
        'mousedown .xui-cover': 'onClickCover',
        'click .xa-receipt': 'onClickConfirmReceipt',
        'click .xa-pay': 'onClickPayButton'
    },
    
    initialize: function(options) {
        xlog('in PayOrderPage');
        this.orderId = orderId;
        this.payInterfaceType = options.payInterfaceType || 0;
    },

    onClickPayButton: function() {
        if (!this.payInterfaceType) {
            return;
        }
        var args = {order_id: this.orderId};
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            args: _.extend({
                webapp_owner_id: W.webappOwnerId,
                module: 'mall',
                target_api: 'order/pay',
                interface_type: this.payInterfaceType,
                interface_id: 0
            }, args),
            success: function(data) {
                order_id = data['order_id'];
                if (data['msg'] != null) {
                    $('body').alert({
                        isShow: true,
                        speed: 2000,
                        info: data['msg'] || '操作失败!'
                    });
                    _this.enableSubmitOrderButton();
                } else {
                    window.location.href = data['url'];     
                }
            },
            error: function(resp) {
                var errMsg = null;
                if (resp.data) {
                    errMsg = resp.data['msg'];
                }
                if (!errMsg) {
                    errMsg = '操作失败!';
                }
                $('body').alert({
                    isShow: true,
                    info: errMsg,
                    speed:2000
                });
            }
        });
    },

    /**
     * onClickConfirmCancel: 点击“取消订单”确认是否删除
     */
    onClickConfirmCancel:function(){
        var cancel = confirm("确定取消订单？")
        if (cancel==true){
            this.confirmCancelOrder();
        }
    },
    /**
     * onClickConfirmReceipt: 点击“确认收货”是否确认收货
     */
    onClickConfirmReceipt:function(){
        var receipt = confirm("是否确认收货？")
        if (receipt==true){
            this.confirmReceiptOrder();
        }
    },
    
    /**
    * confirmReceiptOrder: 确定“确认收货”的响应函数
    */
    confirmReceiptOrder:function(){
        $('body').alert({
            isShow: true,
            info:'正在确认收货...',
            speed: 2000
        });
        var action = 'finish-客户';
        var args = {order_id: this.orderId, 'action': action};
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            args: _.extend({
                webapp_owner_id: W.webappOwnerId,
                module: 'mall',
                target_api: 'order_status/update'
            }, args),
            success: function(data) {
                window.location.reload();
            },
            error: function(resp) {
                $('body').alert({
                    isShow: true,
                    speed:2000
                });
            }
        });
    },
    /**
    * onClickCancelOrderBtn: 确定“取消订单”的响应函数
    */
    confirmCancelOrder: function(event) {
        $('body').alert({
            isShow: true,
            info:'正在取消订单...',
            speed: 20000
        });
        var action = 'cancel-客户';
        var args = {order_id: this.orderId, 'action': action};
        W.getApi().call({
            app: 'webapp',
            api: 'project_api/call',
            method: 'post',
            args: _.extend({
                webapp_owner_id: W.webappOwnerId,
                module: 'mall',
                target_api: 'order_status/update'
            }, args),
            success: function(data) {
                window.location.reload();
            },
            error: function(resp) {
                $('body').alert({
                    isShow: true,
                    info: resp.data['msg'],
                    speed:2000
                });
            }
        });
    },

    /**
     * onClickCover: 点击cover部分的响应函数
     */
    onClickCover: function(event) {
        $(event.currentTarget).fadeOut(100);
    }
});
