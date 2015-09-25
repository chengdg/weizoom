ensureNS('W.view.apps');
W.view.apps.PrizeSelectorV4 = Backbone.View.extend({
	events: {
		'click .xa-selectCoupon': 'onClickSelectCouponLink',
		'click .xa-removeCoupon': 'onClickRemoveCoupon',
	},

	templates: {
		viewTmpl: "#apps-prize-selector-v4-tmpl"
	},
	
	initialize: function(options) {
		this.$el = $(options.el);
		
		this.options = options || {};		
		this.prize = options.prize || {type:'coupon', data:null};
		this.prize['type'] = 'coupon';
		this.prize['data'] = {id:0, name:''};
		this.trigger('change-prize', _.deepClone(this.prize));//keep
	},
	
	render: function() {
		var html = this.renderTmpl('viewTmpl', {prize:this.prize});
		this.$el.append(html);
	},

	onChangeSelect: function(event) {
		var $select = $(event.currentTarget);
		var prizeType = $select.val();
		this.$('.xui-apps-prizeSelector').removeClass('has_error');
		this.$('.xa-optionTarget').hide();
		this.$('.errorHint').hide();
		this.$('.xa-entity').val('');
		this.$('[data-target="'+prizeType+'"]').show().css('display','inline');

		this.prize['type'] = prizeType;
		this.prize['data'] = null;
		this.trigger('change-prize', _.deepClone(this.prize));
	},

	onClickSelectCouponLink: function(event) {
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectCouponDialog', {
			success: function(data) {
				var coupon = data[0];
				_this.prize['type'] = 'coupon';
				_this.prize['data'] = {
					id: coupon.id,
					name: coupon.name
				};
				xwarn(_this.prize);

				_this.$el.find('.xa-couponName').text(coupon.name);
				_this.$el.find('.xa-optionTarget').hide();
				_this.$el.find('.xa-selectedCoupon').show().css('display', 'inline');

				_this.trigger('change-prize', _.deepClone(_this.prize));
			}
		});
	},

	onClickRemoveCoupon: function(event) {
		this.$el.find('.xa-optionTarget').hide();
		this.$el.find('.xa-selectCoupon').show();
		this.$('.coupon_div').css('display', 'inline');
		this.prize['type'] = 'coupon';
		this.prize['data'] = {id:0, name:''};
		this.trigger('change-prize', _.deepClone(this.prize));//keep
	}
});

W.registerUIRole('[data-ui-role="apps-prize-selector-v4"]', function() {
    var $el = $(this);
    var view = new W.view.apps.PrizeSelectorV4({
        el: $el.get(0),
    });
    view.render();

    //缓存view
    $el.data('view', view);
});