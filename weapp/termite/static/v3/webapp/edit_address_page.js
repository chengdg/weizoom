/**
 * Backbone View in Mobile
 */
W.page.EditAddressPage = W.page.InputablePage.extend({
    events: _.extend({
        'click .xa-submit': 'onClickSubmitButton'
    }, W.page.InputablePage.prototype.events),
    
    initialize: function(options) {
        xlog('in EditAddressPage');
        this.redirectUrlQueryString = options.redirectUrlQueryString;
    },

    /**
     * onClickSubmitButton: 点击“提交”按钮的响应函数
     */
    onClickSubmitButton: function(event) {
        var $form = $('form');
        if (W.validate($form)) {
            var args = $form.serializeObject();
            W.getApi().call({
                app: 'webapp',
                api: 'project_api/call',
                method: 'post',
                args: _.extend(args, {
                    woid: W.webappOwnerId,
                    module: 'mall',
                    target_api: 'address/save'
                }),
                success: function(data) {
                    var shipName = data['ship_name'];
                    if (data['msg'] != null) {
                        $('body').alert({
                            isShow: true,
                            speed: 2000,
                            isSlide: true,
                            info: data['msg']
                        })
                    } else {
                        alert("---log----112233445566",this.redirectUrlQueryString);
                        window.location.href = "./?"+this.redirectUrlQueryString;
                    }
                },
                error: function(resp) {
                    var errMsg = '保存失败';
                    if (resp.errMsg) {
                        errMsg = resp.errMsg;
                    } else if (resp.data && resp.data['msg']) {
                        errMsg = resp.data['msg']
                    }

                    $('body').alert({
                        isShow: true,
                        isSlide: true,
                        info: errMsg,
                        speed: 2000
                    });
                }
            });
        } else {
            
        }
    }
});
