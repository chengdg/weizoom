/*
 Copyright (c) 2011-2012 Weizoom Inc
 */

W.TimelinesView = Backbone.View.extend({
	el: '.tx_timelinesActionView',

	getTemplate: function() {
		$('#timelines-action-view').template('timelines-action-view-tmpl');
		return 'timelines-action-view-tmpl';
	},

	events: {
		'click .tx_selectAll': 'selectAll',
		'click .tx_moveTimeline': 'moveTimeline',
		'click .tx_selectTimeline': 'selectTimeline'

	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.options.timelinesOptions = this.options.timelinesOptions || {};

		this.$el.html($.tmpl(this.getTemplate()));

		//创建Timeline集合
		this.options.collection = options.collection || this.collection;

		this.$('.tx_selectAll').attr('disabled', true);
		this.options.collection.bind('add', this.addCollection, this);
		this.options.collection.bind('add', function() {
			this.$('.tx_selectAll').attr('checked', false);
		}, this);
		this.options.collection.bind('reset', function(resp) {
			this.$('.tx_selectAll').attr('checked', false).attr('disabled', true);
		}, this)

		this.options.collection.bind('change:isSelected', this.bindChangeSelected, this);
	},

	/**
	 * 响应全选框的的点击事件
	 * @param event
	 */
	selectAll: function(event) {
		var isSelected = event.target.checked;
		this.options.collection.each(function(timeline) {
			timeline.set({'isSelected': isSelected});
		});

//		this.$('.tx_moveTimeline').attr('disabled', !isSelected);
	},

	addCollection: function(model) {
		this.$('.tx_selectAll').attr('disabled', false);
		model.bind('change:isSelected', this.bindChangeSelected, this);
	},


	bindChangeSelected: function() {
		var _this = this;
		var isAllSelected = true;
		var isDisabled = true;
		this.options.collection.each(function(model) {
			if(!model.get('isSelected')) {
				isAllSelected = false;
			}else {
				isDisabled = false;
			}
		});
		this.$('.tx_selectAll').attr('checked', isAllSelected);
//		this.$('.tx_moveTimeline').attr('disabled', isDisabled);
	},

	getSelectedTimeline: function() {
		var selectedModels = null;
		if (this.options.collection) {
			//过滤出被选中的model集合
			selectedModels = this.options.collection.filter(function(model) {
				return model.get('isSelected');
			});
		}

		if (selectedModels && selectedModels.length !== 0) {
			return selectedModels;
		}
	},

	moveTimeline: function(event) {
		xlog('move');
		var models = this.getSelectedTimeline();
		if(!models) {
			this.$('.tx_moveTimeline').removeClass('open');
			event.stopPropagation();
			event.preventDefault();
			W.getErrorHintView().show('请先选择客户');
			return;
		}
		var _this = this;
		var timelineIds = _.map(models, function(model) {return model.get('id');});

		W.ISELECTED_GROUPS_LOADING = true;
		var moveDropBox = W.getMoveTimelineDropBox();
		moveDropBox.show({
			locationElement:$(event.currentTarget),
			isShowAddGroupButton : true,
			isShowAll: false
		});
		moveDropBox.bind(moveDropBox.CLICK_ACTIONS_EVENT, function(resp) {
			W.getApi().call({
				app: 'customer',
				api: 'customer_group/update',
				method: 'post',
				args: {
					ids: timelineIds.join(','),
					groupId: resp.id
				},
				success: function(data) {
					_.map(models, function(model) {
						model.set({group_id: resp.id, isSelected: false});
					})
				},
				error: function(resp) {
				},
				scope: this
			});
		}, this);
	},

	selectTimeline: function(event) {
		var moveDropBox = W.getMoveTimelineDropBox();
		moveDropBox.show({
			locationElement:$(event.currentTarget),
			isShowAddGroupButton : false,
			isShowAll: true
		});
		moveDropBox.bind(moveDropBox.CLICK_ACTIONS_EVENT, function(resp) {
			this.$('.tx_selectTimeline').html(resp.name+'&nbsp;<span class="caret"></span>');
//			this.$('.tx_moveTimeline').attr('disabled', true);
			this.trigger('selectGroup', {'groupId': resp.id});
		}, this);
	}
})
