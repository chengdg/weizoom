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
            return '<span class="wa-down wui-down" style="border-right:0;border-radius:2px 0 0 2px;">-</span>'
                    +'<span class="wui-counterText"></span>'
                    +'<span class="wa-up wui-up" style="border-left:0;border-radius:0 2px 2px 0;">+</span>'
                    +'<div class="wui-limit wa-limit"></div>';
        },

        initialize: function(count) {
            this.$el.wrap('<div class="wui-counter"></div>');
            this.$parent = this.$el.parent('.wui-counter');
            this.$parent.append(this.template());
            this.count = parseInt(this.$el.val() || 1);
            this.minCount = this.$el.data('minlimit');
            if(this.minCount <= 1){
                this.minCount = 1;
            }else{
                this.$parent.find('.wa-limit').html('至少购买'+this.minCount+'件');
            }
            if(this.count < this.minCount){
                this.count = this.minCount;
                this.$el.siblings('.wa-down').css('border-color','#e5e5e5');
            }
            this.maxCount = parseInt(this.$el.attr('data-max-count') || -99999);
            if(this.count == this.maxCount){
                this.$el.siblings('.wa-up').css('border-color','#e5e5e5');
            }
            this.$textValue = this.$parent.find('.wui-counterText');
            this.$textValue.text(this.count);

            this.isEnable = true;
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
            var $up = this.$el.siblings('.wa-up');
            var $down = this.$el.siblings('.wa-down');

            if (!this.isEnable) {
                //被禁用，直接返回
                this.$el.trigger('click-disabledCounter', this.count);
                return;
            }
            if (this.maxCount === 0) {
                return;
            }
            if (this.maxCount > 0) {
                if((this.count >= this.maxCount && delta > 0) || (this.maxCount < this.minCount)) {
                    //不能超过最大数量
                    this.$el.trigger('reach-max-count', this.maxCount);
                    return;
                }
            }
            if (this.count === this.minCount && delta < 0) {
                return;
            }
            this.count = this.count + delta;
            if (this.count < 0) {
                this.count = 0;
            }

            var disableColor = '#e5e5e5';
            var enableColor = '#ccc';
            var upColor = enableColor;
            var downColor = enableColor;
            if (this.count === 0) {
                upColor = disableColor;
                downColor = disableColor;
            }
            else if(this.count === 1){
                downColor = disableColor;
            }
            $up.css('border-color', upColor);
            $down.css('border-color', downColor);

            this.$textValue.text(this.count);
            this.$el.val(this.count);
            this.$el.trigger('count-changed', this.count);

            var borderColor = '#ccc';

            if(this.count == this.maxCount){
                borderColor = "#e5e5e5";
            }

            this.$el.siblings('.wa-up').css('border-color', borderColor);
            return this;
        },

        changeCountTo: function(count) {
            var delta = count - this.count;
            // xlog('change delta is ' + delta);
            this.changeCount(delta);
            return this;
        },

        reset: function() {
            this.count = this.minCount;
            if(this.count<this.maxCount || this.maxCount<-1){
                this.changeCountTo(this.count);
            }
            return this;
        },

        setMaxCount: function(count) {
            console.log('setMaxCount', count);
            this.maxCount = parseInt(count);

            if (this.maxCount === 0) {
                this.count = 0;
                this.$textValue.text(this.count);
                this.$el.val(this.count);
                this.$el.siblings('.wa-up,.wa-down').css('border-color', '#e5e5e5');
            } else {
                if (this.count >= this.maxCount && this.maxCount > 0) {
                    xlog('change to ' + this.maxCount);
                    this.changeCountTo(this.maxCount);
                }else if (this.count <= 1) {
                    xlog('change to ' + 1);
                    this.changeCountTo(1);
                }
                if (this.maxCount < this.minCount) {
                    this.$el.trigger('reach-max-count', this.maxCount);
                }
            }
            return this;
        },

        enable: function() {
            this.isEnable = true;
            return this;
        },

        disable: function() {
            xlog('disable counter');
            this.isEnable = false;
            return this;
        }
    };

    gmu.define('Counter', {
        _init: function() {
        },

        _create: function() {
            xlog(this.$el);
            this.counter = new CounterView({
                $el: this.$el
            });
            this.$el.data('view', this.counter);
        }

    })

	// taking into account of the component when creating the window
	// or at the create event
    /*
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=counter)", e.target).counter();
	});
    */
    $(function() {
        $('[data-ui-role="counter"]').counter();
    })

})(Zepto);
