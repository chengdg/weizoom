ensureNS('W.view.termite');
W.view.termite.NavbarSecondNav = Backbone.View.extend({
	events: {
		'click .xa-navbar-secondnav-add': 'onClickAddSecondNav',
		'input input[type="text"]': 'onInputValue',
        'input .xa-second-nav-selectLink-url': 'onManualInputUrl',
        'click .xa-second-nav-link-menu': 'onClickLinkMenuButton',
        'click .xa-second-nav-selectLink-close': 'onClickCloseLinkButton',
        'click .xa-second-nav-close': 'onClickCloseSecondNav',
	},

	templates: {
		viewTmpl: '#termite-navbar-secondnav-tmpl',
		navTmpl: '#termite-navbar-secondnav-tmpl-nav'
	},

	initialize: function(options) {
		this.$el = $(this.el);
        this.navsStr = this.$el.attr('data-json') || '';
        this.navsbarType = this.$el.attr('data-navbar-type') || '';
        this.maxItemLength = 5;
	},

	render: function() {
        var _this = this;
		var template = this.getTmpl('viewTmpl');
		var html = template({});
        this.$el.html(html);

        var navsJson = JSON.parse(this.navsStr);
        if (navsJson.length > 0) {
            for (var i = 0; i < navsJson.length; i++) {
                this.addSecondNav(navsJson[i]);
            };
        }

        /* 修改显示的box */
        _.delay(function() {
            _this.trigger('update-show-box', _this.$el, navsJson.length);
        }, 30);
	},

    setNavbarType: function(type){
        if (type == 'weixin') {
            this.setMaxItemLength(5);
        } else {
            this.setMaxItemLength(999);
        }
    },

    setMaxItemLength: function(length){
        this.maxItemLength = length;
        this.isShowAddBtn();
    },

    isShowAddBtn: function(){
        var length = this.$el.find('.xa-nav').length;
        if (this.maxItemLength <= length && this.maxItemLength > 0) {
            this.$el.find('.xa-navbar-secondnav-add').hide();
        }else{
            this.$el.find('.xa-navbar-secondnav-add').show();
        }
    },

    addSecondNav: function(data){
        if (data.target) {
            data['targetData'] = JSON.parse(data.target);
        };
        var template = this.getTmpl('navTmpl');
        var html = template(data);
        this.$('.xa-navbar-secondnav-navs').append($(html));
    },

    setJsonData: function(){
        var $navs = this.$('.xa-nav');
        var navs = [];
        for (var i = 0; i < $navs.length; ++i) {
            var $nav = $navs.eq(i);
            var title = $.trim($nav.find('[name="title"]').val());
            var target = $.trim($nav.find('[name="second-nav-target"]').val());
            navs.push({
                title: title,
                target: target
            })
        }
        this.trigger('update-data', JSON.stringify(navs));
    },

	onClickAddSecondNav: function(event) {
		var template = this.getTmpl('navTmpl');
		var html = template({});
		this.$('.xa-navbar-secondnav-navs').append($(html));

        var length = this.$el.find('.xa-nav').length;
		this.trigger('update-show-box', this.$el, length);
        this.setJsonData();

        this.isShowAddBtn();
	},

	onInputValue: function(event) {
        this.setJsonData();
	},
	
    /**
     * onClickLinkMenuButton: 点击选择链接按钮
     */
    onClickLinkMenuButton: function(event){
        var _this = this;
        var $el = $(event.currentTarget).parent('.xui-eidt-urlBox');
        // 实例化选择链接view
        this.linkView = W.getSelectWebSiteLinkView({
            el: $el
        });
        this.linkView.onClickLinkMenu(event);
        this.linkView.unbind('finish-select-url');
        this.linkView.bind('finish-select-url', function(data){
            _this.updateBoxShow($el, data)
        });
    },

    /**
     * updateBoxShow: 修改显示格式
     */
    updateBoxShow: function($el, data){
        $el.find('[name="second-nav-target"]').val(data);
        if (data.length > 0) {
            var linkData = $.parseJSON(data);
            if (linkData.type === 'manualInput') {

            } else {
                $el.find('.xa-second-nav-selected-title-box').show();
                $el.find('.xa-second-nav-selectLink-url').val(linkData.data).attr('disabled','disabled').trigger('input');
                $el.find('.xa-second-nav-selectLink-title').text(linkData.data_path);
                $el.find('.xa-second-nav-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
            }
        }else{
            $el.find('.xa-second-nav-selected-title-box').hide();
            $el.find('.xa-second-nav-selectLink-url').val('').removeAttr('disabled').trigger('input');
            $el.find('.xa-second-nav-selectLink-name').text('');
            $el.find('.xa-second-nav-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');
        }
    },
    /**
     * onSelectedLinkUrl: 选择完成链接后，调用该函数
     */
    onSelectedLinkUrl: function(event, data){
        var $input = $(event.currentTarget).parent().find('input[type="hidden"]');
        $input.val(data).trigger('input');
    },

    /**
     * onManualInputUrl: 手工输入链接的响应函数
     */
    onManualInputUrl: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $input = $(event.currentTarget);
        var url = $input.val();
        if (url.length >= 7 && url.substr(0, 3) != './?' && url.substr(0, 7) != 'http://') {
            url = 'http://'+ url
            $input.val(url);
        };
        var linkData = {data:url, data_path:"", type:'manualInput'};
        var $el = $(event.currentTarget).parents('.xui-eidt-urlBox');
        this.updateBoxShow($el, JSON.stringify(linkData));
    },

    /**
     * onClickCloseLinkButton: 关闭已选择的链接
     */
    onClickCloseLinkButton: function(event){        
        event.stopPropagation();
        event.preventDefault();
        var $el = $(event.currentTarget).parents('.xui-eidt-urlBox');
        this.updateBoxShow($el, "");
    },

    /**
     * onClickCloseSecondNav: 删除一条二级菜单
     */
    onClickCloseSecondNav: function(event){
        var $secondEl = $(event.currentTarget).parents('.xa-nav');
        $secondEl.remove();

        this.setJsonData();
        var length = this.$el.find('.xa-nav').length;
        this.trigger('update-show-box', this.$el, length);
        
        this.isShowAddBtn();
    }

});

W.registerUIRole('[data-ui-role="termite-navbar-secondnav"]', function() {
    var $el = $(this);
    var view = new W.view.termite.NavbarSecondNav({
        el: $el.get(0)
    });
    view.render();

    //缓存view
    $el.data('view', view);
});