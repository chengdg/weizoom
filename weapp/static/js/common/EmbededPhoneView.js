/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 用于嵌入到页面中的微信模拟器
 * @class
 */
W.common.EmbededPhoneView = Backbone.View.extend({
	el: '#small-phone',

	events: {
        'mouseenter .wx-news-container': 'onShowActionBar',
		'mouseleave .wx-news-container': 'onHideActionBar',
		'click div.wx-action-bar': 'onSelectNews',
		'click #create-news-btn': 'onCreateNews',
        'click #back-weixin-btn': 'onClickBackBtn',
        'click #screen a': 'onClickLink'
	},

    compileTemplate: function() {
        $('#small-phone-tmpl-src').template('small-phone-tmpl');
        $('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
        $('#text-message-tmpl-src').template('text-message-tmpl');
    },
	
	initialize: function(options) {
		this.$el = $(this.el);

        this.messages = new W.common.Messages();//options.messages || [];
        this.messages.bind('change', _.bind(this.onChangeMessage, this));
        this.messages.bind('creat-model-from-cache', function() {
            this.onCreateNews();
        }, this);
        this.messages.bind('delete-model-from-cache', function(model) {
            this.deleteNews(model);
            this.selectNewsByIndex(0);
        }, this);        
        
        this.id2message = {};
        this.id2element = {};

		this.mode = options.mode || "weixin";
        this.onBeforeChangeNews = options.onBeforeChangeNews;
        this.onBeforeCreateNews = options.onBeforeCreateNews;
		this.shopName = options.shopName || "";
        this.initBrowserUrl = options.initBrowserUrl || '/m/shop/'+this.shopName+'/?embed=1';

        this.deleteIds = [];

		if (this.mode == "weixin") {
			this.reset(this.messages);
            this.enableWeixin = true;
            this.enableBrowser = true;
            this.initBrowserUrl = '/loading/';
		} else if (this.mode == 'webapp') {
			xlog('enter webapp mode');
            this.enableWeixin = false;
            this.enableBrowser = true;
            if (options.initBrowserUrl) {
                this.initBrowserUrl = options.initBrowserUrl;
            }
		} else {
            this.enableWeixin = true;
            this.enableBrowser = true;
        }

		this.enableAction = options.enableAction || false;
		this.container = null;
        this.enableAddNews = options.enableAddNews || false;

		this.isBrowserVisible = false;
        this.autoRefreshEnabled = true;

        this.messageIndex = 0; //用于计算message序号，对于多图文消息，我们会将多条message视为一条message

        this.compileTemplate();
	},

    /**
     * 禁止自动refresh
     */
    disableRefresh: function() {
        this.autoRefreshEnabled = false;
    },

    /**
     * 开启自动refresh
     */
    enableRefresh: function() {
        this.autoRefreshEnabled = true;   
    },

    /**
     * 获取一个新的message index
     */
    getNewMessageIndex: function() {
        this.messageIndex += 1;
        return this.messageIndex;
    },

    getMessageIndex: function() {
        return this.messageIndex;
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

    refreshBrowser: function(link) {
        xlog('refresh browser');

        var browser = $('#mobile-browser');
        if (!link) {
            link = browser.attr('src');
        }
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
		return _.filter(this.messages.toJSON(), function(message) {
//			return message.type == 'news' && message.id < 0;
            return message.type == 'news';
		}, this);
	},

    /**
     * 获得删除的id集合
     * @return {*}
     */
    getDeletedNewsIds: function() {
        return this.deleteIds.join(',')
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
            title: W.previewName,
            initBrowserUrl: this.initBrowserUrl
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

        //merge messages, change message model to message  JSON
        var mergedMessages = [];
        var curMessageIndex = -1;
        var count = this.messages.length;
        var tempMessages = [];
        for (var i = 0; i < count; ++i) {
            var message = this.messages.at(i);
            var messageIndex = message.get('metadata').messageIndex;
            if (messageIndex != curMessageIndex) {
                curMessageIndex = messageIndex;
                if (tempMessages.length != 0) {
                    mergedMessages.push(tempMessages);
                    tempMessages = [];
                }
            }

            tempMessages.push(message.toJSON());
        }
        if (tempMessages.length != 0) {
            mergedMessages.push(tempMessages); //处理最后一条消息
        }

        //render messages
        var count = mergedMessages.length;
        for (var i = 0; i < count; ++i) {
            var messages = mergedMessages[i];
            if (messages.length == 1) {
                var message = messages[0];
                //text or single_news
                if (message.type == 'text') {
                    this.container.append($.tmpl('text-message-tmpl', {
                        extraClass: message.metadata.direction == 'send' ? 'shop-service' : 'customer',
                        texts: message.text.split('\n'),
                        imagePath: message.pic_url,
                        id: message.id
                    }));
                } else {
                    this.container.append($.tmpl('single-news-tmpl', {
                        news: message,
                        enableAddNews: this.enableAddNews
                    }));
                }
            } else {
                //multi_news
                var mainNews = messages[0];
                var subNewses = messages.slice(1);
	            this.enableAddNews = (subNewses.length == 9 ? false : true);
                this.container.append($.tmpl('multi-newses-tmpl', {
                    mainNews: mainNews,
                    subNewses: subNewses,
                    enableAddNews: this.enableAddNews
                }));
            }
        }
        
        //cache message's DOM element
        this.messages.each(function(message) {
            message.element = null;
            var selector = 'div[data-id="'+message.id+'"]';
            message.element = this.$(selector);
        });
	},

	/**
	 * 添加一条新建的news message
	 * @param news
	 */
	addNews: function(news) {
        var message = news;
        var metadata = message.get('metadata');
        metadata.messageIndex = this.getNewMessageIndex();
		this.messages.push(message);
        this.refresh();

        if (message.get('metadata') && message.get('metadata').autoSelect) {
            this.selectNews(message.id);
        }
	},

    /**
     * 向最后一条message中附加一条额外的message
     */
    appendNews: function(news) {        
        var message = news;
        var metadata = message.get('metadata');
        metadata.messageIndex = this.getMessageIndex();

        this.messages.push(message);
        this.refresh();

        this.selectNews(message.id);
    },

    /**
     * 添加一组新建的news message
     */
    addNewses: function(messages) {
        this.messages.add(messages);
        this.refresh();

        var count = this.messages.length;
        for (var i = 0; i < count; ++i) {
            var message = this.messages.at(i);
            var metadata = message.get('metadata');
            if (0 == i) {
                metadata.messageIndex = this.getNewMessageIndex();
            } else {
                metadata.messageIndex = this.getMessageIndex();
            }
            if (message.get('metadata') && message.get('metadata').autoSelect) {
                this.selectNews(message.id);
            }
        }
    },

	deleteNews: function(news) {
        this.messages.remove(news);
        if(news.id > 0){
            this.deleteIds.push(news.id);
        }
		this.refresh();
	},

    checkNews: function() {
        xlog('check newses...');
        if (this.messages.length == 0) {
            this.trigger('start-create-news');
        }
    },

    /**
     * 添加一条“发送”方向的文本消息
     */
    addTextMessage: function(message) {
        var metadata = message.get('metadata');
        metadata.direction = 'send';
        metadata.messageIndex = this.getNewMessageIndex();
        message.set('pic_url', W.previewImage);
        this.messages.push(message);
        this.refresh();
    },

    /**
     * 收到一条文本消息
     * @param text
     */
    receiveTextMessage: function(message, options) {
        var metadata = message.get('metadata');
        metadata.direction = 'receive';
        metadata.messageIndex = this.getNewMessageIndex();
        message.set('pic_url', '/static/img/weixin-customer.jpg');
        this.messages.push(message);
        if (options && options.silent) {
            // silent, do nothing
        } else {
            this.refresh();
        }
    },

    /**
     * 选择一条news
     */
    selectNews: function(id) {
        if (this.enableAction) {
            var message = this.messages.get(id);
            var newsEl = message.element;
            $('div.wx-action-bar').attr('data-pin', 'false').hide();
            
            var actionBar = newsEl.find('div.wx-action-bar');
            actionBar.attr('data-pin', 'true');
            actionBar.show();

            this.trigger('select-news', message, this.messages.length);
        }
    },

    /**
     * 根据index选择一条
     */
    selectNewsByIndex: function(index) {
        var message = this.messages.at(index);
        if (message) {
            this.selectNews(message.id);
        }
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
     * 点击左上角"微信"按钮的响应函数
     */
    onClickBackBtn: function(event) {
        this.closeBrowser();
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
        if (this.onBeforeChangeNews) {
            if (!this.onBeforeChangeNews()) {
                return;
            }
        }
    
        var newsEl = $(event.target).parents('div.wx-news-container');
        var id = newsEl.attr('data-id');
        this.selectNews(parseInt(id));
	},

    onChangeMessage: function(message) {
        _.each(message.changed, function(value, key) {
            // value = value == null ? '' : value
            // if (!value.hasOwnProperty('replace')){
            //     value = '';
            // }
            
            if (message.get('type') == 'text') {
                var selector = 'div.content';
                message.element.find(selector).html(value.replace(/\n/g, "<br />"));
            } else {
                if (key === 'pic_url') {
                    var selector = 'img[name="picture"]';
                    if (value.length == 0) {
                        value = '/static/img/empty_image.png';
                    }
                    message.element.find(selector).attr('src', value);
                } else {
                    var selector = 'span[name="'+key+'"]';
                    message.element.find(selector).html(value.replace(/\n/g, "<br />"));
                }
            }
        });
    },

	/**
	 * 添加图文消息的区域的点击事件的响应函数
	 * @param event
	 */
	onCreateNews: function(event) {
        if (this.onBeforeCreateNews) {
            if (!this.onBeforeCreateNews()) {
                return;
            }
        }
        this.trigger('start-create-news');
	},

	/**
	 * 重置message集合
	 */
	reset: function(messages) {
        if (messages) {
    		this.messages = messages;
        } else {
            this.messages = new W.common.Messages();;
        }
        _.each(this.messages.models, function(message) {
            this.id2message[message.id] = message;
        }, this);
        this.refresh();
	}
});