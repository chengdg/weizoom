/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 微信消息编辑器
 * @class
 */

ensureNS('W.view.weixin');
W.view.weixin.MaterialListView = Backbone.View.extend({
	el: '',

	events: {
		'click .x-embededPhone-deleteBtn': 'onDeleteNews',
	    'click .x-embededPhone-editBtn': 'onUpdateNews',
	    'mouseover .x-oneMaterial': 'onMouseEnterMaterial',
	    'mouseout .x-oneMaterial': 'onMouseLeaveMaterial'
	},

	getTemplate: function() {
        $('#weixin-material-list-tmpl-src').template('weixin-material-list-tmpl');
        return 'weixin-material-list-tmpl';
    },

    compileNewsTemplate: function() {
        $('#single-news-tmpl-src').template('single-news-tmpl');
        $('#multi-newses-tmpl-src').template('multi-newses-tmpl');
    },

	initialize: function(options) {
		this.$el = $(this.el);
		this.enableEdit = options.enableEdit || false;

		this.template = this.getTemplate();
		this.compileNewsTemplate();
		
		this.newses = new W.model.weixin.material.Newses();
		this.newses.page = options.page || 0;
		this.currentMaterialIndex = 0;
    },

	render: function() {
        xlog('begin 1')
		this.$el.html($.tmpl(this.template, {
		}));
        xlog('finish 1')

		this.$leftMaterialContainer = this.$('.leftList').eq(0);
		this.$rightMaterialContainer = this.$('.rightList').eq(0);

		this.fetchData();
		return this;
	},

	/**
	 * addOneMaterial: 添加一个material
	 */
	addOneMaterial: function(material) {
	    this.currentMaterialIndex++;
        var materialJSON = material.toJSON();
        var newses = materialJSON.newses;
        if (newses.length == 1) {
            xlog('begin 2');
            var newsNode = $.tmpl('single-news-tmpl', {
                news: newses[0],
	            enableEdit: this.enableEdit,
	            enableUpdateMaterial: true,
	            enableDeleteMaterial: true
            }).removeClass('mt10');
            xlog('finish 2');
        } else {
            var mainNews = newses[0];
            var subNewses = newses.slice(1);
            xlog('begin 3');
            var newsNode = $.tmpl('multi-newses-tmpl', {
                mainNews: mainNews,
                subNewses: subNewses,
	            enableEdit: this.enableEdit,
	            enableUpdateMaterial: true,
	            enableDeleteMaterial: true
            }).removeClass('mt10');
            xlog('end 3');
        }
        var phoneNode = $('<div id="small-phone" class="small-phone-nobackground x-oneMaterial" data-can-select="true" data-id="'+material.get('id')+'"></div>')
        phoneNode.append(newsNode);

	    if(this.currentMaterialIndex % 2 === 0) {
		    this.$rightMaterialContainer.append(phoneNode);
	    }else {
		    this.$leftMaterialContainer.append(phoneNode);
	    }
	    //隐藏编辑和删除按钮
	    //$('div.edit-div input').hide();
    },

	/**
	 * fetchData: 从数据库获取news集合
	 */
	fetchData: function() {
		var _this = this;
		this.newses.fetch({
            reset: false,
            success: function(newses, response) {
            	if (newses.length === 0) {
            		_this.$('#weixinMaterialList-hint').text('目前没有素材，请创建！')
            	} else {
		            newses.each(function(news) {
		            	_this.addOneMaterial(news);
	    	        });
	    	        _this.$('#weixinMaterialList-hint').hide();
	        	    _this.$('#weixinMaterialList-materials').show();
	        	}
	        	_this.trigger('fetchDataAfter', response);
	        	if (response.data.pageinfo) {
	        		_this.page_has_next = response.data.pageinfo.has_next || false;
	        	} 
	            /*
                _this.paginationView.setPageInfo(_this.newses.getPageData(response));
                _this.paginationView.show();
                */
            },
            error: function(newses, response) {
                //var msg = response.errMsg || '由于网络原因，加载失败，请重新刷新页面!';
                //alert(msg)
                if (response.errMsg) {
                    alert(response.errMsg);
                }
            }
        });
	},

	/**
	 * clear: 清空现存的news集合
	 */
	clear: function(){
        this.newses.reset([])
        this.$el.find('li').remove();
    },

    /**
     * onMouseEnterOverMaterial: 鼠标移动到material上的响应函数
     */
    onMouseEnterMaterial: function(event) {
    	var $el = $(event.currentTarget);
		$el.find('div.edit-div input').show();
    },

    /**
     * onMouseLeaveMaterial: 鼠标移出material时的响应函数
     */
    onMouseLeaveMaterial: function(event) {
    	var $el = $(event.currentTarget);
		$el.find('div.edit-div input').hide();
    },

    /**
     * onDeleteNews: 点击material的“删除”按钮的响应函数
     */
    onDeleteNews: function(event) {
        var $el = $(event.target);
        var _this = this;
    	W.view.fn.requreConfirm({
            $el: $el,
            confirm: function() {
                var $div = $el.parents('.x-oneMaterial');
                var newsId = $div.attr('data-id');

                W.getApi().call({
                    app: 'weixin/message/material',
                    api: 'news/delete',
                    args: {
                        id: newsId
                    },
                    success: function(data) {
                        //改变日历中，已有信息
                        _this.trigger('finish-delete-news');
                        W.view.fn.finishConfirm();
                    },
                    error: function(resp) {

                    },
                    scope: _this
                });
            }
        })
    },

    /**
     * onUpdateNews: 点击material的“删除”按钮的响应函数
     */
    onUpdateNews: function(event) {
    	event.stopPropagation();
        event.preventDefault();

        var $div = $(event.target).parents('.x-oneMaterial');
        var newsId = $div.attr('data-id');
        this.trigger('update-news', newsId);
    }
});