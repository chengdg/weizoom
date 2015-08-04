/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信模拟器
 * @class
 */

//W.PhoneView = Backbone.View.extend({
ensureNS('W.view.common');
W.view.common.WeixinSimulator = Backbone.View.extend({
    el: '',

    events: {
        'submit #weixin-form': 'onSubmit',
        'click #userSelect button': 'onSelectUser',
        'click div.wx-message-link': 'onClickMessageLink',
        'click #back-weixin-btn': 'onClickBackBtn',
        'click #weixin-unsubscribe-btn': 'onClickUnsubscribeBtn',
        'click #weixin-menubar-btn': 'onClickMenubarBtn',
        'click #screen a': 'onClickLink'
    },

    getTemplate: function() {
        $('#weixin-simulator-tmpl-src').template('weixin-simulator-tmpl');

        return 'weixin-simulator-tmpl'
    },
    
    initialize: function(options) {
        this.$el = $(this.el);

        this.webappId = options.webappId || "";
        this.title = options.title || "";
        this.timelineContainer = null;

        this.isLogined = options.isLogined || false; //是否处于登录状态
        this.isInDevMode = options.isInDevMode || false; //是否处于开发模式
        this.mpUsers = options.mpUsers || []; //已经存在的公众号集合

        this.template = this.getTemplate();

        this.customerTmpl = new W.Template(
                                '<div class="mt20 customer">'+
                                    '<div class="profile customer-profile"><img src="/static/img/weixin-customer.jpg" width="45"/></div>'+
                                    '<div class="content">${content}</div>'+
                                    '<div class="cb"></div>'+
                                '</div>');

        this.$menubar = null;
        this.menus = options.menus || []; //菜单数据
        xlog(this.menus);
    },

    openBrowser: function(link) {
        xlog('open browser...');
        if (!link) {
            return;
        }
        $('#timeline-zone').hide();
        $('#browser-zone').animate({
            left: '0'
        }, 400, function() {
            $('#mobile-browser').attr('src', link);
        });
        this.isBrowserVisible = true;
    },

    refreshBrowser: function() {
        xlog('refresh browser');
        var browser = $('#mobile-browser');
        var link = browser.attr('src');
        browser.attr('src', link);
    },

    closeBrowser: function() {
        xlog('close browser...');
        $('#browser-zone').animate({
            left: '100%'
        }, 400, function() {
            $('#mobile-browser').attr('src', '/loading/');
            $('#screen').scrollTop(10000);
        });
        $('#timeline-zone').show();
        this.isBrowserVisible = false;
    },

    isViewWebapp: function() {
        return this.isBrowserVisible;
    },

    /**
     * 渲染html结果
     */
    render: function() {
        this.$el.html($.tmpl(this.template, {
            webappId: this.webappId,
            title: this.title,
            isLogined: this.isLogined,
            mpUsers: this.mpUsers
        }));

        this.timelineContainer = this.$el.find('#timeline-zone');

        //如果存在编辑框，focus
        var input = this.$el.find('#weixinInput-contentInput');
        if (input) {
            input.focus();
        }

        if (this.isLogined) {
            //发送关注事件
            this.sendSubscribeEvent();
        }

        var checkMpUserReply = _.bind(this.checkMpUserReply, this);
        setInterval(checkMpUserReply, 5000);

        //处理menubar
        this.$menubar = this.$('#menubar-zone');
        if (this.$menubar.length > 0) {
            this.menubar = new W.view.weixin.EmbededPhoneMenuBar({
                el: this.$menubar,
                mode: 'action'
            });
            this.menubar.bind('click-menubar-edit-button', function() {
                this.$menubar.slideUp('fast');
            }, this)
            this.menubar.bind('click-menu', function(menuId) {
                xlog('[phone]: click menu ' + menuId);
                var content = 'MENU_QUERY_' + menuId;
                var weixinUserName = this.getWeixinUserName();
                W.getApi().call({
                    app: 'simulator',
                    api: 'menu_event_response/get',
                    method: 'post',
                    args: {
                        from_user: weixinUserName,
                        content: content,
                        webapp_id: webappId,
                    },
                    success: function(data) {
                        if (data != 'unknown_type') {
                            this.timelineContainer.append(data);
                        }
                        $('#screen').scrollTop(10000);
                    },
                    error: function(resp) {
                        xlog(resp);
                    },
                    scope: this
                });
            }, this);
        }

        //加载菜单数据
        W.getLoadingView().show();
        W.getApi().call({
            app: 'weixin/manage/customized_menu',
            api: 'menus/get',
            args: {},
            scope: this,
            success: function(menus) {
                W.getLoadingView().hide();
                this.menubar.addMenus(menus);
            },
            error: function(resp) {
                W.getLoadingView().hide();
                alert('加载菜单数据失败!');
            }
        });
    },

    /**
     *addMenus: 添加菜单数据
     */
    addMenus: function(menus) {
        if (this.menubar) {
            this.menubar.addMenus(menus);
        }
    },
    
    /**
     * 获得微信用户的名字
     */
    getWeixinUserName: function() {
        var name = $('#userSelect select[name="weixin_user_name"]').val();
        if (!name) {
            name = 'weizoom';
        }

        return name;
    },

    /**
     * 获得微信公众账号的名字
     */
    getWebappId: function() {
        var name = $('#userSelect select[name="mp_user_name"]').val();
        if (!name) {
            name = this.webappId;
        }

        return name;
    },

    checkMpUserReply: function() {
        var weixinUserName = this.getWeixinUserName();
        var webappId = this.getWebappId();
        if (weixinUserName == '-1' || webappId == '-1') {
            xlog('use has not been selected');
            return;
        }
        W.getApi().call({
            app: 'account',
            api: 'weixin_mp_user_temp_messages/get',
            args: {
                webapp_id: webappId, 
                weixin_user_name: weixinUserName
            },
            success: function(data) {
                if (data != 'unknown_type') {
                    if (data) {
                        this.timelineContainer.append(data);
                        $('#screen').scrollTop(10000);
                    }
                }
            },
            error: function(resp) {
                xlog('call weixin_mp_user_temp_messages/get fail');
                xlog(resp);
            },
            scope: this
        });
    },

    /**
     * 向apiserver发送微信
     */
    sendMessageToApiServer: function(content, callback) {
        var weixinUserName = this.getWeixinUserName();
        var mpUserName = this.getWebappId();
        W.getApi().call({
            app: 'weixin',
            api: 'm/message_to_mp/create',
            args: {
                from_user_name: weixinUserName,
                to_user_name: mpUserName,
                content: content
            },
            success: function(data) {
                data.content = content;
                callback.call(this, data);
            },
            error: function(resp) {
                xlog(resp);
            },
            scope: this
        });
    },

    /**
     * 发送
     */
    sendMessageToViperWeb: function(data) {
        var weixinUserName = this.getWeixinUserName();
        var webappId = this.getWebappId();

        var task = new W.DelayedTask(function() {
            W.getApi().call({
                app: 'simulator',
                api: 'weixin/send',
                method: 'post',
                args: {
                    weixin_user_name: weixinUserName,
                    content: data.content,
                    webapp_id: webappId,
                    weixin_user_fakeid: "weizoom_default_fakeid"
                },
                success: function(data) {
                    if (data != 'unknown_type') {
                        this.timelineContainer.append(data);
                    }
                    $('#screen').scrollTop(10000);
                },
                error: function(resp) {
                    xlog(resp);
                },
                scope: this
            });
        }, this);
        task.delay(100);
    },

    /**
     * 发送微信
     */
    sendWeixin: function(content) {
        this.timelineContainer.append(this.customerTmpl.render({content:content}));
        this.timelineContainer.scrollTop(10000);
        this.$el.find('#weixinInput-contentInput').val('').focus();

        xlog('isInDevMode: ' + isInDevMode);
        if (isInDevMode) {
            this.sendMessageToApiServer(content, this.sendMessageToViperWeb);
        } else {
            this.sendMessageToViperWeb({
                content: content,
                fakeId: 'weizoom_default_fakeid'
            });
        }
        return false;
    },

    sendSubscribeEvent: function() {
        var task = new W.DelayedTask(function() {
            var webappId = this.getWebappId();
            var weixinUserName = this.getWeixinUserName();
            xlog('send subscribe event for ' + webappId + ' by ' + weixinUserName);
            W.getApi().call({
                app: 'simulator',
                api: 'mp_user/subscribe',
                method: 'post',
                args: {
                    webapp_id: webappId,
                    from_user: weixinUserName
                },
                success: function(data) {
                    if (data != 'unknown_type') {
                        this.timelineContainer.append(data);
                        $('#screen').scrollTop(10000);
                    }
                },
                scope: this
            })
        }, this);
        task.delay(100);
    },

    sendUnsubscribeEvent: function() {
        var task = new W.DelayedTask(function() {
            var webappId = this.getWebappId();
            xlog('send subscribe event for ' + webappId);
            W.getApi().call({
                app: 'simulator',
                api: 'mp_user/unsubscribe',
                method: 'post',
                args: {
                    webapp_id: webappId
                },
                success: function(data) {
                },
                scope: this
            })
        }, this);
        task.delay(100);
    },

    /**
     * 发送微信的响应函数
     */
    onSubmit: function(event) {
        var content = $.trim(this.$el.find('#weixinInput-contentInput').val());
        if (content.length == 0) {
            alert('请输入微信内容');
        } else {
            this.sendWeixin(content);
        }
        return false;
    },

    /**
     * 点击微信消息中链接的响应函数
     */
    onClickLink: function(event) {
        event.stopPropagation();
        event.preventDefault();
        var url = $(event.target).attr('href');
        this.openBrowser(url);
    },

    /**
     * 点击用户选择按钮后的响应函数
     */
    onSelectUser: function(event) {
        var weixinUserName = this.getWeixinUserName();
        var webappId = this.getWebappId();

        var weixinUserDisplayName = $('option[value="'+weixinUserName+'"]').text();
        var mpUserDisplayName = $('option[value="'+webappId+'"]').text();
        $('#top-weixin-title').html(weixinUserDisplayName + ' -> ' + mpUserDisplayName);

        $('#userSelect').hide();
        $('input[type="text"]').focus();
        $('#timeline-zone').addClass(weixinUserName+'-profile');
        this.sendSubscribeEvent();
    },

    /**
     * 微信消息内链接点击的响应函数
     */
    onClickMessageLink: function(event) {
        var link = $(event.currentTarget).attr('data-link');
        this.openBrowser(link);
    },

    /**
     * 点击左上角"微信"按钮的响应函数
     */
    onClickBackBtn: function(event) {
        this.closeBrowser();
    },

    /**
     * 点击右上角"取消关注"按钮的响应函数
     */
    onClickUnsubscribeBtn: function(event) {
        this.sendUnsubscribeEvent();
    },

    /**
     * 点击左下角"菜单"按钮的响应函数
     */
    onClickMenubarBtn: function(event) {
        this.$menubar.slideDown('fast');
    }
});