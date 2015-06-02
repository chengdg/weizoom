/**
 * 数值加减的组件
 * change: 对当前DOM对像触发的事件(当数值发生变化后，发触发此事件)
*/
W.CountPanelView = function(options) {
	this.$el =  $(options.el);
    this.count = options.count
	this.initialize();
	this.bindEvents();
};
W.CountPanelView.prototype = {
	template: function(count) {
		return '<a href="javascript:void(0);" class="ui-books-btn-down tx_down">-</a>'
				+'<span class="ui-books-text tx_value"></span>'
				+'<a href="javascript:void(0);" class="ui-books-btn-up tx_up">+</a>';
	},
	initialize: function(count) {
		this.$el.addClass('ui-books-count-group');
		this.$el.html(this.template());
        this.setDefaultValue();
        this.$el.trigger('complete', this.getValue());
	},
    setDefaultValue: function() {
        if(this.count) {
            this.$el.find('.tx_value').text(this.count);
        }
        else {
            this.$el.each(function() {
                $(this).find('.tx_value').text($(this).attr('order_count'));
            })
        }
    },
	bindEvents: function() {
		var _this = this;
		this.$el.delegate('.tx_down', 'click', function(event) {
			_this.changeCount(event, false);
		});
		this.$el.delegate('.tx_up', 'click', function(event) {
			_this.changeCount(event, true);
		});
	},
    getValue: function() {
        var items = [];
        this.$el.each(function() {
            if($('body').find(this).length) {
                var data = {};
                data.count = parseFloat($(this).find('.tx_value').text(), 10);
                data.prise = parseFloat($(this).attr('defalut_value'), 10);
                data.id = $(this).attr('item_id');
                items.push(data);
            }
        });
        return {data:items};
    },
    update: function() {
        this.$el.trigger('complete', this.getValue());
    },
	changeCount: function(event, isUp) {
        this.$value = $(event.currentTarget).parents('.ui-books-count-group').find('.tx_value');
		var value = parseFloat(this.$value.text(), 10) || 1;
		if(isUp) {
			value++;
		}
		else {
			value--;
		}
		if(value <= 0) {
			value = 1;
		}
		this.$value.text(value);
		this.$el.trigger('change', value);
        this.$el.trigger('complete', this.getValue());
	}
};