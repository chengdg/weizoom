/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 选择日期的View
 */
W.common.SelectDateView = Backbone.View.extend({
	el: '',

	events: {
		'click a.wx_changeDate': 'onClickChangeDateLink',
		'click #dateSelector-dropBox': 'onClickDropBox',
		'click button.wx-dateSelector-customTime-submit': 'onClickSubmitButton'
	},
	
	/*
	getTemplate: function() {
		$('#date-selector-custom-time-tmpl-src').template('date-selector-custom-time-tmpl-src');
        return 'date-selector-custom-time-tmpl-src';
	},
	*/

	initialize: function(options) {
		this.$el = $(this.el);
		//this.tmpl = this.getTemplate();

		var date = new Date();
		date.setDate(date.getDate() - 1);
		this.customEndTime = $.datepicker.formatDate('yy-mm-dd', date);
		this.$endTime = this.$('input[name="endTime"]');
		this.$endTime.val(this.customEndTime);

		date.setDate(date.getDate() - 6);
		this.customStartTime = $.datepicker.formatDate('yy-mm-dd', date);
		this.$startTime = this.$('input[name="startTime"]');
		this.$startTime.val(this.customStartTime);

		this.createDatepicker();
	},

	/**
	 * 创建datepicker
	 */
	createDatepicker: function() {
		//添加date selector
		$('body').append('<div id="dateSelector-datepicker" style="position: absolute; display: none; z-index: 1000;"></div>')
		var $datepicker = $('#dateSelector-datepicker');
		this.$datepicker = $datepicker;
		var date = new Date();
		date.setDate(date.getDate() - 1);
		$datepicker.datepicker({
			buttonText: '选择日期',
			/*defaultDate: this.date,*/
			maxDate: date,
			numberOfMonths: 1,
			dateFormat: 'yy-mm-dd',
			closeText: '关闭',
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
				$datepicker.hide();
				var $input = $datepicker.data('$input');
				$input.val(date);
			}
		});
		$datepicker.click(function(event) {
			event.stopPropagation();
		});
		$('.wx-datepicker').click(function(event) {
			event.stopPropagation();
		});

		//显示datepicker
		$('.wx-datepicker').focus(function(event) {
			if ($datepicker.is(":visible")) {
				$datepicker.hide();
			}

			//更换$input
			$datepicker.removeData('$input');
			$datepicker.data('$input', $(this));

			var $input = $(event.currentTarget);
			var offset = $input.offset();
			var height = $input.outerHeight();
			$datepicker.css({
				top: offset.top + height + 1,
				left: offset.left
			}).show();
		});

		//点击其他任意位置，隐藏datepicker
		$(document).click(function(event) {
			if ($datepicker.is(":visible")) {
				$datepicker.hide();
			}
		});
	},

	render: function() {
		//$('body').append($.tmpl(this.tmpl));
	},

	onClickChangeDateLink: function(event) {
		var $link = $(event.target);
		var days = $link.attr('data-days');

		//切换active li
		this.$('li.active').removeClass('active');
		$link.parent().addClass('active');

		this.trigger('change-days', days);
	},

	onClickSetCustomTimeLink: function(event) {
		xlog($(event.target));
		xlog($(event.currentTarget));
		var $link = $(event.currentTarget);
		var offset = $link.offset();
		var height = $link.outerHeight() + 5;

		//显示选择日期
		$('#dateSelector-dropBox').css({
			left: offset.left + 'px',
			top: offset.top + height + 'px'
		}).show();

		//this.trigger('change-days', days);
	},

	onClickDropBox: function(event) {
		event.stopPropagation();
	},

	onClickSubmitButton: function(event) {
		var startTime = this.$startTime.val();
		var endTime = this.$endTime.val();
		xlog(startTime);
		xlog(endTime);
		if (endTime < startTime) {
			this.$('div.errorHint').text('结束日期不能小于开始日期').show();
			return;
		}

		this.$('div.errorHint').hide();
		var $dropdown = this.$('.dropdown-toggle');
		$dropdown.dropdown('toggle');
		this.$('li.active').removeClass('active');
		$dropdown.parent().addClass('active');

		if (this.$datepicker.is(":visible")) {
			this.$datepicker.hide();
		}

		var days = startTime+'~'+endTime;
		$('span.wx-textTime').text(days);
		this.trigger('change-days', days);
	}
});