/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 一条微信消息
 * @class
 */
ensureNS('W.model.weixin');
W.model.weixin.Message = Backbone.Model.extend({
}, {
	idCounter: -99,
	index: 1,

	createNewMessage: function(type, metadata) {
		var id = this.idCounter;
		this.idCounter += 1;
		var index = this.index;
		this.index += 1;

		var scheduledDate = null;
		if (metadata) {
			if (metadata.scheduledDate) {
				scheduledDate = metadata.scheduledDate;
			} 
		}	
		if (!scheduledDate) {
			var date = new Date();
			scheduledDate = (date.getYear()+1900)+'-'+(date.getMonth()+1)+'-'+date.getDate();
		}
		var message = new W.model.weixin.Message({
			id: id,
			display_index: index,
			type: type,
			title: '',
			text: '',
			summary: '',
			pic_url: '',
			url: '',
			link_target: '',
			is_show_cover_pic: true,
			date: scheduledDate,
			metadata: {}
		});
		if (metadata) {
			message.set('metadata', metadata);
		}

		return message;
	},

	createNewsMessage: function(metadata) {
		return this.createNewMessage('news', metadata);
	},

	createTextMessage: function(metadata) {
		return this.createNewMessage('text', metadata);
	}
});


/**
 * 消息集合
 * @class
 */
W.model.weixin.Messages = Backbone.Collection.extend({
	model: W.common.Message,

	initialize: function() {

	}
});