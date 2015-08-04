/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 选择时间的view
 * @constructor
 */
W.SelectTimeView = Backbone.View.extend({
	el: '',

	events: {
		'click #unreadCountHint': 'onClickUnreadCountHint'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.$datepicker = this.$("#datepicker");
		this.isSelectEnabled = true; //标识当前组件是否处于可select状态
		this.date = options.date; //当前选中的日志
		this.scheduledDays = null; //缓存已定制消息的日期

		var time = options.time;
		this.defaultHour = -1;
		this.defaultMinutes = -1;
		if (time) {
			var items = time.split(':')
			this.defaultHour = parseInt(items[0]);
			this.defaultMinutes = parseInt(items[1]);
		}
	},

	/**
	 * 初始化hour选择器的选项
	 */
	createHourSelector: function() {
		var node = $('<div>');
		for (var i = 0; i < 24; ++i) {
			node.append('<option value="' + i + '">' + i + '</option>')
		}
		this.$('select[name="hour"]').html(node.html());
	},

	/**
	 * 初始化minutes选择器的选项
	 */
	createMinutesSelector: function() {
		var node = $('<div>');
		for (var i = 0; i < 60; i+=1) {
			node.append('<option value="' + i + '">' + i + '</option>')
		}
		this.$('select[name="minutes"]').html(node.html());
	},

	render: function() {
		$('body').append('<div id="scheduledMessagesDotZone"></div>');
		this.$scheduledMessagesDotZone = $('#scheduledMessagesDotZone');

		var _this = this;
		if (!this.date) {
			var today = new Date();
			this.date = $.datepicker.formatDate('yy-mm-dd', today);
		}
		this.$datepicker.datepicker({
			buttonText: '选择日期',
			defaultDate: this.date,
			//minDate: today,
			//maxDate: '2013-06-17',
			numberOfMonths: 1,
			dateFormat: 'yy-mm-dd',
			closeText: '确定',
			prevText: '&#x3c;上月',
			nextText: '下月&#x3e;',
			monthNames: ['一月','二月','三月','四月','五月','六月',
			'七月','八月','九月','十月','十一月','十二月'],
			monthNamesShort: ['一','二','三','四','五','六',
			'七','八','九','十','十一','十二'],
			dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
			dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
			dayNamesMin: ['日','一','二','三','四','五','六'],
			onSelect: function(date) {
				_this.date = date;

				//判断是否选择了已定制的day
				_this.checkCurrentDate();
			},
			onChangeMonthYear: function(year, month, instance) {
				_this.scheduledDays = null; //清空缓存数据
				_this.loadScheduledDays(month);
			}
		});

		this.createHourSelector();
		this.createMinutesSelector();
		this.$('select[name="hour"]').val(this.defaultHour);
		this.$('select[name="minutes"]').val(this.defaultMinutes);

		this.loadScheduledDays();

		return this;
	},

	/**
	 * 将日期时间设置到当前时间，并关闭select功能
	 */
	setToNow: function() {
		var date = new Date();
		
		//设置datepicker
		var dateStr = $.datepicker.formatDate('yy-mm-dd', date);
		this.$datepicker.datepicker('setDate', dateStr);
		this.fixToTime(date.getHours(), date.getMinutes());
	},

	/**
	 * 固定hour和minutes
	 */
	fixToTime: function(hour, minutes) {
			//设置hour selector
			this.$('select[name="hour"]').val(hour);
			
			//设置minutes selector
			this.$('select[name="minutes"]').val(minutes);
			
			this.disableSelect();
	},

	/**
	 * 禁用select功能
	 */
	disableSelect: function() {
		if (this.isSelectEnabled) {
			//this.$datepicker.datepicker( "option", "disabled", true);
			this.$('select[name="hour"]').attr('disabled', 'disabled');
			this.$('select[name="minutes"]').attr('disabled', 'disabled');
			this.isSelectEnabled = false;
		}
	},

	/**
	 * 启用select功能
	 */
	enableSelect: function() {
		if (!this.isSelectEnabled) {
			//this.$datepicker.datepicker( "option", "disabled", false);
			this.$('select[name="hour"]').removeAttr('disabled');
			this.$('select[name="minutes"]').removeAttr('disabled');
			this.isSelectEnabled = true;
		}
	},

	/**
	 * 获得当前选择的时间，格式为: 2012-05-01 14:01:00
	 */
	getTime: function() {
		var hour = this.$('select[name="hour"]').val();
		if (hour.length == 1) {
			hour = '0'+hour;
		}

		var minutes = this.$('select[name="minutes"]').val();
		if (minutes.length == 1) {
			minutes = '0'+minutes;
		}

		return this.date + ' ' + hour + ':' + minutes + ':00';
	},

	/**
	 * 获得当前选中的month
	 */
	getMonth: function() {
		var date = this.$datepicker.datepicker("getDate");
		return date.getMonth()+1;
	},

	/**
	 * 获得当前选中的day
	 */
	getDay: function() {
		var date = this.$datepicker.datepicker("getDate");
		return date.getDate();
	},

	/**
	 * 加载已定制消息的日期列表
	 */
	loadScheduledDays: function(month) {
		//清除已经存在的定制消息
		this.$scheduledMessagesDotZone.hide().html('');
		this.scheduledDays = null;

		//获取已经发送的消息列表
		if (!month) {
			month = this.getMonth();
		}
		W.getApi().call({
			app: 'masssend',
			api: 'scheduled_infos/get',
			args: {
				month: month
			},
			success: function(data) {
				this.renderScheduledDays(data.items);
				this.trigger('finish-render-scheduled-days');
			},
			error: function(resp) {

			},
			scope: this
		});
	},

	/**
	 * 在日历中渲染已定制消息的日期
	 */
	renderScheduledDays: function(messages) {
		var _this = this;
		if (!messages || messages.length == 0) {
			if (this.scheduledDays == null) {
				xlog('empty messages, return directly');
				return;
			} else {
				//有有效的scheduledDays，需要刷新页面
			}
		}

		//更新scheduledDays
		if (this.scheduledDays == null) {
			this.scheduledDays = {};
			_.each(messages, function(message) {
				_this.scheduledDays[message.scheduled_day] = message;
			});
		}

		//向日历中添加图片
		this.$('td a').each(function() {
			var link = $(this);
			var day = parseInt($.trim(link.text()));
			var message = _this.scheduledDays[day];
			if (message) {
				var offset = link.offset();
				var top = parseInt(offset.top);
				var left = parseInt(offset.left);
				var width = parseInt(link.width());
				var height = parseInt(link.height());

				var imgLeft = left+width-8;
				var imgTop = top+height+1;

				var imageName = null;
				if (message.type == '图文消息') {
					imageName = 'red_dot.gif';
				} else {
					imageName = 'blue_dot.gif';
				}
				_this.$scheduledMessagesDotZone.append('<img src="/static/img/'+imageName+'" style="position: absolute; top: '+imgTop+'px; left: '+imgLeft+'px; width: 6px">');
			}
		});

		this.$scheduledMessagesDotZone.show();
	},

	/**
	 * 检查当前日期，激发相应event
	 */
	checkCurrentDate: function() {
		var day = this.getDay();
		var date = this.$datepicker.datepicker("getDate");
		var dateStr = $.datepicker.formatDate('yy-mm-dd', date);
		var isScheduled = false;
		if (this.scheduledDays && this.scheduledDays[day]) {
			isScheduled = true;
		} 

		//判断是不是今天
		var isToday = false;
		var today = new Date();
		var todayStr = $.datepicker.formatDate('yy-mm-dd', today);
		if (todayStr === dateStr) {
			isToday = true;
		}

		//判断是不是历史日期
		var isHistory = false;
		if (todayStr > dateStr) {
			isHistory = true;
		}

		this.trigger('select-date', {
			isScheduled: isScheduled,
			isToday: isToday,
			isHistory: isHistory, 
			date: dateStr
		});
	},

	/**
	 * 判断指定时间是否小于当前时间
	 */
	isBeforeCurrentTime: function(datetime) {
		var items = datetime.split(' ');
		var date = items[0];
		var time = items[1];

		var today = new Date();
		var todayStr = $.datepicker.formatDate('yy-mm-dd', today);
		if (date != todayStr) {
			return false;
		}
		else {
			var items = time.split(':');
			var hours = parseInt(items[0]);
			var minutes = parseInt(items[1]);
			if (today.getHours() == hours) {
				if (today.getMinutes() > minutes) {
					return true;
				} else {
					return false;
				}
			} else {
				if (today.getHours() > hours) {
					return true;
				} else {
					return false;
				}
			}
		}
	}
});