ensureNS('W.view.apps');
W.view.apps.PrizeSelectorV5 = Backbone.View.extend({
	events: {
		'click .xa-selectCoupon': 'onClickSelectCouponLink',
		'click .xa-addselectCoupon': 'onClickSelectCouponLink',
		'click .xa-removeCoupon': 'onClickRemoveCoupon',
		'click .xa-changCouponCount':'onChangeCouponCount',
		'click .xa-changeMemberGrade': 'onChangeMemberGrade',
		'click .xa-changeSelectCoupon': 'onChangeSelectCoupon'
	},

	templates: {
		viewTmpl: "#apps-prize-selector-v5-tmpl",
		viewCoupon: "#apps-coupon-v5-tmpl"
	},
	
	initialize: function(options) {
		this.$el = $(options.el);

		this.options = options || {};
		this.prizes = options.prizes || [];
		//this.trigger('change-prize', _.deepClone(this.prize));//keep
	},
	
	render: function() {
		var _this = this;
		W.getApi().call({
			app: 'apps/exsign',
			resource: 'member_grade_list',
			method: 'get',
			args: {},
			success: function(data) {
				_this.member_grades = data;
				var html = _this.renderTmpl('viewTmpl', {prizes:_this.prizes,member_grades:_this.member_grades});
				_this.$el.append(html);
			},
			error: function(resp) {
			  W.showHint('error', '失败!');
			}
		});
	},

	onClickSelectCouponLink: function(event) {
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectCouponDialog', {
			success: function(data) {
				var coupon = data[0];
				var prize = {
					id: coupon.id,
					name: coupon.name,
					count: coupon.count,
					grade_id: -1,
					grade_name: "全部"
				};
				_this.prizes.push(prize);
				xwarn(_this.prizes);
				var html = _this.renderTmpl('viewCoupon', {prize:prize,member_grades:_this.member_grades});
				_this.$el.find('.xui-apps-prizeSelector').append(html);
				_this.$el.find('.xa-selectedCoupon').removeClass('xui-hide');
				_this.$el.find('.xa-addselectCoupon').removeClass('xui-hide');
				_this.$el.find('.coupon_div').addClass('xui-hide');

				_this.trigger('change-prize', _.deepClone(_this.prizes));

			}
		});
	},
	onChangeSelectCoupon: function(event){
		var $changeCoupon = $(event.target);
		var index = this.$el.find('.xa-selectedCoupon').index($changeCoupon.parents('.xa-selectedCoupon'));
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectCouponDialog', {
			success: function(data) {
				var coupon = data[0];
				_this.prizes[index]["id"] =coupon.id;
				_this.prizes[index]["name"] =coupon.name;
				_this.prizes[index]["count"] =coupon.count;
				xwarn(_this.prizes);
				$changeCoupon.parents('.xa-selectedCoupon').find('.xa-couponName').text(coupon.name);
				$changeCoupon.parents('.xa-selectedCoupon').find('.xa-couponCount').text(coupon.count);
				$changeCoupon.parents('.xa-selectedCoupon').find('.xa-changeCouponCount').attr('href','/mall2/coupon/?rule_id='+coupon.id);
				_this.trigger('change-prize', _.deepClone(_this.prizes));

			}
		});

	},
	onChangeCouponCount:function(event){
		//修改库存的handler
	},
	onClickRemoveCoupon: function(event) {
		var $coupon = $(event.target);
		var index = this.$el.find('.xa-selectedCoupon').index($coupon.parents('.xa-selectedCoupon'));
		$coupon.parents('.xa-selectedCoupon').remove();
		if (!$('.xa-selectedCoupon').length){
			this.$el.find('.xa-selectCoupon').removeClass('xui-hide');
			this.$el.find('.xa-addselectCoupon').addClass('xui-hide');
		}
		this.prizes.splice(index,1);
		this.trigger('change-prize', _.deepClone(this.prizes));//keep
	},
	onChangeMemberGrade: function(event){
		var $selectGrade = $(event.currentTarget);
		var index = this.$el.find('.xa-selectedCoupon').index($selectGrade.parents('.xa-selectedCoupon'));
		var grade_id = $selectGrade.attr('value');
		this.prizes[index]["grade_id"] = grade_id;
		var member_grades = this.member_grades;
		var grade_name = "全部";
		for (var i in member_grades){
			if (member_grades[i].id == grade_id){
				grade_name = member_grades[i].name
			}
		}
		this.prizes[index]["grade_name"] = grade_name;
		this.trigger('change-prize', _.deepClone(this.prizes));
	}
});

W.registerUIRole('[data-ui-role="apps-prize-selector-v5"]', function() {
    var $el = $(this);
	var prizes = $el.data('prizes');
	console.log(prizes,"dddddddddddddddd")
	var view;

		view = new W.view.apps.PrizeSelectorV5({
			el: $el.get(0),
			prizes: prizes
		});
		view.render();
		//缓存view
		$el.data('view', view);
});