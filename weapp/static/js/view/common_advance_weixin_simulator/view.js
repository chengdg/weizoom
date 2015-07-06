/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信模拟器
 * @class
 */

ensureNS('W.view.common.advanceWeixinSimulator');

W.view.common.advanceWeixinSimulator.webappId = '3181';
W.view.common.advanceWeixinSimulator.displayWebappId = 'test1';
W.view.common.advanceWeixinSimulator.user = 'zhouxun';
W.view.common.advanceWeixinSimulator.displayUser = '周迅';
W.view.common.advanceWeixinSimulator.browserTarget = '';
W.view.common.advanceWeixinSimulator.browserRefer = '';
W.view.common.advanceWeixinSimulator.sharedImage = '';


/**
 * LoginPage: 登录页面
 */
W.view.common.advanceWeixinSimulator.LoginPage = Backbone.View.extend({
    events: {
        'click .x-loginBtn': 'onClickLoginBtn',
    },

    initialize: function(options) {
        this.$el = $(this.el);
        var _this = this;
        this.$el.on('pageshow', function() {
            W.getApi().call({
                app: 'simulator',
                api: 'sct_cookie/delete',
                args: {},
                success: function(data) {

                }
            })
        });
    },

    onClickLoginBtn: function(event) {
        // W.view.common.advanceWeixinSimulator.webappId = this.$('[name="webapp_id"]').val();
        // W.view.common.advanceWeixinSimulator.displayWebappId = this.$('[name="webapp_id"] option:checked').text();
        W.view.common.advanceWeixinSimulator.user = this.$('[name="user"]').val();
        W.view.common.advanceWeixinSimulator.displayUser = this.$('[name="user"] option:checked').text();
    }

});





W.view.common.advanceWeixinSimulator.AccountListPage = Backbone.View.extend({
    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);

        var _this = this;
        this.$el.on('pagebeforeshow', function() {
            _this.$('.ui-footer [data-icon="home"]').addClass('ui-btn-active');
        });
        this.$el.on('pageshow', function() {
            _this.$('[data-role="header"] h1').text(W.view.common.advanceWeixinSimulator.displayUser + '的微信');
            /*
            _this.$('.x-mpUser').text(W.view.common.advanceWeixinSimulator.webappId);
            _this.$('.x-mpUserInfo').text('欢迎访问' + W.view.common.advanceWeixinSimulator.displayWebappId);
            */
        });
        this.$el.delegate('li', 'click', function(event) {
            var $li = $(event.currentTarget);
            var webappId = $li.attr('data-webapp-id');
            var mpUserName = $li.attr('data-mp-user-name');
            W.view.common.advanceWeixinSimulator.webappId = webappId;
            W.view.common.advanceWeixinSimulator.displayWebappId = webappId;
            W.view.common.advanceWeixinSimulator.mpUserName = mpUserName;
        });
    }
});





W.view.common.advanceWeixinSimulator.DiscoverPage = Backbone.View.extend({
    events: {
    },

    initialize: function(options) {
        this.$el = $(this.el);

        var _this = this;
        this.$el.on('pagebeforeshow', function() {
            _this.$('[data-icon="search"]').addClass('ui-btn-active');
        });
    }
});





W.view.common.advanceWeixinSimulator.FriendPage = Backbone.View.extend({
    events: {
        'click a.oneSharedMessage_link': 'onClickLink'
    },

    getTemplate: function() {
        $('#advance-weixin-simulator-one-shared-message-tmpl-src').template('advance-weixin-simulator-one-shared-message-tmpl');

        return 'advance-weixin-simulator-one-shared-message-tmpl'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        this.template = this.getTemplate();

        var _this = this;
        this.$el.on('pagebeforeshow', function() {
            var logoImgUrl = '/standard_static/img/simulator/friend_logo_' + W.view.common.advanceWeixinSimulator.user + '.jpg';
            var headImgUrl = '/standard_static/img/simulator/' + W.view.common.advanceWeixinSimulator.user + '.jpg';
            _this.$('#friendPageLogo').attr('src', logoImgUrl);
            _this.$('#myHeadImg').attr('src', headImgUrl);
        });
        this.$el.on('pageshow', function() {
            _this.load();
        })
    },

    onClickLink: function(event) {
        var $link = $(event.currentTarget);
        W.view.common.advanceWeixinSimulator.browserTarget = $link.attr('data-href');
    },

    /**
     * load: 加载朋友圈消息
     */
    load: function() {
        W.getApi().call({
            app: 'simulator',
            api: 'shared_messages/get',
            args: {
                user: W.view.common.advanceWeixinSimulator.user
            },
            scope: this,
            success: function(data) {
                var $node = $.tmpl(this.template, data);
                this.$('#friendSharedMessageList').empty().append($node);
            },
            error: function(resp) {
                alert('加载朋友圈失败!');
            }
        })
    }
});





