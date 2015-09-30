ensureNS('W.view.apps');
W.view.apps.PrizeSelectorV4 = Backbone.View.extend({
	events: {
		'click .xa-selectCoupon': 'onClickSelectCouponLink',
		'click .xa-removeCoupon': 'onClickRemoveCoupon',
		'click .xa-changCouponCount':'onChangeCouponCount'
	},

	templates: {
		viewTmpl: "#apps-prize-selector-v4-tmpl"
	},
	
	initialize: function(options) {
		this.$el = $(options.el);
		
		this.options = options || {};		
		this.prize = options.prize || {id:0, name:''};
		//this.trigger('change-prize', _.deepClone(this.prize));//keep
	},
	
	render: function() {
		var html = this.renderTmpl('viewTmpl', {prize:this.prize});
		this.$el.append(html);
	},

	onClickSelectCouponLink: function(event) {
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectCouponDialog', {
			success: function(data) {
				var coupon = data[0];
				_this.prize= {
					id: coupon.id,
					name: coupon.name,
					count:coupon.count
				};
				xwarn(_this.prize);
				_this.$el.find('.xa-couponName').text(coupon.name);
				_this.$el.find('.xa-selectedCoupon').removeClass('xui-hide');
				_this.$el.find('.coupon_div').addClass('xui-hide');
				_this.$el.find('.xa-couponCount').text(coupon.count);

				_this.trigger('change-prize', _.deepClone(_this.prize));

			}
		});
	},
	onChangeCouponCount:function(event){
		//修改库存的handler
	},
	onClickRemoveCoupon: function(event) {
		this.$el.find('.xa-optionTarget').addClass('xui-hide');
		this.$el.find('.xa-selectCoupon').removeClass('xui-hide');
		//this.$('.coupon_div').css('display', 'inline');
		this.prize = {id:0, name:'',count:0};
		this.trigger('change-prize', _.deepClone(this.prize));//keep
		console.log(this.prize);
	}
});

W.registerUIRole('[data-ui-role="apps-prize-selector-v4"]', function() {
    var $el = $(this);
	var prize = $el.data('prize');
	console.log('!!!!!!!!!!!!!!');
	console.log(prize);
    var view = new W.view.apps.PrizeSelectorV4({
        el: $el.get(0),
		prize: prize
    });
    view.render();

    //缓存view
    $el.data('view', view);
});