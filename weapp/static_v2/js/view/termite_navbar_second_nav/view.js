ensureNS('W.view.termite');
W.view.termite.NavbarSecondNav = Backbone.View.extend({
	events: {
		'click .xa-navbar-secondnav-add': 'onClickAddSecondNav',
		'input input[type="text"]': 'onInputValue',
        'click .xa-second-nav-link-menu': 'onClickLinkMenuButton',
        'input .xa-selectLink-url': 'onManualInputUrl',
        'click .xa-selectLink-close': 'onClickCloseLinkButton',
	},

	templates: {
		viewTmpl: '#termite-navbar-secondnav-tmpl',
		navTmpl: '#termite-navbar-secondnav-tmpl-nav'
	},

	initialize: function(options) {
		this.$el = $(this.el);
        this.navsStr = this.$el.attr('data-json') || '';
        console.log(234234, this.navsStr)
	},

	render: function() {
        console.log('render', this.navsStr, 6565)
		var template = this.getTmpl('viewTmpl');
		var html = template({});

        this.$el.html(html);

        if (this.navsStr.length > 0) {
            var json = JSON.parse(this.navsStr);
            console.log(7878, json)
            for (var i = 0; i < json.length; i++) {
                this.addSecondNav(json[i]);
            };
        }
	},

    addSecondNav: function(data){
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
            var target = $.trim($nav.find('[name="target"]').val());
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
		this.trigger('update-show-box', $(event.target).parents('.propertyGroup_property_dynamicControlField_content'), false);
        this.setJsonData();
	},

	onInputValue: function(event) {
        this.setJsonData();
	},
	
    /**
     * onClickLinkMenuButton: 点击选择链接按钮
     */
    onClickLinkMenuButton: function(event){
        var el = $(event.currentTarget).parent('.xui-eidt-urlBox');
        // 实例化选择链接view
        this.linkView = W.getSelectWebSiteLinkView({
            el: el
        });
        this.linkView.onClickLinkMenu(event);
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
        var $targetInput = $input.parent().find('input[type="hidden"]');
        $targetInput.val(JSON.stringify(linkData)).trigger('input');
    },

    /**
     * onClickCloseLinkButton: 关闭已选择的链接
     */
    onClickCloseLinkButton: function(event){        
        event.stopPropagation();
        event.preventDefault();

        var $input = $(event.currentTarget).parents('div.propertyGroup_property_input').find('input[type="hidden"]');
        $input.val("").trigger('input');
    },

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