W.view.common.advanceWeixinSimulator.BrowserPage = Backbone.View.extend({
    events: {
        'click #browserPage-backBtn': 'onClickBackButton',
        'click #browserPage-shareBtn': 'onClickShareButton'
    },

    initialize: function(options) {
        this.$el = $(this.el);

        var _this = this;
        var $browser = this.$('#mobile-browser');
        this.$el.on('pagebeforeshow', function() {
            var $window = $(window);
            $browser.height($window.outerHeight() + 'px');
        });

        this.$el.on('pageshow', function() {
            $browser.attr('src', W.view.common.advanceWeixinSimulator.browserTarget);
        });

        this.$el.on('pagehide', function() {
            $browser.attr('src', '/loading/');
        });
    },

    onClickBackButton: function(event) {
        var target = '#friendPage';
        if (W.view.common.advanceWeixinSimulator.browserRefer) {
            var target = W.view.common.advanceWeixinSimulator.browserRefer;
        }

        $.mobile.changePage($(target), {
            transition: 'slide',
            reverse: true
        });
    },

    onClickShareButton: function(event) {
        //获取最新的location
        W.view.common.advanceWeixinSimulator.browserTarget = $('#mobile-browser').get(0).contentWindow.location.href

        var $img = this.$('iframe').contents().find('img').eq(0);
        if ($img.length > 0) {
            W.view.common.advanceWeixinSimulator.sharedImage = $img.attr('src');
        }

        $.mobile.changePage($('#sharePage'), {
            transition: 'slide'
        });      
    }
});





W.view.common.advanceWeixinSimulator.SharePage = Backbone.View.extend({
    events: {
        'click #sendBtn': 'onClickSendButton'
    },

    initialize: function(options) {
        this.$el = $(this.el);
        
        var _this = this;
        this.$el.on('pagebeforeshow', function() {
            var now = new Date();
            var message = now.toLocaleDateString() + ' ' + now.toLocaleTimeString() + '的心情';
            _this.$('[name="message"]').val(message);
            _this.$('[name="link_title"]').val('[请阅读我...]');
        });
    },

    onClickSendButton: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var message = this.$('[name="message"]').val();
        var linkTitle = this.$('[name="link_title"]').val();
        var linkUrl = W.view.common.advanceWeixinSimulator.browserTarget;
        var linkImg = W.view.common.advanceWeixinSimulator.sharedImage;
        $.mobile.loading( 'show', {
            text: '分享页面...',
            textVisible: true,
            theme: 'z',
            html: ""
        });

        this.share(message, linkTitle, linkUrl, linkImg);
        W.view.common.advanceWeixinSimulator.sharedImage = '';
    },

    /**
     * load: 加载朋友圈消息
     */
    share: function(message, linkTitle, linkUrl, linkImg) {
        W.getApi().call({
            app: 'simulator',
            api: 'webapp_page/share',
            method: 'post',
            args: {
                user: W.view.common.advanceWeixinSimulator.user,
                message: message,
                link_title: linkTitle,
                link_url: linkUrl,
                link_img: linkImg
            },
            scope: this,
            success: function(data) {
                $.mobile.loading('hide');
                $.mobile.changePage($('#friendPage'), {
                    transition: 'slide',
                    reverse: true
                });
            },
            error: function(resp) {
                $.mobile.loading('hide');
                alert('分享页面失败!');
            }
        });
    }
});




