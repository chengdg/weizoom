W.DropBox = Backbone.View.extend({
	tagName: 'div',
	
	className: 'dropdown-menu dropdown-absolte',
	
	isArrow: true,
	
	isTitle: true,
	
	position: 'down-right',
	
	initialize: function(options) {
		var _this = this;
		
		options = options || {};
		this.$el = $(this.el);
		this.$html = $('html');
		
		this.isInFileInput = false;
		this.$el.bind('click', function(event) {
			//console.log(event.target.type)
			if('file' === event.target.type || 'checkbox' === event.target.type || 'checkbox' === event.target.className) {
				_this.isInFileInput = true;
				return;
			}
			return false;
		});
		this.$el.delegate('.tx_close', 'click', function(event) {
			_this.close(event);
		});
		
		this.$content = $('<div class="drop-box-content tx_content"></div>');
		this.$arrow = $('<div class="drop-box-arrow"></div>');
		this.$title = $('<div class="drop-box-title"><h2 class="tx_title"></h2><button class="close tx_close" type="button">×</button></div>');
		this.$loading = this.$content;
		this.buildHtml();
		
		if(options.width) {
			this.$el.css({'width': options.width+'px'});
		}
		$('body').append(this.$el);
		
		this.initializePrivate();
	},
	
	initializePrivate: function() {
	
	},
	
	bindLoading: function(isShow) {
		if(isShow) {
			this.$loading.addClass('drop-box-loading');
		}
		else {
			this.$loading.removeClass('drop-box-loading');
		}
	},
	
	buildHtml: function() {
		if(this.isArrow) {
			this.$el.append(this.$arrow);
			this.$arrow.attr('class', 'drop-box-arrow-'+this.position);
		}
		if(this.isTitle) {
			this.$el.append(this.$title);
		}
		
		this.$el.append(this.$content);
	},
	
	setPosition: function(position) {
		var $action = this.$action;
		var elOffset = $action.offset();
		var elWidth = $action.width();
		var elHeight = $action.height();
		var currWidth = this.$el.width() || 0;
		var arrowHeight = this.$arrow ? this.$arrow.height() : 0;
		
		var isBtn = $action.hasClass('btn') || $action.hasClass('dropdown-toggle');
		var widthCount = $action.hasClass('btn') ? 28 : 16;
		elWidth = isBtn ? elWidth + widthCount : elWidth;
		elHeight = isBtn ? elHeight + 8 : elHeight;
		
		var position = position || this.position;
		switch(position) {
		case 'down-right':
			this.$el.css({
				left: (elOffset.left + elWidth) - currWidth,
				top: elOffset.top + elHeight + arrowHeight
			});
			break;
		case 'down-left':
			this.$el.css({
				left: elOffset.left,
				top: elOffset.top + elHeight + arrowHeight
			});
			break;
		}
		this.$arrow.attr('class', 'drop-box-arrow-'+position);
	},
	
	show: function(options) {
		if(this.isDisabledClose) {
			return;
		}
		//console.log('show bengin')
		this.bind('loading', this.bindLoading, this);
		this.close();
		this.trigger('show');
		this.bindHtmlClickEvent();
		//获取定位元素
		this.$el.show();
		this.$action = options.locationElement || options.$action;
		this.setPosition();
		
		this.showPrivate(options);
		//console.log('show end')
	},
	
	bindHtmlClickEvent: function() {
		var _this = this;
		this.$html.off('click.dropdown.drop-box-weizhong');
		this.$html.bind('click.dropdown.drop-box-weizhong', function (event) {
			//console.log('click.dropdown',_this.isDisabledClose, _this.isInFileInput, event.target === _this.$action[0])
			if(_this.isInFileInput || _this.isDisabledClose) {
				_this.isInFileInput = false;
				return;
			}
			if(event.target === _this.$action[0]) {
				return;
			}
			_this.isInFileInput = false;
			_this.hide();
		})
	},
	
	showPrivate: function(options) {
	
	},
	
	hide: function(event) {
		this.closePrivate(event);
		this.trigger('close');
		this.$el.hide();
		this.unbind();
		this.$html.off('click.dropdown.drop-box-weizhong');
		//console.log('hide end')
	},
	
	close: function(event) {
		//console.log('close',this.$el)
		this.$html.trigger('click.dropdown');
	},
	
	closePrivate: function() {}
});