/*
 Copyright (c) 2011-2012 Weizoom Inc
 */
/**
 * News编辑器
 * @class
 */
ensureNS('W.view.apps');
W.view.apps.PrizeKeywordPane = Backbone.View.extend({
	el: '',
	add_keyword_div:'',
	add_keyword_btn:'',
	page_keywords:'',

	events: {
		'keypress .xa-app-add': 'onPressEnter',
		'click .xa-mistiness': 'onClickMistinessRadio',
		'click .xa-exact': 'onClickExactRadio',
		'click .xa-cancel': 'onClickClose'
	},

	initialize: function(options) {
        this.md = "精确匹配";
        this.type = "accurate";
        this.template = Handlebars.compile($("#apps-prize-keywordpane-src").html());

		this.$add_keyword_btn = $(options.add_keyword_btn);
		this.add_keyword_btn = options.add_keyword_btn;
		this.num = 0;
		this.xx= 0;
		this.yy= 0;
		this.keywords_obj = {};

		render();
	},
	render: function() {
		this.xx = this.$add_keyword_btn.offset().top;
		this.yy = this.$add_keyword_btn.offset().left;
		var offset ={top:this.xx,left:this.yy};
		this.setPos(offset);
	},
	render_keywords: function(page_keywords){
		//只渲染关键字区域
		var keywords = page_keywords==""?{}:JSON.parse(page_keywords);
		if(keywords){
			for(var i in keywords){
				var mod = "";
				if(keywords[i]=='accurate'){
					mod = "精确匹配";
				}else{
					mod = "模糊匹配";
				}
				var pattern = {
					keyword: i,
					mode: mod,
					type: keywords[i]
				};
				$(this.template(pattern)).insertBefore(this.$add_keyword_btn);
			}
		}
	},

	onPressEnter: function (e) {
		if (e.keyCode == 13) {
			var _this = this;
			//判断关键词个数是否超过8个
			var i_length=0;
			for(var i in this.keywords_obj){
				i_length++;
			}
			if (i_length >=8){
				W.showHint('error', '关键词个数不能超过8个');
				return;
			}
			//替换相邻多个空格为一个
			var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');//关键字
			if(keyword == '') {
				W.showHint('error','关键字不能为空！');
				return;
			}
			if(keyword.length > 5) {
				W.showHint('error','单个关键词字数不能超过5个字');
				return;
			}

			//关键字·组_检查
			//var keywords = [];//关键字组
			//var keywords_obj = [];//关键字组对象
			//this.$add_keyword_div.find('.xa-data-patterns').each(function(){
			//	var key_tmp = $(this).find('.data-keyword').text().replace(/\n/g,'').replace(/\r/g,'').replace(/\r\n/g,'').replace(/\s+/g, '').trim();
			//	var mode_tmp = $(this).find('.xa-data-type').attr('data-type').trim();
			//	keywords.push(key_tmp);
			//	keywords_obj.push({'keyword':key_tmp,'mode':mode_tmp});
			//});

			this.keywords_obj[_this.$('.xa-app-add').val()] = _this.type;

			this.trigger('add_keywords', this.keywords_obj);

			this.xx = this.$add_keyword_btn.offset().top;
			this.yy = this.$add_keyword_btn.offset().left;
			var offset ={top:this.xx,left:this.yy};
			_this.setPos(offset);

		}

	},

	onClickMistinessRadio: function() {
		this.md = "模糊匹配";
		this.type = "blur";
	},

	onClickExactRadio: function() {
		this.md = "精确匹配";
		this.type = "accurate";
	},

	onClickSubmit: function(){
		this.num += 1;
		//替换相邻多个空格为一个
		var keyword = this.$('.xa-app-add').val().trim().replace(/\s+/g, ' ');//关键字
		if(keyword == '') {
			W.showHint('error','关键字不能为空！');
			return;
		}
		if(keyword.length > 5) {
			W.showHint('error','单个关键词字数不能超过5个字');
			return;
		}

		//关键字_组_检查
		var keywords = [];//关键字组
		var keywords_obj = [];//关键字组对象
		this.$add_keyword_div.find('.xa-data-patterns').each(function(){
			var key_id = $(this).attr('id');
			var key_tmp = $(this).find('.data-keyword').text().replace(/\n/g,'').replace(/\r/g,'').replace(/\r\n/g,'').replace(/\s+/g, '').trim();
			var mode_tmp = $(this).find('.xa-data-type').attr('data-type').trim();
			keywords.push(key_tmp);
			keywords_obj.push({'keyword':key_tmp,'mode':mode_tmp});
		});

		//判断关键词个数是否超过8个
		if (keywords.length > (8 - 1)) {
			W.showHint('error', '关键词个数不能超过4个');
			return;
		}
		//关键字重复检查
		for(var i=0;i<keywords.length;i++){
			if(keyword==keywords[i]){
				W.showHint('error','关键字不能重复！');
				return;
			}
		}
		//插入模板
		var _this = this;
		var pattern = {
					keyword: _this.$('.xa-app-add').val(),
					mode: _this.md,
					type: _this.type
				};

		$(_this.template(pattern)).insertBefore(this.$add_keyword_btn);
		_this.$('.xa-app-add').val("");

		//关闭
		_this.hide();
	},

	onClickClose: function() {
		this.hide();
	},

	setPos: function (offset) {
		this.$el.css('position','absolute');
		this.$el.css('top', offset.top-25 + 'px');
		this.$el.css('left', offset.left-438 + 'px');
	},

	show: function() {
		this.$el.show();
	},

	hide: function() {
		this.$el.hide();
	}
});


W.registerUIRole('[data-ui-role="apps-prize-keyword-pane"]', function() {
    var $el = $(this);
	console.log('999999999999999asdasd99999---------');
	console.log(this);
	var view = new W.view.apps.PrizeKeywordPane({
		el:'.xa-keywordBoxDiv',
		add_keyword_btn:'#add_keyword_btn'
	});
	$el.data('view', view);

	$(this).delegate('#add_keyword_btn', 'click', function(){
		view.show();
	});
    //W.getApi().call({
    //    app: 'apps/sign',
    //    resource: 'sign',
    //    method: 'get',
    //    args: {},
    //    success: function(data){
    //        view =
    //        view.trigger('get_keywords', data);
    //        $el.data('view', view);
    //        view.render();
    //    },
    //    error: function(error){
    //        W.showHint('error', '获取优惠券库存失败~');
    //    }
    //});
});