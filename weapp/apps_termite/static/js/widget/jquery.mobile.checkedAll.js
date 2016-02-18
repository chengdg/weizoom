/*
 * Jquery Mobile地址选择插件
 * 
 *
 * 使用示例;
 * author: tianyanrong
 */
(function($, undefined) {
    CheckAllView = function(options) {
        this.$el = options.$el;
        this.bindEvents();
    }
    CheckAllView.prototype = {
        bindEvents: function() {
            var _this = this;
            this.$el.delegate('.tx_check', 'change', function(event) {
                _this.setChecked();
                _this.updatePrice(event);
            });
            this.$el.delegate('.tx_checks_btn', 'touchstart', function(event) {
                _this.setAllChecked();
            });
            this.$el.delegate('.tx_checks_btn', 'click', function(event) {
                _this.setAllChecked();
            });
        },
        
        updatePrice: function(event, isChecked) {
            var $parent;
            if(!event) {
                $parent = $('body');
            }
            else {
                var $el = $(event.currentTarget);
                $parent = $el.parents('[item_id]');
                isChecked = event.target.checked;
            }
            
            $parent.find('[data-ui-role="orderCount"]').trigger('status-event', !isChecked);
        },
        
        setChecked: function() {
            var isAllChecked = true;
            $('.tx_check').each(function() {
                if(!this.checked) {
                    isAllChecked = false;
                }
            });
            $('.tx_checks').prop( "checked", isAllChecked).checkboxradio("refresh");
        },
        
        setAllChecked: function() {
            var isChecked =  $('.tx_checks')[0].checked;
            $('.tx_check').prop( "checked", !isChecked).checkboxradio("refresh");
            this.updatePrice(null, !isChecked);
        }
    }
    

	// taking into account of the component when creating the window
	// or at the create event
	$(document).bind("pagecreate create", function(e) {
		$(":jqmData(ui-role=checkedAll)", e.target).each(function() {
            new CheckAllView({
                $el: $(this)
            })
        })
	});
    
})(jQuery);
