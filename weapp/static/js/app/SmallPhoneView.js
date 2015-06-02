/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 小尺寸的微信模拟器
 * @class
 */
$('#small-phone-tmpl-src').template('small-phone-tmpl');
$('#single-news-tmpl-src').template('single-news-tmpl');
$('#multi-newses-tmpl-src').template('multi-newses-tmpl');
$('#text-message-tmpl-src').template('text-message-tmpl');

W.SmallPhoneView = Backbone.View.extend({
	el: '#small-phone',

	events: {
        'mouseenter .wx-news-container': 'onShowActionBar',
		'mouseleave .wx-news-container': 'onHideActionBar',
		'click div.wx-action-bar': 'onSelectNews',
		'click #create-news-btn': 'onCreateNews'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.messageId = 1;
        this.id = -100;

        this.messages = options.messages || [];
        this.id2message = {};

		this.mode = options.mode || "weixin";
		this.shopName = options.shopName || "";

		if (this.mode == "weixin") {
			this.reset(this.messages);
            this.enableWeixin = true;
            this.enableBrowser = false;
		} else if (this.mode == 'webapp') {
			xlog('enter webapp mode');
            this.enableWeixin = false;
            this.enableBrowser = true;
		} else {
            this.enableWeixin = true;
            this.enableBrowser = true;
        }

		this.enableAction = options.enableAction || false;
		this.container = null;
        this.enableAddNews = options.enableAddNews || false;

		this.isBrowserVisible = false;
	},

    openBrowser: function(link) {
        if (link) {
            $('#mobile-browser').attr('src', link);
        }
        $('#timeline-zone').hide();
        $('#browser-zone').animate({
            left: '0'
        }, 400);
	    this.isBrowserVisible = true;
    },

    refreshBrowser: function() {
        xlog('refresh browser');

        var browser = $('#mobile-browser');
        var link = browser.attr('src');
        browser.attr('src', '/loading/');

        var task = new W.DelayedTask(function() {
            browser.attr('src', link);
        });
        task.delay(300);
    },

    closeBrowser: function() {
        $('#browser-zone').animate({
            left: '100%'
        }, 400);
        $('#timeline-zone').show();
	    this.isBrowserVisible = false;
    },

	isViewWebapp: function() {
		return this.isBrowserVisible;
	},

    /**
     * 获得一个未用过的message id
     * @return {Number}
     */
    getMessageId: function() {
        var id = this.messageId;
        this.messageId += 1;
        return id;
    },

    /**
     * 获得一个未用过的id
     * @return {*}
     */
    getId: function() {
        var id = this.id;
        this.id -= 1;
        return id;
    },

	/**
	 * 判断是否有新创建的news
	 */
	hasNewCreatedNews: function() {
        var count = this.messages.length;
        for (var i = 0; i < count; ++i) {
            var message = this.messages[i];
            if (message.type == 'news' && message.id < 0) {
                return true;
            }
        }

        return false;
	},

	/**
	 * 获得新增news
	 * @return {*}
	 */
	getNewCreatedNewses: function() {
		return _.filter(this.messages, function(message) {
			return message.type == 'news' && message.id < 0;
		}, this);
	},

    /**
     * 渲染html结果
     */
	render: function() {
        //创建html
        this.$el.html($.tmpl('small-phone-tmpl', {
            enableWeixin: this.enableWeixin,
            enableBrowser: this.enableBrowser,
            shopName: this.shopName,
            title: W.previewName
        }));
        this.container = this.$el.find('#timeline-zone');
        this.refresh();
	},

	/**
	 * 重新绘制消息区域
	 */
	refresh: function() {
        if (!this.container) {
            //DOM还没有准备好，返回
		    return;
        }

        this.container.html('');
		if (this.messages.length == 0) {
			return;
		}

        //组合
        var messages = [];
        var count = this.messages.length;
        var currentMessageId = -1;
        for (var i = 0; i < count; ++i) {
            var message = this.messages[i];
            if (message.type == 'text') {
                messages.push(message);
            } else {
                if (message.messageId != currentMessageId) {
                    messages.push([]);
                    currentMessageId = message.messageId;
                }

                var newses = messages[messages.length-1];
                newses.push(message);
            }
        }

        count = messages.length;
        for (i = 0; i < count; ++i) {
            message = messages[i];
            if (message.type == 'text') {
                this.container.append($.tmpl('text-message-tmpl', {
                    extraClass: message.direction == 'send' ? 'shop-service' : 'customer',
                    texts: message.text.split('\n'),
                    imagePath: message.direction == 'receive' ? '/static/img/robert_50.png' : W.previewImage
                }));
            } else {
                newses = message;
                if (newses.length == 1) {
                    this.container.append($.tmpl('single-news-tmpl', {
                        news: newses[0],
                        enableAddNews: this.enableAddNews
                    }));
                } else {
                    var mainNews = newses[0];
                    var subNewses = newses.slice(1);
                    this.container.append($.tmpl('multi-newses-tmpl', {
                        mainNews: mainNews,
                        subNewses: subNewses,
                        enableAddNews: this.enableAddNews
                    }));
                }
            }
        }
	},

	/**
	 * 添加一条新建的news message
	 * @param news
	 */
	addNews: function(news) {
        var message = news;
        message.type = 'news';
        message.messageId = this.getMessageId();
        if (!message.id) {
            message.id = this.getId();
        }
		this.messages.push(message);
		this.id2message[message.id] = message;
		this.refresh();
	},

    /**
     * 为最后一条message添加一条news
     * @param news
     */
    appendNews: function(news) {
        if (this.messages.length == 0) {
            //没有消息，转换成addNews行为
            this.addNews(news);
        } else {
            var lastMessage = this.messages[this.messages.length-1];

            var message = news;
            message.type = 'news';
            message.messageId = lastMessage.messageId;
            if (!message.id) {
                message.id = this.getId();
            }
            this.messages.push(message);
            this.id2message[message.id] = message;
            this.refresh();
        }
    },

	/**
	 * 更新一条news的信息
	 * @param news
	 */
	updateNews: function(news) {
		this.refresh();
	},

	deleteNews: function(news) {
        this.messages = _.filter(this.messages, function(message) {
            return message.id != news.id;
        });
		this.refresh();
	},

    checkNews: function() {
        xlog('check newses...');
        if (this.messages.length == 0) {
            this.trigger('start-create-news');
        }
    },

    addText: function(textMessage) {
        if (textMessage.text.length == 0) {
            return;
        }

        var message = textMessage;
        message.type = 'text';
        message.direction = 'send';
        message.messageId = this.getMessageId();
        if (!message.id) {
            message.id = this.getId();
        }
        this.messages.push(message);
        this.id2message[message.id] = message;
        this.refresh();
    },

    /**
     * 收到一条文本消息
     * @param text
     */
    receiveText: function(text, options) {
        var message = {
            text: text,
            type: 'text',
            direction: 'receive',
            messageId: this.getMessageId(),
            id: 0
        }
        this.messages.push(message);
        this.id2message[message.id] = message;
        if (options && options.silent) {
            this.refresh();
        }
    },

	onShowActionBar: function(event) {
        if (this.enableAction) {
    		var news = $(event.currentTarget);
    	   	var actionBar = news.find('div.wx-action-bar');
    		if ('false' == actionBar.attr('data-pin')) {
    			actionBar.show();
    		}
        }
	},

	onHideActionBar: function(event) {
        if (this.enableAction) {
    		var news = $(event.currentTarget);
    		var actionBar = news.find('div.wx-action-bar');
    		if ('false' == actionBar.attr('data-pin')) {
    			actionBar.hide();
    		}
        }
	},

	onSelectNews: function(event) {
        if (this.enableAction) {
    		$('div.wx-action-bar').attr('data-pin', 'false').hide();

    		var actionBar = $(event.currentTarget);

    		actionBar.attr('data-pin', 'true');
    		actionBar.show();
    		var newsEl = $(event.target).parents('div.wx-news-container');
    		var id = newsEl.attr('data-id');
            var news = this.id2message[id];
    		this.trigger('select-news', news);
        }
	},

	/**
	 * 添加图文消息的区域的点击事件的响应函数
	 * @param event
	 */
	onCreateNews: function(event) {
		$('div.wx-action-bar').attr('data-pin', 'false').hide(); //取消所有action bar
		this.trigger('start-create-news');
	},

	/**
	 * 重置message集合
	 */
	reset: function(messages) {
        if (messages) {
    		this.messages = messages;
        } else {
            this.messages = [];
        }
        _.each(this.messages, function(message) {
            this.id2message[message.id] = message;
        }, this);
        this.refresh();
	}
});