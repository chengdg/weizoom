ensureNS('W.view.apps');
W.view.apps.PrizeSelector = Backbone.View.extend({
	events: {
		'change select': 'onChangeSelect',
		'input .xa-integral': 'onInputIntegral',
		'click .xa-selectCoupon': 'onClickSelectCouponLink',
		'click .xa-removeCoupon': 'onClickRemoveCoupon'
	},

	templates: {
		viewTmpl: "#apps-prize-selector-tmpl"
	},
	
	initialize: function(options) {
		this.$el = $(options.el);
		
		this.options = options || {};		
		this.prize = options.prize || {type:'no_prize', data:null};
	},
	
	render: function() {
		var html = this.renderTmpl('viewTmpl', {prize:this.prize});
		this.$el.append(html);
	},

	onChangeSelect: function(event) {
		var $select = $(event.currentTarget);
		var prizeType = $select.val();
		this.$('.xa-optionTarget').hide();
		this.$('.xa-integral').val('');
		if (prizeType === "coupon"){
			this.$('.coupon_div').show().css('display', 'inline');
			this.$('.coupon_div a').show();

		}
		else{
			this.$('[data-target="'+prizeType+'"]').show();
		}

		this.prize['type'] = prizeType;
		this.prize['data'] = null;
		this.$('.errorHint').text("");
		this.trigger('change-prize', _.deepClone(this.prize));
	},

	onInputIntegral: function(event) {
		var $input = $(event.currentTarget);
		this.prize['data'] = $input.val();
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
		this.trigger('change-prize', _.deepClone(this.prize));
	}
});

W.registerUIRole('[data-ui-role="apps-prize-selector"]', function() {
    var $el = $(this);
    var prize = $el.data('prize');
    var view = new W.view.apps.PrizeSelector({
        el: $el.get(0),
        prize: prize
    });
    view.render();

    //缓存view
    $el.data('view', view);
});