/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 定时发布微信编辑器
 * @constructor
 */
W.TimedWeixinEditer = Backbone.View.extend({
	el: '',
	
	getTemplate: function() {
		$('#timed-weixin-editer-tmpl-src').template('timed-weixin-editer-tmpl');
		return 'timed-weixin-editer-tmpl';
	},

	events: {
		'click #timedSend': 'onSelectTimedSend',
		'click #ontimeSend': 'onSelectOntimedSend',
		'click #submitBtn': 'onClickSubmitButton',
		'click #deleteBtn': 'onClickDeleteButton'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		//渲染html
		this.template = this.getTemplate();
		this.$el.html($.tmpl(this.template));
		this.$submitButton = this.$('#submitBtn');
		this.$deleteButton = this.$('#deleteBtn');
		this.$textMessageTab = this.$('a[href="#timedWeixinEditer-textMessageZone"]');
		this.$newsMessageTab = this.$('a[href="#timedWeixinEditer-newsMessageZone"]');
		this.historicalMessage = options.historicalMessage || {};
		this.message = null;

		//创建select news type view
		this.selectNewsTypeView = this.createSelectNewsTypeView();
		this.selectNewsTypeView.bind('before-edit-news', function() {
			var items = this.selectTimeView.getTime().split(' ');
			var queryString = 'date='+items[0]+'&time='+items[1]+'&send_type='+this.getSendType() +'&after_material=1';
			this.selectNewsTypeView.setReturnQueryString(queryString);
		}, this);
		this.selectNewsTypeView.bind('delete-material', function() {
			this.material = 0;
		}, this);

		//创建select time view
		this.selectTimeView = this.createSelectTimeView({
			date: options['date'] || '',
			time: options['time'] || ''
		});
		/*
		if (options['sendType'] === '1') {
			this.changeToOntimeSendMode();
		}
		*/
		this.selectTimeView.bind('select-date', this.onSelectDate, this);
		this.selectTimeView.bind('finish-render-scheduled-days', this.onFinishRenderScheduledDays, this);

		//创建rich editer
		this.richEditer = this.createRichEditer();

		//确定当前type
		this.type = 'text';
		this.material = null;
		this.isAfterMaterial = options.isAfterMaterial || false;
		if (options.material) {
		 	this.type = 'news';
		 	this.material = options.material;
		}
		$('a[data-toggle="tab"]').on('shown', _.bind(function(event) {
			var tab = $(event.target);
			this.type = tab.attr('data-type');
		}, this));
	},

	createSelectTimeView: function(options) {
		var view = new W.SelectTimeView(_.extend({
			el: '#timedWeixinEditer-timeSelecter'
		}, options));
		view.render();

		return view;
	},

	createSelectNewsTypeView: function(options) {
		var view = new W.SelectNewsTypeView({
			el: '#timedWeixinEditer-newsMessageZone'
		});
		view.render();

		return view;
	},

	createRichEditer: function() {
		var _this = this;

		var editor = new W.common.RichTextEditor({
			el: '#textMessage',
			type: 'text',
			width: 420
		});
		editor.bind('blur', function(content) {
			$('#textMessage').html(content);
		});
		editor.render();
		return editor;
	},

	render: function() {
		
	},

    refresh: function(){
        this.selectTimeView.loadScheduledDays();
    },

	/**
	 * 禁用tab
	 */
	disableTab: function() {
		this.$textMessageTab.attr('href', 'javascript:void(0);').parent().addClass('disabled');
		this.$newsMessageTab.attr('href', 'javascript:void(0);').parent().addClass('disabled');
	},

	/**
	 * 启用tab
	 */
	enableTab: function() {
		this.$textMessageTab.attr('href', '#timedWeixinEditer-textMessageZone').parent().removeClass('disabled');
		this.$newsMessageTab.attr('href', '#timedWeixinEditer-newsMessageZone').parent().removeClass('disabled');
	},

	/**
	 * 显示发布类型
	 */
	showSendType: function(type) {
		//确定type value
		var typeValue = null;
		if (type === 'ontime') {
			typeValue = '1';
		} else {
			typeValue = '0';
		}

		//选择相应的radio
		this.$('input[name="send_type"]').each(function() {
			var $radio = $(this);
			if($radio.val() === typeValue) {
				$radio.attr('checked', 'checked');
			} else {
				$radio.removeAttr('checked');
			}
		});

		//根据type，隐藏相应的radio
		if (type === 'ontime') {
			this.$('#ontimeSendControl').show();
			this.$('#timedSendControl').hide();
		} else if (type === 'timed') {
			this.$('#timedSendControl').show();
			this.$('#ontimeSendControl').hide();
		} else {
			this.$('#ontimeSendControl').show();
			this.$('#timedSendControl').show();
		}
	},

	getSendType: function() {
		var sendType = null;
		this.$('input[name="send_type"]').each(function() {
			var $radio = $(this);
			if($radio.is(":checked")) {
				sendType = $radio.val();
			}
		});
		return sendType;
	},

	/**
	 * 点击"立即发送"的响应函数
	 */
	onSelectOntimedSend: function() {
		this.selectTimeView.setToNow();
	},

	/**
	 * 点击"定时发送"的响应函数
	 */
	onSelectTimedSend: function() {
		this.selectTimeView.enableSelect();
	},

	/**
	 * 启用提交按钮
	 */
	enableSubmitButton: function() {
		if (this.$submitButton.is(":disabled")) {
			this.$submitButton.addClass('btn-success').removeAttr('disabled');
		}
	},

	/**
	 * 禁用提交按钮
	 */
	disableSubmitButton: function() {
		if (!this.$submitButton.is(":disabled")) {
			this.$submitButton.removeClass('btn-success').attr('disabled', 'disabled');
		}
	},

	/**
	 * 启用删除按钮
	 */
	enableDeleteButton: function() {
		if (!this.$deleteButton.is(":visible")) {
			this.$deleteButton.show();
		}
	},

	/**
	 * 禁用提交按钮
	 */
	disableDeleteButton: function() {
		if (this.$deleteButton.is(":visible")) {
			this.$deleteButton.hide();
		}
	},

	/**
	 * 进入显示模式
	 */
	enterDisplayMode: function(dateInfo, message) {
		//时间固定
		this.selectTimeView.fixToTime(message.scheduled_hour, message.scheduled_minutes);

		//发布方式
		if (message.send_type === '定时消息') {
			this.showSendType('timed');		
		} else {
			this.showSendType('ontime');
		}

		//tab区域
		if (message.type === '图文消息') {
			var materialId = $.parseJSON(message.content).material;
			var enableDelete = this.isAfterMaterial;
			this.selectNewsTypeView.showMaterial(materialId, enableDelete, dateInfo.date);
			this.$newsMessageTab.tab('show');
		} else {
			this.selectNewsTypeView.showEditLink();
			this.richEditer.setContent(message.content);
			this.$textMessageTab.tab('show');
		}
		var tab = this.$('#tabZone');
		if (!tab.is(":visible")) {
			tab.show();
		}
		this.disableTab();

		//发布按钮
		this.disableSubmitButton();

		//删除按钮
		if (dateInfo.isHistory) {
			this.disableDeleteButton();
		} else {
			this.enableDeleteButton();
		}
	},

	/**
	 * 进入编辑模式
	 */
	enterEditMode: function(dateInfo, material) {
		//时间可选
		this.selectTimeView.enableSelect();

		//发布方式
		if (dateInfo.isToday) {
			this.showSendType('both');
		} else {
			this.showSendType('timed');
		}

		//tab区域
		if (material) {
			var enableDelete = this.isAfterMaterial;
			this.selectNewsTypeView.showMaterial(material, enableDelete, dateInfo.date);
			this.$newsMessageTab.tab('show');
		}  else {
			this.selectNewsTypeView.showEditLink();
			this.$textMessageTab.tab('show');
		}
		var tab = this.$('#tabZone');
		if (!tab.is(":visible")) {
			tab.show();
		}

		//发布按钮
		if (dateInfo.isHistory) {
			this.disableSubmitButton();
		} else {
			this.enableSubmitButton();
		}

		//删除按钮
		this.disableDeleteButton();
	},

	/**
	 * 选择一个日期的响应函数
	 */
	onSelectDate: function(dateInfo) {
		//reset
		this.enableTab();
		this.richEditer.setContent('')
		W.getErrorHintView().hide();
		W.getItemDeleteView().hide();


		if (dateInfo.isScheduled) {
			//获取已定制消息
			W.getApi().call({
				app: 'masssend',
				api: 'message/get',
				args: {
					date: dateInfo.date
				},
				success: function(data) {
					this.message = data.message;
					this.enterDisplayMode(dateInfo, this.message);
				},
				error: function(resp) {

				},
				scope: this
			});
		} else {
			this.enterEditMode(dateInfo, this.material);
		}
	},


	/**
	 * 响应select time view中处理完已定制消息的事件的函数
	 */
	onFinishRenderScheduledDays: function() {
		//检查当前选中日期的发布情况
		this.selectTimeView.checkCurrentDate();
	},

	/**
	 * 创建消息
	 */
	onClickSubmitButton: function() {
		W.getErrorHintView().hide();
		//确定content
		var content = null;
		if (this.type === 'text') {
			content = this.richEditer.getContent();
			if (content.length == 0) {
				W.getErrorHintView().show('文本消息不能为空');
				return;
			}
		} else {
			if (!this.material || parseInt(this.material) == 0) {
				W.getErrorHintView().show('请添加图文消息');
				return;
			} else {
				content = JSON.stringify({material: this.material});
			}
		}

		//确定send type
		var sendType = this.getSendType();

		//确定定制的发布时间
		var time = this.selectTimeView.getTime();

		if (parseInt(sendType) == 0) {
			//如果是定时发布，检查时间
			if (this.selectTimeView.isBeforeCurrentTime(time)) {
				W.getErrorHintView().show('发布时间不能早于当前时间');
				return;
			}
		}

		var date = time.split(' ')[0]

		W.getLoadingView().show();
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'masssend',
				api: 'message/create',
				method: 'post',
				args: {
					type: this.type,
					content: content,
					send_type: sendType,
					scheduled_at: time
				},
				success: function(message) {
					window.location.href = '/masssend/messages/?date=' + date;
					/*
					W.getLoadingView().hide();
					this.selectTimeView.loadScheduledDays();
					*/
				},
				error: function() {
					W.getLoadingView().hide();
				},
				scope: this
			});
		}, this);
		task.delay(200);
	},

	/**
	 * 点击删除消息按钮的响应函数
	 */
	onClickDeleteButton: function(event) {
		if (!this.message) {
			return;
		}

		event.stopPropagation();
        event.preventDefault();

        var $el = $(event.target);
        var deleteCommentView = W.getItemDeleteView();
        deleteCommentView.bind(deleteCommentView.SUBMIT_EVENT, function(options){
    		W.getApi().call({
				app: 'masssend',
				api: 'message/delete',
				args: {
					id: this.message.id
				},
				success: function() {
					deleteCommentView.hide();
					this.selectTimeView.loadScheduledDays();
                    this.trigger('finish-delete-message');
				},
				error: function() {
					W.getLoadingView().hide();
				},
				scope: this
			});
		}, this);

		deleteCommentView.show({
            $action: $el,
            info: '确定删除该条消息吗?'
        });
	}
});