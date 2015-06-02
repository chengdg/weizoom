/*
Copyright (c) 2011-2012 Weizoom Inc
*/


/**
 * 自助绑定
 * 
 * author: chuter
 */
ensureNS('W.weapp.dialog.BindMpUserDialog');

W.weapp.dialog.BindMpUserDialog = W.dialog.Dialog.extend({
    events: _.extend({
        'click #bindMpUser-bindBtn': 'onClickBindBtn'
    }, W.dialog.Dialog.prototype.events),

    getTemplate: function() {
        $('#bind-mpuser-dialog-tmpl-src').template('bind-mpuser-dialog-tmpl');
        return "bind-mpuser-dialog-tmpl";
    },

    onInitialize: function(options) {
    },

    onShow: function(options) {
    },

    /**
     * onClickBindBtn: 点击“绑定”按钮后的响应函数
     */
    onClickBindBtn: function(event) {
        W.getApi().call({
            app: 'account',
            api: 'mpuser/emulate_bind',
            args: {},
            success: function(data) {
                alert('绑定成功');
            },
            error: function(resp) {
                alert('绑定失败！请重试！')
            }
        })
    },

    /**
     * onClickSubmitButton: 点击“确定”按钮后的响应函数
     */
    onClickSubmitButton: function(event) {
        $('#bind_button').attr('disabled','disabled');
        W.getLoadingView().show();

        var _this = this;

        this.onGetDataAsync(event, function(data) {
            _this.$dialog.modal('hide');
            if (_this.successCallback) {
                //调用success callback
                var task = new W.DelayedTask(function() {
                    _this.successCallback(data);
                    _this.successCallback = null;
                });
              
                task.delay(100);
            }
        }, function() {
            W.getLoadingView().hide();
            $('#bind_button').removeAttr('disabled');
        });
    },

    onGetDataAsync: function(event, success_callback, failed_callback) {
        if (!W.validate()) {
            W.getLoadingView().hide();
            $('#bind_button').removeAttr('disabled');
            return false;
        }

        var appid = $.trim(this.$dialog.find('input[name="appid"]').val());
        var secret = $.trim(this.$dialog.find('input[name="secret"]').val());
        var mpusername = $.trim(this.$dialog.find('input[name="mpusername"]').val());

        var mp_type = $('input[name=mp_type]:radio:checked').val();
        var is_certified = $('input[name=is_certified]:radio:checked').val();
        var aeskey = $('input[name=aeskey]:radio:checked').val();
        var encode_aeskey = $('input[name="encode_aeskey"]').val();
        if (is_certified == 'true' && (appid.length == 0 || secret.length == 0)) {
            W.getLoadingView().hide();
            $('#bind_button').removeAttr('disabled');
            W.getErrorHintView().show('已经认证的账号必须填写appid和appsecret！');
            return false;
        }

        if (aeskey == '2'){
            if (encode_aeskey == ''){
            W.getLoadingView().hide();
            $('#bind_button').removeAttr('disabled');
            W.getErrorHintView().show('加密模式必须填写EncodingAESKey');
            return false;
            }
        }

        if (appid.length == 0 && secret.length == 0) {
            //校验是否完成绑定
            W.getApi().call({
                app: 'account',
                api: 'bind_status/get',
                async: false,
                args: {
                    mp_type: mp_type,
                    is_certified: is_certified,
                    mpusername: mpusername,
                    aeskey:aeskey,
                    aeskey:aeskey
                },
                scope: this,
                success: function(data) {
                    if (data.is_binded) {
                        success_callback(data);
                    } else {
                        W.getErrorHintView().show('没有完成绑定，请确认在微信中已经完成绑定！');
                        failed_callback();
                    }                    
                },
                error: function(resp) {
                    //TODO 进行错误通知
                    W.getErrorHintView().show('服务繁忙，请稍后重试！');
                    failed_callback();
                }
            });
        } else if(appid.length > 0 && secret.length > 0) {
            //先校验是否完成绑定，然后校验appid和appsecret是否正确
            //校验是否完成绑定
            W.getApi().call({
                app: 'account',
                api: 'bind_status/get',
                async: false,
                args: {
                    mp_type: mp_type,
                    is_certified: is_certified
                },
                scope: this,
                success: function(data) {
                    if (data.is_binded) {
                        //校验填写的appid和appsecret是否正确
                        W.getApi().call({
                            app: 'account',
                            api: 'mpuser_access_token/create',
                            async: false,
                            args: {
                                appid: appid,
                                secret: secret
                            },
                            scope: this,
                            success: function(data) {
                                success_callback(data);                   
                            },
                            error: function(resp) {
                                W.getErrorHintView().show('Appid,AppSecret验证失败: ' + resp.errMsg);
                                failed_callback();
                            }
                        });
                    } else {
                        W.getErrorHintView().show('没有完成绑定，请确认在微信中已经完成绑定！');
                        failed_callback();
                    }                    
                },
                error: function(resp) {
                    //TODO 进行错误通知
                    W.getErrorHintView().show('服务繁忙，请稍后重试！');
                    failed_callback();
                }
            });
        } else {
            alert('请输入正确的Appid和AppSecret!');
            failed_callback();
        }
    },

    /**
     * onClickSubmitButton: 点击“完成”按钮后的响应函数
     */
    onGetData: function(event) {
        var appid = $.trim(this.$dialog.find('input[name="appid"]').val());
        var token = $.trim(this.$dialog.find('input[name="token"]').val());

        var mp_type = $('input[name=mp_type]:radio:checked').val();
        var is_certified = $('input[name=is_certified]:radio:checked').val();

        var has_bind = false;

        if (appid.length == 0 && token.length == 0) {
            //校验是否完成绑定
            W.getApi().call({
                app: 'account',
                api: 'bind_status/get',
                async: false,
                args: {
                    mp_type: mp_type,
                    is_certified: is_certified
                },
                scope: this,
                success: function(data) {
                    if (data.is_binded) {
                        has_bind = true;
                    } else {
                        W.getErrorHintView().show('没有完成绑定，请确认在微信中已经完成绑定！');
                    }

                    event.success_call_back();
                },
                error: function(resp) {
                    //TODO 进行错误通知
                    W.getErrorHintView().show('服务繁忙，请稍后重试！');
                }
            });
        } else if(appid.length > 0 && token.length > 0) {
            //先校验是否完成绑定，然后校验appid和appsecret是否正确

        } else {
            alert('请输入正确的Appid和AppSecret!');
        }

        return has_bind;
    }
});