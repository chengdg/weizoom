/**
 * 微信内置浏览器的Javascript API，功能包括：
 *
 * 1、分享到微信朋友圈
 * 2、分享给微信好友
 * 3、分享到腾讯微博
 * 4、隐藏/显示右上角的菜单入口
 * 5、隐藏/显示底部浏览器工具栏
 * 6、获取当前的网络状态
 * 7、调起微信客户端的图片播放组件
 * 8、关闭公众平台Web页面
 *
 * 部分功能可能被微信禁用
 */
W.WeixinJsApi = {

    author : "chuter",
    version : "1.0",

    /**
     * removeParameter: 从url中移除指定的参数
     *  return 修改后的url
     */
    _removeUrlParameter : function(url, parameter) {
        var returnUrl = url;
        var urlparts = returnUrl.split('?');

        if (urlparts.length >= 2) {
            var urlBase = urlparts.shift(); //get first part, and remove from array
            var queryString = urlparts.join("?"); //join it back up

            var prefix = encodeURIComponent(parameter) + '=';
            var pars = queryString.split(/[&;]/g);
            for (var i = pars.length; i-->0;) {             //reverse iteration as may be destructive
                if (pars[i].lastIndexOf(prefix, 0) !== -1) {   //idiom for string.startsWith
                    pars.splice(i, 1);
                }
            }
            returnUrl = urlBase + '?' + pars.join('&');
        }
      
        return returnUrl;
    },

    /**
     * 分享到微信朋友圈

     * @param data为待分享的信息，包括：
     * appId
     * imageUrl //指定一个分享出去后显示的封面图片
     * link //指定分享出去的信息的链接地址
     * desc //分享信息的摘要信息
     * title //分享信息的标题
     *
     * @param callbacks为相关回调方法，包括：
     * async //ready方法是否需要异步执行，默认false
     * ready(argv) //就绪状态
     * dataLoaded(data)  //数据加载完成后调用，async为true时有用，也可以为空
     * cancel(resp)
     * fail(resp)   
     * confirm(resp) //成功
     * all(resp)   //无论成功失败都会执行的回调
     */
    shareToTimeline : function(data, callbacks) {
        var _this = this;
        callbacks = callbacks || {};
        var shareTimeline = function (theData) {
            WeixinJSBridge.invoke('shareTimeline', {
                "appid":theData.appId ? theData.appId : '',
                "img_url":theData.imgUrl,
                "link":_this._removeUrlParameter(theData.link, 'sct'),
                "desc":theData.title,
                "title":theData.desc, // 注意这里要分享出去的内容是desc
                "img_width":"120",
                "img_height":"120"
            }, function (resp) {
                switch (resp.err_msg) {
                    // share_timeline:cancel 用户取消
                    case 'share_timeline:cancel':
                        callbacks.cancel && callbacks.cancel(resp);
                        break;
                    // share_timeline:fail　发送失败
                    case 'share_timeline:fail':
                        callbacks.fail && callbacks.fail(resp);
                        break;
                    // share_timeline:confirm 发送成功
                    case 'share_timeline:confirm':
                    case 'share_timeline:ok':
                        callbacks.confirm && callbacks.confirm(resp);
                        break;
                }
                // 无论成功失败都会执行的回调
                callbacks.all && callbacks.all(resp);
            });
        };
        WeixinJSBridge.on('menu:share:timeline', function (argv) {
            if (callbacks.async && callbacks.ready) {
                window["_wx_loadedCb_"] = callbacks.dataLoaded || new Function();
                if(window["_wx_loadedCb_"].toString().indexOf("_wx_loadedCb_") > 0) {
                    window["_wx_loadedCb_"] = new Function();
                }
                callbacks.dataLoaded = function (newData) {
                    window["_wx_loadedCb_"](newData);
                    shareTimeline(newData);
                };
                // 然后就绪
                callbacks.ready && callbacks.ready(argv);
            } else {
                // 就绪状态
                callbacks.ready && callbacks.ready(argv);
                shareTimeline(data);
            }
        });
    },

    /**
     * 发送给微信上的好友
     *
     * @param data为待分享的信息，包括：
     * appId
     * imageUrl //指定一个分享出去后显示的封面图片
     * link //指定分享出去的信息的链接地址
     * desc //分享信息的摘要信息
     * title //分享信息的标题
     *
     * @param callbacks为相关回调方法，包括：
     * async //ready方法是否需要异步执行，默认false
     * ready(argv) //就绪状态
     * dataLoaded(data)  //数据加载完成后调用，async为true时有用，也可以为空
     * cancel(resp)
     * fail(resp)   
     * confirm(resp) //成功
     * all(resp)   //无论成功失败都会执行的回调
     */
    sendToFriend : function(data, callbacks) {
        var _this = this;
        callbacks = callbacks || {};
        var sendAppMessage = function (theData) {
            WeixinJSBridge.invoke('sendAppMessage', {
                "appid":theData.appId ? theData.appId : '',
                "img_url":theData.imgUrl,
                "link": _this._removeUrlParameter(theData.link, 'sct'),
                "desc":theData.desc,
                "title":theData.title,
                "img_width":"120",
                "img_height":"120"
            }, function (resp) {
                switch (resp.err_msg) {
                    // send_app_msg:cancel 用户取消
                    case 'send_app_msg:cancel':
                        callbacks.cancel && callbacks.cancel(resp);
                        break;
                    // send_app_msg:fail　发送失败
                    case 'send_app_msg:fail':
                        callbacks.fail && callbacks.fail(resp);
                        break;
                    // send_app_msg:confirm 发送成功
                    case 'send_app_msg:confirm':
                    case 'send_app_msg:ok':
                        callbacks.confirm && callbacks.confirm(resp);
                        break;
                }
                // 无论成功失败都会执行的回调
                callbacks.all && callbacks.all(resp);
            });
        };
        WeixinJSBridge.on('menu:share:appmessage', function (argv) {
            if (callbacks.async && callbacks.ready) {
                window["_wx_loadedCb_"] = callbacks.dataLoaded || new Function();
                if(window["_wx_loadedCb_"].toString().indexOf("_wx_loadedCb_") > 0) {
                    window["_wx_loadedCb_"] = new Function();
                }
                callbacks.dataLoaded = function (newData) {
                    window["_wx_loadedCb_"](newData);
                    sendAppMessage(newData);
                };
                // 然后就绪
                callbacks.ready && callbacks.ready(argv);
            } else {
                // 就绪状态
                callbacks.ready && callbacks.ready(argv);
                sendAppMessage(data);
            }
        });
    },

    /**
     * 分享到腾讯微博

     * @param data为待分享的信息，包括：
     * link //指定分享出去的信息的链接地址
     * desc //分享信息的摘要信息
     *
     * @param callbacks为相关回调方法，包括：
     * async //ready方法是否需要异步执行，默认false
     * ready(argv) //就绪状态
     * dataLoaded(data)  //数据加载完成后调用，async为true时有用，也可以为空
     * cancel(resp)
     * fail(resp)   
     * confirm(resp) //成功
     * all(resp)   //无论成功失败都会执行的回调
     */
    shareToTecentWeibo : function(data, callbacks) {
        var _this = this;
        callbacks = callbacks || {};
        var shareWeibo = function (theData) {
            WeixinJSBridge.invoke('shareWeibo', {
                "content":theData.desc,
                "link":_this._removeUrlParameter(theData.link, 'sct')
            }, function (resp) {
                switch (resp.err_msg) {
                    // share_weibo:cancel 用户取消
                    case 'share_weibo:cancel':
                        callbacks.cancel && callbacks.cancel(resp);
                        break;
                    // share_weibo:fail　发送失败
                    case 'share_weibo:fail':
                        callbacks.fail && callbacks.fail(resp);
                        break;
                    // share_weibo:confirm 发送成功
                    case 'share_weibo:confirm':
                    case 'share_weibo:ok':
                        callbacks.confirm && callbacks.confirm(resp);
                        break;
                }
                // 无论成功失败都会执行的回调
                callbacks.all && callbacks.all(resp);
            });
        };
        WeixinJSBridge.on('menu:share:weibo', function (argv) {
            if (callbacks.async && callbacks.ready) {
                window["_wx_loadedCb_"] = callbacks.dataLoaded || new Function();
                if(window["_wx_loadedCb_"].toString().indexOf("_wx_loadedCb_") > 0) {
                    window["_wx_loadedCb_"] = new Function();
                }
                callbacks.dataLoaded = function (newData) {
                    window["_wx_loadedCb_"](newData);
                    shareWeibo(newData);
                };
                // 然后就绪
                callbacks.ready && callbacks.ready(argv);
            } else {
                // 就绪状态
                callbacks.ready && callbacks.ready(argv);
                shareWeibo(data);
            }
        });
    },

    /**
     * 使用微信Native的图片播放组件
     * 这里必须对参数进行强检测，如果参数不合法，直接会导致微信客户端crash
     *
     * @param curSrc 当前播放的图片地址
     * @param srcList 图片地址列表
     */
    imagePreview : function(curSrc, srcList) {
        if(!curSrc || !srcList || srcList.length == 0) {
            return;
        }
        WeixinJSBridge.invoke('imagePreview', {
            'current' : curSrc,
            'urls' : srcList
        });
    },

    /**
     * 显示网页右上角的按钮
     */
    showOptionMenu : function() {
        WeixinJSBridge.call('showOptionMenu');
    },


    /**
     * 隐藏网页右上角的按钮
     */
    hideOptionMenu : function() {
        WeixinJSBridge.call('hideOptionMenu');
    },

    /**
     * 显示底部工具栏
     */
    showToolbar : function() {
        WeixinJSBridge.call('showToolbar');
    },

    /**
     * 隐藏底部工具栏
     */
    hideToolbar : function() {
        WeixinJSBridge.call('hideToolbar');
    },

    /**
     * 获取当前用户网络状态

     * 返回如下几种类型：
     *
     * network_type:wifi     wifi网络
     * network_type:edge     非wifi,包含3G/2G
     * network_type:fail     网络断开连接
     * network_type:wwan     2g或者3g
     *
     * 使用方法：
     * W.WeixinJsApi.getNetworkType(function(networkType){
     *
     * });
     *
     * @param callback
     */
    getNetworkType : function(callback) {
        if (callback && typeof callback == 'function') {
            WeixinJSBridge.invoke('getNetworkType', {}, function (e) {
                // 在这里拿到e.err_msg，这里面就包含了所有的网络类型
                callback(e.err_msg);
            });
        }
    },

    /**
     * 关闭当前微信公众平台页面
     */
    closeWindow : function (callbacks) {
        callbacks = callbacks || {};
        WeixinJSBridge.invoke("closeWindow", {}, function(resp) {
            switch (resp.err_msg) {
                // 关闭成功
                case 'close_window:ok':
                    callbacks.success && callbacks.success(resp);
                    break;
                // 关闭失败
                default :
                    callbacks.fail && callbacks.fail(resp);
                    break;
            }
        });
    },

    /**
     * 当页面加载完毕后执行，使用方法：
     *
     * WeixinApi.ready(function(Api){
     *     // 从这里只用Api即是W.WeixinJsApi
     * });
     *
     * @param readyCallback
     */
    ready : function(readyCallback) {
        if (readyCallback && typeof readyCallback == 'function') {
            var Api = this;
            var wxReadyFunc = function () {
                readyCallback(Api);
            };
            if (typeof window.WeixinJSBridge == "undefined"){
                if (document.addEventListener) {
                    document.addEventListener('WeixinJSBridgeReady', wxReadyFunc, false);
                } else if (document.attachEvent) {
                    document.attachEvent('WeixinJSBridgeReady', wxReadyFunc);
                    document.attachEvent('onWeixinJSBridgeReady', wxReadyFunc);
                }
            } else{
                wxReadyFunc();
            }
        }
    }
}