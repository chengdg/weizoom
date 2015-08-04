/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * <input data-ui-role="orderCount" type="hidden" name="total_count" id="total_count" value="{{order.number}}" total_price_element=".tx_price" item_price="{{ product.price }}" total_postage_price="{{ product.postage }}" item_postage_price="{{ product.postage }}">
 * value--下订数量
 * item_price--单个商品价格
 * item_price_element--显示单个商品价格的容器
 * item_postage_price--单个商品运费(item_postage_price与total_postage_price只能选一个)
 * total_postage_price--所有商品运费(item_postage_price与total_postage_price只能选一个)
 * total_price_element--显示所有商品总价格的容器
 * author: tianyanrong
 */
(function($, undefined) {
    
    CountPanelView = function(options) {
        this.$el =  options.$el;
        if(!this.$el.val()) {
            this.$el.val(1);
        };
        
        this.initialize();
        this.bindEvents();
    };
    CountPanelView.prototype = {
        template: function(count) {
            return '<a href="javascript:void(0);" class="ui-books-btn-down tx_down">-</a>'
                    +'<span class="ui-books-text tx_value"></span>'
                    +'<a href="javascript:void(0);" class="ui-books-btn-up tx_up">+</a></div>';
        },
        initialize: function(count) {
            this.$el.wrap('<div class="booksCountPanel ui-books-count-group"></div>');
            this.$parent = this.$el.parent('.booksCountPanel');
            this.$parent.append(this.template());
            this.count = this.$el.val() || 1;
            this.setDefaultValue();
            this.setPrise();
        },
        setDefaultValue: function() {
            this.$parent.find('.tx_value').text(this.count);
        },
        bindEvents: function() {
            var _this = this;
            this.$parent.delegate('.tx_down', 'click', function(event) {
                _this.changeCount(event, false);
            });
            this.$parent.delegate('.tx_up', 'click', function(event) {
                _this.changeCount(event, true);
            });
        },
        setPrise: function() {
            var items = [];
            var $el = $('body').find('[data-ui-role="orderCount"]');
            var $totalPrice;
            var totalPrice = 0;
            var postagePrice = 0;
            $el.each(function() {
                var count = parseFloat($(this).parent().find('.tx_value').text(), 10);
                var prise = parseFloat($(this).attr('item_price'), 10);
                var itemPostagePrice = parseFloat($(this).attr('item_postage_price'), 10);
                var price = (count * prise);
                price = itemPostagePrice ? (price + itemPostagePrice) : price;
                var $itemPrice = $($(this).attr('item_price_element'));
                $itemPrice.text(price.toFixed(2));
                
                $totalPrice = $($(this).attr('total_price_element'));
                postagePrice = parseFloat($(this).attr('total_postage_price'), 10) || postagePrice;
                totalPrice += price;
            });
            $totalPrice.text((postagePrice+totalPrice).toFixed(2));
        },
        changeCount: function(event, isUp) {
            this.$value = this.$parent.find('.tx_value');
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
            this.$el.val(value);
            this.setPrise();
        }
    };

	// component definition
	$.widget("mobile.orderCount", $.mobile.widget, {
		_create : function() {
            this._bind();
			this.$input = this.element;
            this.orderCount = new CountPanelView({
                $el: this.$input
            })
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
		$(":jqmData(ui-role=orderCount)", e.target).orderCount();
	});
    
})(jQuery);
