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
            var ship_info = deepCopyJSON(args);
            console.log('arg_type:',args,typeof(args));
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
                    var ship_id = data['ship_id'];
                    var ship_infos;
                    if(localStorage.ship_infos){
                        ship_infos = JSON.parse(localStorage.ship_infos);

                    }
                    else{
                        ship_infos = JSON.constructor();
                    }

                    ship_infos[ship_id] = JSON.stringify(ship_info);
                    setCreatedAt(ship_infos);
                    localStorage.ship_infos = JSON.stringify(ship_infos);


                    if (data['msg'] != null) {
                        $('body').alert({
                            isShow: true,
                            speed: 2000,
                            isSlide: true,
                            info: data['msg']
                        })
                    } else {
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
