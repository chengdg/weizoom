/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 微站内部链接
 * @class
 */
ensureNS('W.view.weixin')
W.view.weixin.MenuLinkView = W.view.common.SelectWebSiteLinkView.extend({
	
	getTemplate: function() {
        $('#weixin-menu-link-tmpl-src').template('weixin-menu-dropdown-link-tmpl');
        return 'weixin-menu-dropdown-link-tmpl';
    },
	
	initialize: function(options) {
		this.$el = $(this.el);    
        var _this = this;
        W.getApi().call({
            app: 'webapp',
            api: 'tools/get',
            // scope: this,
            success: function(data) {
                _this.$el.append($.tmpl(_this.getTemplate(), data));

                _this.$menu = _this.$el.find('.xa-linkItemActionMenu').eq(0);
                _this.isShowMenu = false;
                _this.actionRoleId = null;
                _this.linkCustomeType = "custom";

                _this.initMenuData();
                _this.$el.delegate('.xa-linkItemMenu', 'click', _.bind(_this.onClickItemMenu, _this));
                _this.$el.click(function() {
                    _this.hideActionMenu();
                });
                var data = options.data || null;
            },
            error: function() {
                alert('2')

            }
        });
	},

    showActionMenu: function($icon, parentEl) {
        this.$menu.css({
            top: '170px',
            left: '95px'
        });
        this.$menu.show();
        this.isShowMenu = true;
    },
    
    /**
     * onClickItemMenu: 点击一条内部链接
     */
    onClickItemMenu: function(event){
    	var menuType = $(event.currentTarget).attr('data-type');
    	var item =  this.menus[menuType];
    	var title = item.title;
    	var selectedLinkTarget = this.$el.find('#menuLinkTarget').data('menuLinkTarget');
    	var _this = this;
    	if (title) {
			W.dialog.showDialog('W.dialog.weixin.SelectWebSiteLinkDialog', {
				title: title,
				menuType: menuType,
				menuItem: item,
				selectedLinkTarget: selectedLinkTarget,
				getLinkTargetJsonFun: _this.getLinkTargetJson,
				success: function(data) {
    				_this.setEditHtml(data, true);
    				_this.trigger('finish-select-url', data)
				}
			});
    	} else {
    		var data = this.getLinkTargetJson(item.id, item.name, item.name, item.name, item.name, item.link)
    		
	        if (data.data === null) {
	            alert('没有设置该链接');
	            return false;
	        }
    		this.setEditHtml(data, true);
    		this.trigger('finish-select-url', data)
    	}
    },

    /**
     * setEditHtml： 选择链接后的页面展示
     */
    setEditHtml: function(data, isTrigger){
        var $selectedTitleBox = this.$el.find('.xui-selected-title-box');
        var $selectedTitle = $selectedTitleBox.find('.xui-selected-title');
        var $selectLinkMenu = this.$el.find('.xa-news-editor-select-link-menu');

        var $urlDisplayValueInput = this.$el.find('#menuUrlDisplayValue');
        var $urlInput = this.$el.find('#menuUrl');
        var $linkTargetInput = this.$el.find('#menuLinkTarget');
    	if (data && data.length > 0) {
    		// 选择链接
            var linkTarget = $.parseJSON(data);
            var linkTargetStr = data;

    		if (linkTarget.workspace !== this.linkCustomeType) {
    			// 外部链接不需要处理
	    		$urlDisplayValueInput.attr('disabled','disabled');
		    	$selectedTitle.text(linkTarget.data_path);
		    	$selectedTitleBox.show();
	    		$selectLinkMenu.text('修改');
    		}else{
                $urlDisplayValueInput.removeAttr('disabled')
                $selectedTitleBox.hide();
                $selectLinkMenu.text('从微站选择');
            }

            $linkTargetInput.data('menuLinkTarget', linkTargetStr).val(linkTargetStr);
			$urlDisplayValueInput.val(linkTarget.data);
    		$urlInput.val(linkTarget.data);
    		
    		if (!linkTarget.data_path || linkTarget.data_path.length <= 0) {
    			this.$el.find('.xui-selected-title-box').hide();
    		}
    	}else{
    		// 未选择链接
			$linkTargetInput.data('menuLinkTarget', '').val('');
	    	$urlDisplayValueInput.val('').removeAttr('disabled');
            $urlInput.val('');

	    	$selectedTitle.text('');
	    	$selectedTitleBox.hide();
	    	$selectLinkMenu.text('从微站选择');
    	}

    	if (isTrigger) {
    		// 是否 trigger input
			$urlDisplayValueInput.trigger('input');
    		$linkTargetInput.trigger('input');	
    		$urlInput.trigger('input');
    	}
    },
	
    /**
     * handlerCustomerUrl: 处理外部链接
     */
    handlerCustomerUrl: function(){
		var linkTargetVal = this.$el.find('#menuLinkTarget').val();
		var linkTarget = $.parseJSON(linkTargetVal);
		if (linkTargetVal.length < 3 || linkTarget.workspace == this.linkCustomeType) {
			var urlVar = this.$el.find('#menuUrlDisplayValue').val();
	    	var data = this.getCustomerLinkTargetJson(urlVar)
	    	this.setEditHtml(data, true);
		}
    }
});