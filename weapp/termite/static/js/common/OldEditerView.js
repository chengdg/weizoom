W.OldEditerView = Backbone.View.extend({
	tagName: 'div',
	
	className: 'editerViewDiv',
	
	SUBMIT_EVENT: 'submit',
	
	getTemplate: function() {
		$('#old-editer-view-tmpl-src').template('old-editer-view-tmpl');
		return 'old-editer-view-tmpl';
	},
	
	events: {
		'keyup #messageText': 'keyUpText',
		'click #replyMessage': 'doSubmit',
		'click .addLink': 'addLink',
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.templateName = this.getTemplate();
		this.maxCount = options.maxCount || 300;
		this.showAddLink = options.showAddLink || false;
		type = options.type || 'top';
		if (type === 'top') {
			this.showTop = true;
			this.showBottom = false;
		} 
		else {
			this.showTop = false;
			this.showBottom = true;
		}
		this.textarea = this.$el.find('#messageText');
	},
	
	render: function() {
		var options = {
			showTop: this.showTop,
			showBottom: this.showBottom
		}
		var pagination_dom = $.tmpl(this.getTemplate(), options);
		this.$el.html(pagination_dom);
		return this;
	},
	
	getHtml: function() {
		return this.$el;
	},
	
	keyUpText: function(event) {
		var lengthValue = this.getLength();
		if(lengthValue.isValid) {
			this.$el.find('.wordCounInfo').removeClass('red').html('您还可以输入<span class="wordCount">'+lengthValue.length+'</span>个字');
			this.$el.find('.doReplyMessage').attr('disabled', false);
		}else {
			this.$el.find('.wordCounInfo').addClass('red').html('已超出<span class="wordCount">'+lengthValue.length+'</span>个字');
			this.$el.find('.doReplyMessage').attr('disabled', true);
		}
	},
	
	getLength: function(event) {
		var valueLength;
		var maxLength = this.maxCount;
		var value = $.trim(this.$el.find('#messageText').val());
		
		value = value.replace(/[^\x00-\xff]/g, "**");
		
		var reg = /(http:\/\/|https:\/\/)((\w|%|=|\?|\.|\/|&|-|#|:)+)/g;
		var https = value.match(reg);
		if(https != null){
			//处理文中的url链接长度，每个url链接的长度计算为20个长度
			value = value.replace(reg, '');
			httpLength = value.length/2;
			valueLength = httpLength + https.length * 10;
		}else{
			valueLength = value.length/2;
		}
		
		if(valueLength > maxLength) {
			length = -parseFloat(maxLength-valueLength,10);
			length = Math.round(length);
			return {isValid: false, length: length};
		}else {
			return {isValid: true, length: parseInt(maxLength-valueLength,10)};
		}
	},
	
	doSubmit: function(event) {
		var lengthValue = this.getLength();
		if(!lengthValue.isValid) {
			textarea.keyup();
			return;
		}
		
		this.trigger(this.SUBMIT_EVENT);
	},
	
	clean: function() {
		this.$el.find('#messageText').val('').click();
	},
	
	addLink: function(event) {
		var _this = this;
		var addLinkDialog = W.GetAddLinkDialog({
			title: '添加链接'
		});
		addLinkDialog.bind(addLinkDialog.SUBMIT_SUCCESS_EVENT, function() {
			var content = _this.$el.find('#messageText').val();
			content = content + addLinkDialog.link;
			_this.$el.find('#messageText').val(content);
			_this.$el.find('#messageText').keyup();
			addLinkDialog.close();
		}, addLinkDialog);
		addLinkDialog.show({});
	},
});