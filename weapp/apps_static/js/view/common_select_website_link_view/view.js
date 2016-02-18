/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * 微站内部链接
 * @class
 */
ensureNS('W.view.common')
W.view.common.SelectWebSiteLinkView = Backbone.View.extend({
  el: '',

  events: {
    // 'click .xa-news-editor-select-link-menu': 'onClickLinkMenu',
    'click .xa-close-link': 'onClickCloseLink'
  },

  getTemplate: function() {
    $('#weixin-webapp-link-dropdown-menu-tmpl-src').template('weixin-webapp-link-dropdown-menu-tmpl');
    return 'weixin-webapp-link-dropdown-menu-tmpl';
  },

  initialize: function(options) {
    this.$el = $(this.el);
    var _this = this;
    this.menuEvent = null;
    this.isShowMenu = false;
    this.actionRoleId = null;
    this.linkCustomeType = "custom";

    W.getApi().call({
      app: 'webapp',
      api: 'tools/get',
      async: false,
      // scope: this,
      success: function(tools) {
        tools['isUseWepage'] = W.isUseWepage;
        $('body').append($.tmpl(_this.getTemplate(), tools));

        _this.$menu = $('.xa-linkActionMenu').eq(0);

        _this.tools = tools;
        _this.initMenuData();
        $document = $(document);
        $document.delegate('.xa-itemMenu', 'click', _.bind(_this.onClickItemMenu, _this));
        $document.click(function() {
          _this.hideActionMenu();
        });

        var data = options.data || null;
      },
      error: function() {

      }
    });
    // this.setEditHtml(data);
  },

  setOptions: function(options){
    this.$el = $(options.el);
  },
  
  initMenuData: function(event){
    var _this = this;
    W.getLoadingView().show();
    W.getApi().call({
      method: 'get',
      app: 'new_weixin',
      resource: 'webapp_link_menus',
      args: {},
      success: function(data) {
        W.getLoadingView().hide();
        _this.menus = data;
      },
      error: function(response) {
        // alert('失败');
        W.getLoadingView().hide();
      },
      scope: this
    });
  },

  onClickLinkMenu: function(event, parentEl){
    event.stopPropagation();
    event.preventDefault();

    this.menuEvent = event;
    var $icon = $(event.currentTarget);
    this.showActionMenu($icon, parentEl);
  },

  showActionMenu: function($icon, parentEl) {
    // console.log('parentEl', parentEl, $(parentEl+':visible'))
    var offset = $icon.offset();
    var parentOffset = null;
    var top = offset.top+18;
    var left = offset.left+2;
    // console.log(top, left)
    if (parentEl) {
      parentOffset = $(parentEl+':visible').offset();
      left += parentOffset.left-74;
      top += parentOffset.top+30;
    };
    // console.log(top, left)
    this.$menu.css({
      top: top+'px',
      left: left+'px'
    });
    this.$menu.show();
    this.isShowMenu = true;
  },

  hideActionMenu: function() {
    if (this.isShowMenu) {
      this.$menu.hide();
      this.isShowMenu = false;
      this.actionRoleId = null;
    }
  },

  onClickCloseLink: function(event){
    this.setEditHtml(null, true);
  },

  /**
   * onClickItemMenu: 点击一条内部链接
   */
  onClickItemMenu: function(event){
    var menuType = $(event.currentTarget).attr('data-type');
    var item =  this.menus[menuType];
    
    var title = item.title;
    
    var selectedLinkTarget = this.$el.find('#linkTarget').data('link_target');
    var _this = this;
    if (title) {
      W.dialog.showDialog('W.dialog.weixin.SelectWebSiteLinkDialog', {
        tools: _this.tools,
        title: title,
        menuType: menuType,
        menuItem: item,
        selectedLinkTarget: selectedLinkTarget,
        getLinkTargetJsonFun: _this.getLinkTargetJson,
        success: function(data) {
          //  微众商城代码
          //if(W.uid == 216){
          //  jsonData = JSON.parse(data);
          //  if(jsonData.workspace_name == '商品及分组'){
          //    jsonData.data = jsonData.data.replace('module=mall', 'module=apps:weshop:mall2')
          //    data = JSON.stringify(jsonData)
          //  }
          //}
          _this.setEditHtml(data, true);
          _this.trigger('finish-select-url', data);          
          W.Broadcaster.trigger('link-url:selected', _this.menuEvent, data);
        }
      });
    } else {
      var data = this.getLinkTargetJson(item.id, item.name, item.name, item.name, item.name, item.link)
      if ($.parseJSON(data).data === null) {
        W.showHint('error', '没有设置该链接');
        return false;
      }
      this.setEditHtml(data, true);
      this.trigger('finish-select-url', data);
      W.Broadcaster.trigger('link-url:selected', this.menuEvent, data);
    }
  },

  /**
   * setEditHtml： 选择链接后的页面展示
   */
  setEditHtml: function(data, isTrigger){
    // console.log('setEditHtml', isTrigger, data);
    var $selectedTitleBox = this.$el.find('.xa-selected-title-box');
    var $selectedTitle = $selectedTitleBox.find('.xa-selected-title');
    var $selectLinkMenu = this.$el.find('.xa-news-editor-select-link-menu');

    var $urlDisplayValueInput = this.$el.find('#urlDisplayValue');
    var $urlInput = this.$el.find('#url');
    var $linkTargetInput = this.$el.find('#linkTarget');
    if (data && data.length > 0) {   
      // 选择链接
      // var linkTarget = data;
      // var linkTargetStr = JSON.stringify(data);

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

      $linkTargetInput.data('link_target', linkTargetStr).val(linkTargetStr);
      $urlDisplayValueInput.val(linkTarget.data);
      $urlInput.val(linkTarget.data);
    }else{
      // 未选择链接
      $linkTargetInput.data('link_target', '').val('');
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

  getLinkTargetJson: function(id, menuName, itemTitle, name, data_path, link){    
    var data = {
      'workspace': id,
      'workspace_name': menuName,
      'data_category': itemTitle,
      'data_item_name': name,
      'data_path': data_path,
      'data': link
    }
    return JSON.stringify(data);
  },

  getCustomerLinkTargetJson: function(url){
    return this.getLinkTargetJson(
      this.linkCustomeType,
      "外部链接",
      "外部链接",
      "外部链接",
      url,
      url
    )
  },
  /**
   * handlerCustomerUrl: 处理外部链接
   */
  handlerCustomerUrl: function(){
    var linkTargetVal = this.$el.find('#linkTarget').val();
    var linkTarget = $.parseJSON(linkTargetVal);
    if (linkTargetVal.length < 3 || linkTarget.workspace == this.linkCustomeType) {
      var urlVar = this.$el.find('#urlDisplayValue').val();
      var data = this.getCustomerLinkTargetJson(urlVar)
      this.setEditHtml(data, true);
    }
  }
});

W.getSelectWebSiteLinkView = function(options) {
  var view = W.registry['W.view.common.SelectWebSiteLinkView'];
  if (!view) {
    //创建dialog
    xlog('create W.view.mall.MallOrderRemarkView');
    view = new W.view.common.SelectWebSiteLinkView(options);
    W.registry['W.view.common.SelectWebSiteLinkView'] = view;
  }else{
    view.setOptions(options);
  }
  return view;
};