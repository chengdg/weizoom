/*
 * Jquery Mobile数量调节器插件
 * 
 *
 * 使用示例;
 * <input data-ui-role="orderCount" type="hidden" name="total_count" id="total_count" value="{{order.number}}" total_price_element=".tx_price" item_price="{{ product.price }}" total_postage_price="{{ product.postage }}" item_postage_price="{{ product.postage }}">
 * value--数量
 *
 * count-changed: count变化后激发的事件
 */
(function($, undefined) {
    CounterView = function(options) {
        this.$el = options.$el;
        this.count = this.$el.val() || 1;

        this.initialize();
    };
    CounterView.prototype = {
        template: function(count) {
            return '<a href="javascript:void(0);" class="wa-down">-</a>'
                    +'<span class="wui-counterText"></span>'
                    +'<a href="javascript:void(0);" class="wa-up">+</a></div>';
        },

        initialize: function(count) {
            this.$el.wrap('<div class="wui-counter"></div>');
            this.$parent = this.$el.parent('.wui-counter');
            this.$parent.append(this.template());
            this.count = parseInt(this.$el.val() || 1);
            if(this.count === 1){
                $('.wa-down').css('color','#d1d1d1');
            }
            this.maxCount = parseInt(this.$el.attr('data-max-count') || -1);

            this.$textValue = this.$parent.find('.wui-counterText');
            this.$textValue.text(this.count);

            this.bindEvents();
        },

        /**
         * bindEvents: 绑定向上（向下）按钮的click事件的响应函数
         */
        bindEvents: function() {
            var _this = this;
            this.$parent.delegate('.wa-down', 'click', function(event) {
                _this.changeCount(-1);
            });
            this.$parent.delegate('.wa-up', 'click', function(event) {
                _this.changeCount(1);
            });
        },

        /**
         * changeCount: 将count增加delta指定的数量
         */
        changeCount: function(delta) {
            if (this.maxCount > 0) {
                if(this.count >= this.maxCount && delta > 0) {
                    //不能超过最大数量
                    return;
                }
            }

            this.count = this.count + delta;
            if (this.count <= 0) {
                this.count = 1;
            }
            if(this.count === 1){
                $('.wa-down').css('color','#d1d1d1');
            }else{
                $('.wa-down').css('color','#727272');
            }

            this.$textValue.text(this.count);
            this.$el.val(this.count);
            this.$el.trigger('count-changed', this.count);
        },

        changeCountTo: function(count) {
            
        },

        setMaxCount: function(count) {
            this.maxCount = count;

            if (this.count > this.maxCount) {
                this.count = this.maxCount;
                if (this.count <= 0) {
                    this.count = 1;
                }            
                this.$textValue.text(this.count);
                this.$el.val(this.count);
                this.$el.trigger('count-changed', this.count);
            }
        }
    };

	// component definition
	$.widget("mobile.counter", $.mobile.widget, {
		_create : function() {
            this._bind();
			this.$input = this.element;
            this.counter = new CounterView({
                $el: this.$input
            });
            //TODO: use widget builtin function
            this.$input.data('view', this.counter);
        },

		_bind : function() {
		},
		
		_unbind : function() {
		},
		
		destroy : function() {
			// Unbind any events that were bound at _create
			this._unbind();

			this.options = null;
		}
	});

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=counter)", e.target).counter();
	});
    
})(jQuery);
