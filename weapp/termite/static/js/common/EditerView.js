/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 编辑器
 * @class
 */
W.EditerView = Backbone.View.extend({	
	className: 'editerViewDiv',
	
	getTemplate: function() {
		if (!this.isTemplateInitialized) {
			$('#editer-view-tmpl-src').template('editer-view-tmpl');
			this.isTemplateInitialized = true;
		}
		return 'editer-view-tmpl';
	},
	
	events: {
		'click .addLink': 'addLink',
	},
	
	initialize: function(options) {
		xlog('create editer view');
		this.$textarea = $(this.el);
		if (options.initClean) {
			this.$textarea.val('');
		}
		this.$textarea.wrap('<div class="editorView"/>');
		this.$el = this.$textarea.parent();
		this.el = this.$el[0];
		
		this.maxCount = options.maxCount || 300;
		this.showAddLink = options.showAddLink || false;
		this.position = options.position || 'top';
		this.isTemplateInitialized = false;

		//绑定keyup事件
		var onInputContent = _.bind(this.onInputContent, this);
		this.$textarea.on('input', onInputContent);
	},
	
	render: function() {
		var options = {
			showAddLink: this.showAddLink,
			maxCount: this.maxCount
		}
		var node = $.tmpl(this.getTemplate(), options);
		if (this.position === 'top') {
			this.$el.prepend(node);
		} else {
			this.$el.append(node);
		}

		this.$el.append('<div class="errorHint"></div>');

		this.$wordCountInfo = this.$el.find('.wordCountInfo');
		return this;
	},

	focus: function() {
		this.$textarea.focus();
	},
	
	getHtml: function() {
		return this.$el;
	},
	
	onInputContent: function(event) {
		var lengthValue = this.getLength();
		if(lengthValue.isValid) {
			this.$wordCountInfo.removeClass('red').html('您还可以输入<span class="wordCount">'+lengthValue.length+'</span>个字');
			this.trigger('under_count_limit');
		}else {
			this.$wordCountInfo.addClass('red').html('已超出<span class="wordCount">'+lengthValue.length+'</span>个字');
			this.trigger('exceed_count_limit');
		}
	},
	
	getLength: function() {
		var value = $.trim(this.$textarea.val());
		var valueLength = value.length;
		var maxLength = this.maxCount;

		if(valueLength > maxLength) {
			length = -parseFloat(maxLength-valueLength,10);
			length = Math.round(length);
			return {isValid: false, length: length};
		}else {
			return {isValid: true, length: parseInt(maxLength-valueLength,10)};
		}
	},
	
	addLink: function(event) {
		var _this = this;
		var addLinkDialog = W.getAddLinkDialog({
			title: '添加链接'
		});
		addLinkDialog.bind(addLinkDialog.SUBMIT_SUCCESS_EVENT, function() {
			var content = _this.$textarea.val();
			content = content + addLinkDialog.link;
			_this.$textarea.val(content);
			_this.$textarea.keyup();
			addLinkDialog.close();
		}, addLinkDialog);
		addLinkDialog.show({});
	},

	val: function() {
		return $.trim(this.$textarea.val());
	}
});