W.view.common.advanceWeixinSimulator.MessagePage = Backbone.View.extend({
    events: {
        'submit #messagePage-editPanel': 'onSubmit',
        'click div.wx-message-link': 'onClickMessageLink',
        'click #screen a': 'onClickLink',
        'click #messagePage-editPanel-menubarTrigger': 'onClickMenubarTrigger',
    },

    initialize: function(options) {
        this.$el = $(this.el);

        this.customerTmpl = new W.Template(
                                '<div class="mt20 customer">'+
                                    '<div class="profile customer-profile"><img src="/static/img/weixin-customer.jpg" width="45"/></div>'+
                                    '<div class="content">${content}</div>'+
                                    '<div class="cb"></div>'+
                                '</div>');
        
        var _this = this;
        this.$el.on('pagebeforeshow', function() {
        });
        this.$el.on('pageshow', function() {
            W.getApi().call({
                app: 'webapp',
                api: 'homepage_info/get',
                args: {
                    'webapp_owner_name': W.view.common.advanceWeixinSimulator.mpUserName
                },
                success: function(data) {
                    _this.$('.xa-homepageLink').attr('href', '/workbench/jqm/preview/?project_id='+data['project_id']+'&woid='+data['webapp_owner_id'])
                }
            })
            _this.$('[data-role="header"] h1').text(W.view.common.advanceWeixinSimulator.mpUserName + '的公众号');
            if (_this.hasMessage()) {
                _this.scrollScreen();
            } else {
                _this.sendSubscribeEvent();
            }
            _this.$('input[type="text"]').eq(0).focus();
            //创建menubar
            _this.createMenubar();
        });

        this.$timelineContainer = this.$('#timeline-zone');
        this.$editPanel = this.$('#messagePage-editPanel');
        this.$window = $(window);
    },

    /**
     * scrollScreen: 滚动屏幕
     */
    scrollScreen: function() {
        var height = this.$window.outerHeight();
        var timelinesHeight = this.$timelineContainer.outerHeight();
        if (timelinesHeight + 100 > height) {
            this.$window.scrollTop(10000);
        }
    },

    createMenubar: function() {
        this.$menubar = this.$('#menubar-zone');
        this.menubar = new W.view.weixin.EmbededPhoneMenuBar({
            el: this.$menubar,
            mode: 'action'
        });
        this.menubar.bind('click-menubar-edit-button', function() {
            var _this = this;
            this.$menubar.slideUp('fast', function() {
                _this.$editPanel.show();
            });
        }, this)
        this.menubar.bind('click-menu', function(menuId) {
            xlog('[phone]: click menu ' + menuId);
            var content = 'MENU_QUERY_' + menuId;
            var weixinUserName = W.view.common.advanceWeixinSimulator.user;
            var webappId = W.view.common.advanceWeixinSimulator.webappId;
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
                        this.$timelineContainer.append(data);
                    }
                    this.scrollScreen();
                },
                error: function(resp) {
                    xlog(resp);
                },
                scope: this
            });
        }, this);

        //加载菜单数据
        W.getApi().call({
            app: 'weixin/manage/customized_menu',
            api: 'menus/get',
            args: {
                webapp_id: W.view.common.advanceWeixinSimulator.webappId
            },
            scope: this,
            success: function(menus) {
                this.menubar.addMenus(menus);
            },
            error: function(resp) {
                alert('加载菜单数据失败!');
            }
        });
    },

    hasMessage: function() {
        return this.$timelineContainer.find('div.content').length > 0;
    },

    /**
     * 发送
     */
    sendMessageToWeb: function(data) {
        var task = new W.DelayedTask(function() {
            W.getApi().call({
                app: 'simulator',
                api: 'weixin/send',
                method: 'post',
                args: {
                    weixin_user_name: W.view.common.advanceWeixinSimulator.user + '_' + W.view.common.advanceWeixinSimulator.mpUserName,
                    content: data.content,
                    webapp_id: W.view.common.advanceWeixinSimulator.webappId,
                    weixin_user_fakeid: data.fakeId
                },
                success: function(data) {
                    if (data != 'unknown_type') {
                        this.$timelineContainer.append(data);
                        this.scrollScreen();
                    }
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
     * sendWeixin: 发送微信消息
     */
    sendWeixin: function(content) {
        this.$timelineContainer.append(this.customerTmpl.render({content:content}));
        this.scrollScreen();

        this.sendMessageToWeb({
            content: content,
            fakeId: 'weizoom_default_fakeid'
        });
        return false;
    },

    /**
     * getSctCookie: 获取sct cookie
     */
    getSctCookie: function() {
        var webappId = W.view.common.advanceWeixinSimulator.webappId;
        var openid = W.view.common.advanceWeixinSimulator.user;
        var mpUserName = W.view.common.advanceWeixinSimulator.mpUserName;
        W.getApi().call({
            app: 'simulator',
            api: 'sct_cookie_url/get',
            args: {
                webapp_id: webappId,
                openid: openid + '_' + mpUserName
            },
            success: function(data) {
                var _this = this;
                $.get(data.url, function(data) {
                    _this.$('[data-role="header"] h1').html(W.view.common.advanceWeixinSimulator.mpUserName + '的公众号(<span style="color: red">会员'+openid+'</span>)');
                })
            },
            scope: this
        })
    },

    /**
     * sendSubscribeEvent: 发送subscribe事件
     */
    sendSubscribeEvent: function() {
        var task = new W.DelayedTask(function() {
            var webappId = W.view.common.advanceWeixinSimulator.webappId;
            var weixinUserName = W.view.common.advanceWeixinSimulator.user;
            var mpUserName = W.view.common.advanceWeixinSimulator.mpUserName;
            xlog('send subscribe event for ' + webappId + ' by ' + weixinUserName);
            W.getApi().call({
                app: 'simulator',
                api: 'mp_user/subscribe',
                method: 'post',
                args: {
                    webapp_id: webappId,
                    from_user: weixinUserName + '_' + mpUserName
                },
                success: function(data) {
                    if (data != 'unknown_type') {
                        this.$timelineContainer.append(data);
                        this.scrollScreen();
                    }
                    this.getSctCookie();
                },
                scope: this
            })
        }, this);
        task.delay(100);
    },

    onSubmit: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $messageEl = this.$('[name="messageInput"]');
        var message = $.trim($messageEl.val());
        if (message.length == 0) {
            //do nothing
        } else {
            this.sendWeixin(message);
            $messageEl.val('').focus();
        }
    },


    /**
     * onClickMessageLink: 微信消息内链接点击的响应函数
     */
    onClickMessageLink: function(event) {
        var link = $(event.currentTarget).attr('data-link');
        W.view.common.advanceWeixinSimulator.browserTarget = link;
        W.view.common.advanceWeixinSimulator.browserRefer = '#messagePage';
        $.mobile.changePage($('#browserPage'), {
            transition: 'slide'
        });
    },

    /**
     * onClickMenubarTrigger: 点击menubar trigger的响应函数
     */
    onClickMenubarTrigger: function(event) {
        this.$editPanel.hide();
        this.$menubar.slideDown('fast');
    }
});
