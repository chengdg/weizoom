/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 一条微信消息
 * @class
 */
W.common.Message = Backbone.Model.extend({
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
			scheduledDate = date.getMonth()+1+'月'+date.getDate()+'日';
		}
		var message = new W.common.Message({
			id: id,
			display_index: index,
			type: type,
			title: '',
			text: '',
			summary: '',
			pic_url: '',
			url: '',
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
W.common.Messages = W.common.MessagesLocalStorage.extend({
	model: W.common.Message,

	initialize: function() {
        this.initializeEvent();
	}
});