/*
Copyright (c) 2011-2012 Weizoom Inc
*/
W.TagFilterView = function(options) {
	var _this = this;
    this.language = options.language || 'Chinese';
    this.initialize(options);
}

W.TagFilterView.prototype = {    
    languages: {
        Chinese: {
            loading: '加载中...'
        },
        English: {
            loading: 'loading...'
        }
    },

    model: {
		app: 'tour',
		api: 'tags/get',
	},
    
    parse: function(data) {
        this.cacheData = data;
        return data;
    },
    
    initialize: function(options) {
        this.$el = options.$el;
        this.activeId = options.activeId;
        this.templateId = options.templateId;
        this.appTemplate = options.appTemplate;
        this.shopId = options.shopId;
        this.id = options.id;
        this.language = options.language;
        this.fetch();
    },
    
    fetch: function() {
        var _this = this;
        if(this.cacheData) {
            return;
        }
        this.$el.alert({
			'info': this.languages[this.language].loading
		});
        var _this = this;
        args = {};
        args.appTemplate = _this.appTemplate;
        args.shopId = _this.shopId;
        args.id = _this.id;
        args.language = _this.language;
        W.getApi().call({
			api: this.model.api,
			app: this.model.app,
            args: args,
			success: function(data) {
				_this.parse(data);
				_this.render(_this.cacheData);
				_this.$el.alert({
					isShow: false
				});
			},
			error: function(resp) {
				var msg = '更新失败';
				if(!_this.isFirstLoading) {
					msg = '加载失败';
					_this.isFirstLoading = true;
				}
				_this.$el.alert({
					info: msg,
					speed: 2000
				});
			}
		});
    },
    render: function(data) {
        var tmplId = this.templateId + '-tmpl';
		$('#' + this.templateId).template(tmplId);
        data.language = this.language;
        data.nameKey = this.language === 'English' ? 'EN_name' : 'CH_name';
        data.active_id = this.activeId;
		this.$el.html($.tmpl(tmplId, data));
    }
}