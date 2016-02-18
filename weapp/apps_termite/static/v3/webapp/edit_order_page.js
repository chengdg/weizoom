/**
 * Backbone View in Mobile
 */
(function() {

/**
 * 运费计算器
 * 1. 计算统一运费商品的运费
 * 2. 剩下的商品使用系统运费模板
 */
var PostageCalculator = BackboneLite.View.extend({
	initialize: function(options) {
		this.postageFactor = options.postageFactor;
	},

	/**
	 * 判断商品集合是否满足包邮条件
	 */
	satisfyFreePostageCondition: function(products) {
		var totalPrice = 0.0;
		var totalCount = 0;
		for (var i = 0; i < products.length; ++i) {
			var product = products[i];
			totalPrice += product.original_price * product.count;
			totalCount += product.count;
		}

		// 包邮条件
		if (this.postageFactor.free_factor) {
			var freeFactors = this.postageFactor.free_factor[this.provinceId]
			if (freeFactors) {
				for (var i = 0; i < freeFactors.length; ++i) {
					var freeFactor = freeFactors[i];
					if(freeFactor){
						// 满钱数包邮
						if (freeFactor['condition'] == "money" && freeFactor['condition_value'] <= totalPrice) {
							return true;
						}
						// 满件数包邮
						if (freeFactor['condition'] == "count" && freeFactor['condition_value'] <= totalCount) {
							return true
						}
					}
				}
			}
		}

		return false;
	},

	/**
	 * getProductPostageForWeight: 计算weight在使用postageFactor时的运费
	 */
	getPostageForWeight: function(weight, postageFactor) {
		if (weight == 0){
			return 0.0;
		}

		if (postageFactor.firstWeight == 0 && (postageFactor.addedWeight == 0 || postageFactor.addedWeight == undefined)) {
			// 免运费
			return 0.0;
		}

		if (weight <= postageFactor.firstWeight) {
			return postageFactor.firstWeightPrice;
		}

		weight = weight - postageFactor.firstWeight;
		var price = postageFactor.firstWeightPrice;
		var addedWeight = parseFloat(postageFactor.addedWeight);

		if (addedWeight == 0) {
			return price;
		}

		var addedCount = 1;
		while (true) {
			weight = weight - addedWeight;
			if (weight <= 0) {
				break;
			} else {
				addedCount += 1;
			}
		}
		var addedPrice = addedCount * postageFactor.addedWeightPrice;
		return price + addedPrice;
	},

	getPostage: function(products, provinceId){
		// 获取地区ID
		this.provinceId = provinceId;

		var unifiedPostageMoney = 0.0;
		var unifiedPostageMoney_id = []
		var postageTemplateMoney = 0.0;
		var productsUseTemplate = [];
		var weight = 0.0;
		for (var i = 0; i < products.length; i++) {
			product = products[i];
			if (product.postageConfig.id === -1) {
				//商品使用统一运费
				if($.inArray(product.id, unifiedPostageMoney_id) === -1){
					unifiedPostageMoney += product.postageConfig.money;
					unifiedPostageMoney_id.push(product.id)
				}
			} else {
				//商品使用运费模板
				productsUseTemplate.push(product);
				weight += product.weight * product.count;
			}
		}

		if (this.postageFactor && !this.satisfyFreePostageCondition(productsUseTemplate)) {
			var specialPostageFactor = this.postageFactor.special_factor[this.provinceId];
			if (specialPostageFactor) {
				postageTemplateMoney = this.getPostageForWeight(weight, specialPostageFactor);
			} else {
				postageTemplateMoney = this.getPostageForWeight(weight, this.postageFactor);
			}
		}

		return unifiedPostageMoney + postageTemplateMoney;
	}
});

 /**
 * OrderIntegralSaleView: 整单积分抵扣View
 */
var OrderIntegralSaleView = BackboneLite.View.extend({
	events: {
		'click .xa-integral': 'onClickIntegral',
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.integralInfo = options.integralInfo;
		this.orderPriceProvider = options.orderPriceProvider;
		this.isChecked = false;
	},

	render: function() {
		var $totalIntegral = this.$el;
		var integralObject = this.calculateIntegralMoney();
		if (!this.isChecked) {
			$totalIntegral.find('.xa-product-integral-info').html('您有<span class="xt-totalIntegral">'+integralObject.totalIntegral+'</span>积分，可使用<span class="xt-usableIntegral">'+integralObject.integral+'</span>积分抵扣￥<span class="xt-money">'+integralObject.money+'</span>元');
		}
	},
	onClickIntegral:function(){
		var $label = $(event.currentTarget);
		var $totalIntegral = this.$el;
		var $checkbox =  $label.find('.xa-integral-checkbox');
		var integralObject = this.calculateIntegralMoney();
		if (!this.isChecked) {
			this.isChecked = true;
			$checkbox.attr('checked','checked');
			$totalIntegral.find('.xa-product-integral-info').html('您已使用<span class="xt-usedIntegral">'+integralObject.integral+'</span>积分抵扣￥<span class="xt-money">'+integralObject.money+'</span>元');
			this.trigger('use-integral', integralObject);
			$('.xa-triggerGroup').hide();
		}else{
			this.isChecked = false;
			$checkbox.removeAttr('checked');
			$totalIntegral.find('.xa-product-integral-info').html('您有<span class="xt-totalIntegral">'+integralObject.totalIntegral+'</span>积分，可使用<span class="xt-usableIntegral">'+integralObject.integral+'</span>积分抵扣￥<span class="xt-money">'+integralObject.money+'</span>元');
			this.trigger('cancel-use-integral', {});
			$('.xa-triggerGroup').show();
		}
	},
	calculateIntegralMoney:function(price){
		var $totalIntegral = this.$el;
		// 最大可用抵扣比例
		var usedIntegralCount = parseInt($totalIntegral.attr('data-integralCount'));
		// 最大可用积分
		var usedIntegralMoney = (this.orderPriceProvider.getOrderPromotionedPrice() * usedIntegralCount / 100).toFixed(2);
		var integralInfo = this.integralInfo;
		var haveTotalIntegral = integralInfo.count;
		var usedIntegral = Math.ceil(usedIntegralMoney * integralInfo.count_per_yuan)
		if(haveTotalIntegral < usedIntegral){
			usedIntegral = haveTotalIntegral;
			usedIntegralMoney = (usedIntegral / integralInfo.count_per_yuan).toFixed(2);
		}
		return{
			integral: usedIntegral,
			money: usedIntegralMoney,
			totalIntegral:haveTotalIntegral
		}
	}
});

/**
 * IntegralSaleView: 积分应用View
 */
var IntegralSaleView = BackboneLite.View.extend({
	events: {
		'click .xa-integral': 'onClickIntegral',
	},

	initialize: function(options) {
		this.$el = $(this.el);

		this.integralInfo = options.integralInfo;
		this.productGroups = options.productGroups;
		this.integralManager = options.integralManager;
		this.isChecked = false;
	},

	render: function() {
		xlog('in render')
		console.log(this.productGroups,33333333333333333)
		var $productGroup = this.$el;
		var productGroupId = parseInt($productGroup.data('productGroupId'));
		var productGroup = _.findWhere(this.productGroups, {"id": productGroupId});

		var usableIntegral = this.integralManager.getUsableIntegral();


		if (this.isChecked) {
			var usedIntegral = this.usedIntegral;
			//$('#integral_'+ product.id+'_'+productModel).val(usedIntegral.integral);
			$productGroup.find('.xa-product-integral-info').html('您已使用<span class="xt-usedIntegral">'+usedIntegral.integral+'</span>积分抵扣￥<span class="xt-money">'+usedIntegral.money.toFixed(2)+'</span>元');
			if (productGroup.promotion_result) {
				$productGroup.find('.xa-subtotal').html('<span class="xt-subtotal">'+productGroup.promotion_result.subtotal.toFixed(2)+'</span>');
			}
		} else {
			this.usedIntegral = this.useIntegral(productGroup);
			var usedIntegral = this.usedIntegral;
			$productGroup.find('.xa-product-integral-info').html('您有<span class="xt-totalIntegral">'+usableIntegral+'</span>积分，可使用<span class="xt-usableIntegral">'+usedIntegral.integral+'</span>积分抵扣￥<span class="xt-money">'+usedIntegral.money.toFixed(2)+'</span>元');
			if (productGroup.promotion_result) {
				$productGroup.find('.xa-subtotal').html('<span class="xt-subtotal">'+productGroup.promotion_result.subtotal.toFixed(2)+'</span>');
			}
		}
	},

	/**
	 *  useIntegral: 使用积分
	 */
	useIntegral: function(productGroup){
		var integralSaleRule = productGroup.integral_sale_rule;

		// 获得使用积分的商品基准价格
		if (productGroup.promotion_result) {
			//如果促销活动更改了价格，则使用更改后的价格作为使用积分的基准价格
			if (productGroup.promotion_result.subtotal) {
				totalProductPrice += productGroup.promotion_result.subtotal;
			}
		} else {
			var totalProductPrice = 0.0;
			for (var i = 0; i < productGroup.products.length; ++i) {
				var product = productGroup.products[i];
				totalProductPrice += product.count * product.price;
			}
		}

		//遍历product，使用每一个product的integral sale rule，计算每一个product的积分使用情况
		var products = productGroup.products
		var maxIntegral = 0;
		for (var i = 0; i < products.length; ++i) {
			var product = products[i];
			var productPrice = 0;
			if (productGroup.promotion_type == 'flash_sale') {
				product_price = productGroup.promotion.detail.promotion_price;
				productPrice = product.count * product_price;
			} else {
				product_price = product.price;
				productPrice = product.count * product_price;
			}
			if (product.active_integral_sale_rule) {
				var integralSaleRule = product.active_integral_sale_rule;
				maxIntegral += productPrice * integralSaleRule.discount / 100 * this.integralInfo.count_per_yuan;
			}
		}

		// 确定商品可用积分
		var usableIntegral = this.integralManager.getUsableIntegral();
		var neededIntegral = usableIntegral;
		if (maxIntegral < usableIntegral) {
			neededIntegral = maxIntegral;
		}
		// 该product group可用积分，相对价钱，计算时，使用浮点数计算
		var money = (neededIntegral+0.0) / this.integralInfo.count_per_yuan;

		xlog('maxIntegral: ' + maxIntegral);
		xlog('usableIntegral: ' + usableIntegral);
		xlog('neededIntegral: ' + neededIntegral);

		return {
			integral: Math.ceil(neededIntegral),
			realIntegral: neededIntegral,
			money: money
		}
	},

	/**
	 * onClickIntegral: 点击"使用积分"区域的响应函数
	 */
	onClickIntegral: function(event) {
		xlog('enter onClickIntegral');
		var $label = $(event.currentTarget);
		var $productGroup = $label.parents('.xa-productGroup');
		var $checkbox = $productGroup.find('.xa-integral-checkbox');
		var $integral = $productGroup.find('.xa-integral');
		var productGroupId = parseInt($productGroup.data('productGroupId'));
		var productGroup = _.findWhere(this.productGroups, {"id": productGroupId});
		var product = productGroup.products[0];
		var productModel = product.model.replace(/:/g, '-');
		var usedIntegral = this.usedIntegral;
		xlog($checkbox);

		if (!this.isChecked) {
			$checkbox.prop('checked', true);
			this.isChecked = true;
			if (productGroup.promotion_result == "" || productGroup.promotion_result == null)
				productGroup.promotion_result = {}
			productGroup.promotion_result["integralMoney"] = usedIntegral.money;
			productGroup.promotion_result["originalSubtotal"] = productGroup.promotion_result["subtotal"];
			productGroup.promotion_result["subtotal"] = productGroup.promotion_result["subtotal"] - usedIntegral.money;
			$integral.val(usedIntegral.realIntegral);
			this.trigger('use-integral', this.usedIntegral);
			if($integral.val()>0)
				$('.xa-triggerGroup').hide();
		}else{
			this.usedIntegral = null;
			$checkbox.prop('checked', false);
			this.isChecked = false;
			productGroup.promotion_result["integralMoney"] = 0.0;
			if (productGroup.promotion_result["originalSubtotal"]) {
				productGroup.promotion_result["subtotal"] = productGroup.promotion_result["originalSubtotal"];
			}
			$integral.val(0);
			this.trigger('cancel-use-integral', usedIntegral);
			var needShowCoupon = true;
			$('.xa-integral:hidden').each(function(i,n){
				if($(n).val()>0)
					needShowCoupon = false;
			});
			if(needShowCoupon)
				$('.xa-triggerGroup').show();
		}
	},
});


/**
 * WeizoomCardView: 微众卡View
 */
var WeizoomCardView = BackboneLite.View.extend({
	events: {
		//引导 微众卡使用
		'click .xa-useWeizoomCardButton': 'onClickUseWeizoomCardButton',
		//弹窗 微众卡使用
		'click .xa-confirmButton': 'onAddNewWeizoomCardButton',
		//微众卡删除
		'click .xa-removeWeizoomCardButton': 'onClickRemoveWeizoomCardButton',
		'click .xa-addNewCard': 'onClickAddNewWeizoomCardButton',
		'click .xa-cancleWeizoomDialogButton': 'onClickCancelDialogButton',
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.enableSubmitWeizoomCard = true;

		this.useWeizoomCards = [];
	},

	render: function() {

	},

	/**
	 * onClickWeizoomCardButton: 点击"使用"按钮
	 */
	onClickUseWeizoomCardButton: function(event){
		if (this.enableSubmitWeizoomCard) {
			this.enableSubmitWeizoomCard = false;
			var name = $('#tmp_card_name').val().trim();
			var pass = $('#tmp_card_pass').val().trim();
			this.handleWeizoomCard(name, pass, $('.xa-guideUse'));
		}
	},

	onAddNewWeizoomCardButton: function(event){
		if (this.enableSubmitWeizoomCard) {
			this.enableSubmitWeizoomCard = false;
			var name = $('.xa-cardid').val().trim();
			var pass = $('.xa-password').val().trim();
			this.handleWeizoomCard(name, pass, $('.xa-cardDialog'));
		}
	},

	onClickAddNewWeizoomCardButton: function(event) {
		$('.xa-cardDialog').css({
            height: window.screen.height,
            display: 'block'
        });
	},

	onClickCancelDialogButton: function(event) {
		$('.xa-cardDialog').hide();
		$('.xa-cardid').val('');
		$('.xa-password').val('');
		$('.xa-errorHint').hide();
    },

	handleWeizoomCard: function(name, pass, $el){
		var error_message = '卡号或密码错误';
		if (name.length === 0) {
			error_message = '请输入卡号';
			$el.find('.xa-errorHint').show().text(error_message);
			this.enableSubmitWeizoomCard = true;
			return;
		}else if(pass.length === 0){
			error_message = '请输入密码';
			$el.find('.xa-errorHint').show().text(error_message);
			this.enableSubmitWeizoomCard = true;
			return;
		}else{
			$el.find('.xa-errorHint').hide();
		}
		var weizoomCardIsMemberSpecial = false;
		for (var i = 0; i < this.useWeizoomCards.length; i++) {
			if (this.useWeizoomCards[i]['weizoomCardNum'] === name) {
				error_message = '该微众卡已经添加';
				$el.find('.xa-errorHint').show().text(error_message);
				this.enableSubmitWeizoomCard = true;
				return false;
			}else if(this.useWeizoomCards[i]['weizoomCardIsMemberSpecial']){
					weizoomCardIsMemberSpecial = true;
				}

		}

		var _this = this;
		W.getApi().call({
			app: 'webapp',
			api: 'project_api/call',
			method: 'post',
			args: _.extend({
				woid: W.webappOwnerId,
				project_id: W.projectId,
				name: name,
				module: 'mall',
				password: pass,
				target_api: 'weizoom_card/check'
			}),
			success: function(data) {
				if(data.code == 200) {
					if (weizoomCardIsMemberSpecial && data.is_new_member_special){
						error_message = '只能使用一张新会员专属卡';
						$el.find('.xa-errorHint').show().text(error_message);
						return false;
					}
					_this.useWeizoomCards.push({weizoomId: data.id, money: data.money, weizoomCardNum: name, weizoomCardPassWord: pass,weizoomCardIsMemberSpecial: data.is_new_member_special});
					$('.xa-cardDetails').append(
						'<div class="xui-weizoomCardInfo xa-weizoomCardInfo" data-weizoom-card-id="'+data.id+'">'
						+'<span class="xui-cardName">'+name+'</span>'
						+'<span class="xui-balance"> 余额:</span>'
						+'<span class="xui-money">'+data.money.toFixed(2)+'</span>'
						+'<span class="xui-usable">可使用:</span>'
						+'<span class="xui-money xa-usable-weizoom-card-money">'+data.money.toFixed(1)+'</span>'
						+'<a href="javascript:void(0);" class="xui-deleteButton xa-removeWeizoomCardButton">'
							+'<img src=/static_v2/img/webapp/mall/delete.png>'
						+'</a>'
						+'</div>');
					_this.fillWeizoomCardData();

					$('.xa-guideUse').hide();
					$('.xa-cardInfo').show();
					$('.xa-cardDialog').hide();
					$('.xa-cardid').val('');
					$('.xa-password').val('');
					_this.trigger('use-weizoom-card');
					$el.find('.xa-errorHint').hide();
				} else {
					$el.find('.xa-errorHint').show().text(error_message);
				}

				_this.enableSubmitWeizoomCard = true;
			},
			error: function(data) {
				var code = parseInt(data['code']);
				var msg = '';
				msg = data['data']['msg'];
				msg = msg || data.errMsg || error_message;

				$el.find('.xa-errorHint').show().text(msg);
				_this.enableSubmitWeizoomCard = true;
			}
		})
	},

	/**
	 * onClickRemoveWeizoomCardButton: 删除微众卡
	*/
	onClickRemoveWeizoomCardButton: function(event){
		console.log('remove weizoom card');
		var $weizoomCardEl = $(event.currentTarget).parents('div.xa-weizoomCardInfo');
		var weizoomCardId = $weizoomCardEl.attr('data-weizoom-card-id');
		$weizoomCardEl.remove();
		// $('.xa-use-weizoomcard-count').text(_this.useWeizoomCards.length);
		/* 删除数据 */
		for (var i = 0; i < this.useWeizoomCards.length; i++) {
			if (this.useWeizoomCards[i].weizoomId == weizoomCardId) {
				this.useWeizoomCards.splice(i,1);
			};
		};
		this.fillWeizoomCardData();

		if (this.useWeizoomCards.length === 0) {
			$('.xa-guideUse').show();
		}

		this.trigger('use-weizoom-card');
	},

	/**
	* fillWeizoomCardData: 微众卡数据填充
	*/
	fillWeizoomCardData:function(){
		var card = [];
		var pass = [];
		_.each(this.useWeizoomCards, function(weizoomCard){
			card.push(weizoomCard.weizoomCardNum);
			pass.push(weizoomCard.weizoomCardPassWord);
		});
		this.$('#card_name').val(card.join(','));
		this.$('#card_pass').val(pass.join(','));

		$('.xa-use-weizoomcard-count').text(this.useWeizoomCards.length);
	},

	/**
	* updateWeizoomCardPrice: 获取微众卡所使用的积分
	*/
	useWeizoomCard: function(totalPrice) {
		var totalWeizoomCardMoney = 0.0;
		for (var i = 0; i < this.useWeizoomCards.length; i++) {
			var card = this.useWeizoomCards[i];
			var cardMoney = card.money;
			var usedMoney = 0;

			if (totalPrice - totalWeizoomCardMoney - cardMoney < 0) {
				usedMoney = totalPrice - totalWeizoomCardMoney;
				totalWeizoomCardMoney = totalPrice;
			} else {
				usedMoney = cardMoney
				totalWeizoomCardMoney += usedMoney;
			}

			var $el = $('div[data-weizoom-card-id="'+card.weizoomId+'"]').find('.xa-usable-weizoom-card-money');
			$el.text(usedMoney.toFixed(2));
		};

		// 是否隐藏 添加按钮
		/**
		* 1、微众卡的总价大于订单总额
		* 2、最多使用微众卡数量10张
		*/
		if (totalPrice == totalWeizoomCardMoney || this.useWeizoomCards.length >= 10) {
			$('.xa-addNewCard').hide();
		} else if(this.useWeizoomCards.length <= 0) {
			$('.xa-cardInfo').hide();
			$('.xa-guideUse').show();
		} else {
			$('.xa-guideUse').hide();
			$('.xa-cardInfo').show();
			$('.xa-addNewCard').show();
		}
		return totalWeizoomCardMoney;
	}
});


/**
 * CouponManager: 优惠券管理View
 */
var CouponManager = BackboneLite.View.extend({
	events: {
		'click .xa-coupon': 'onClickCoupon',
		'click .xa-cancelCoupon': 'onClickCancelCouponLink',
		'click .xa-useCouponCode': 'onClickUseCouponCodeButton',
		'click .xa-closeCouponDialog': 'onClickCloseCouponDialog',
		'click .xa-couponSwiperSlide': 'onClickCouponDialog'
	},

	initialize: function(options) {
		this.$el = $(this.el);
		this.editOrderPageView = options.editOrderPageView;
	},

	render: function() {

	},

	/**
	 * onClickCloseCouponDialog: 点击coupon dialog中返回链接的响应函数
	 */
	onClickCloseCouponDialog: function(event) {
		var $dialog = $(event.target).parents('[data-ui-role="swipedialog"]');
		$dialog.data('view').hide();
	},

	/**
	 * onClickCoupon: 点击coupon的响应函数
	 */
	onClickCoupon: function(event) {
		this.onClickCloseCouponDialog(event);

		var $coupon = $(event.currentTarget);

		var id = $coupon.data('id');
		var money = $coupon.data('money');
		if (id && money) {
			$('#coupon_id').val(id).data('money', money).data('productid', $coupon.data('productid'));
			$('#is_use_coupon')[0].checked = true;

			// 修改使用优惠券后的样式
			$('.xa-coupon-money').html('已抵用'+money +'元');
			$('.xa-no-use-coupon-show').hide();
			$('.xa-use-coupon-show').show();

			var productid = $('#coupon_id').data('productid');
			$(view.products).each(function(i, n){
				if(productid > 0 && n.id == productid){
					// 单品券对应商品显示原价
					n.member_discount = n.price;
					n.price = n.original_price;
					view.prices();
					$('[data-product-id="'+n.id+'"]').find('.xa-product-price').text(n.price.toFixed(2));
				}else if (productid <= 0 && n.member_discount){
					// 单品券对应商品显示原价
					n.price = n.member_discount;
					n.member_discount = null;
					view.prices();
					$('[data-product-id="'+n.id+'"]').find('.xa-product-price').text(n.price.toFixed(2));
				}
			});

		}
		var $target = this.$el.find('.xa-couponItem');
		this.trigger('use-coupon');
		$('.xa-integral').hide();
		$('.xa-order-integral').hide();
	},

	/**
	 * onClickCancelCouponLink: 点击“取消使用”优惠券链接的响应函数
	 */
	onClickCancelCouponLink: function(event) {
		this.flag = true;
		$('.xa-no-use-coupon-show').show();
		$('.xa-use-coupon-show').hide();
		$('#is_use_coupon')[0].checked = false;
		$('#coupon_id').val(0).data('money', 0);
		this.trigger('use-coupon');
		$('.xa-integral').show();
		$('.xa-order-integral').show();

		//单品券恢复会员价格
		var productid = $('#coupon_id').data('productid');
		$(view.products).each(function(i, n){
			if(n.id == productid && n.member_discount){
				n.price = n.member_discount;
				n.member_discount = null;
				view.prices();
				$('[data-product-id="'+n.id+'"]').find('.xa-product-price').text(n.price.toFixed(2));
			}
		});

	},
	onClickCouponDialog:function(event){
		if(this.flag){
			this.flag = false;
			return;

		}
		var $target = $(event.currentTarget);
		var targetId = $target.data('target');
		$(targetId).data('view').show();

	},
	recordErrorForTest: function(message) {
		$('#xt-errMsg').val(message);
	},

	onClickUseCouponCodeButton: function(event) {
		var couponCouponId = $('[name=coupon_coupon_id]').val().trim();
		var _this = this;

		if (couponCouponId.length == 0) {
			//用户没有输入coupon
			this.onClickCloseCouponDialog(event);
		} else if (couponCouponId.length < 10) {
			$('.error-info').html('优惠券码格式不正确');
			_this.recordErrorForTest('优惠券码格式不正确');
		} else {
			var productIds = [];
			var productPrice = [];
			var original_price = [];
			var productId2price = {};
			$(_this.editOrderPageView.products).each(function(i,n){
				productIds.push(n.id);
				productPrice.push(n.count*n.price);
				original_price.push(n.count* n.original_price);
				if (!productId2price.hasOwnProperty(n.id)){
					//用于处理同一商品买了不同规格的情况
					productId2price[n.id] = 0;
				}
				productId2price[n.id] += n.count*n.price;  //duhao 20150909
			});
			var totalPrice = _this.editOrderPageView.prices().totalPrice;
			$('body').alert({
				isShow: true,
				info:'正在验证...',
				speed: 1000
			});
			W.getApi().call({
				app: 'webapp',
				api: 'project_api/call',
				method: 'post',
				args: {
					woid: W.webappOwnerId,
					module: 'mall',
					target_api: 'can_use_coupon/is',
					coupon_coupon_id: couponCouponId,
					total_price: totalPrice,
					product_ids: productIds.join('_'),
					product_price: productPrice.join('_'),
					original_price: original_price.join('_'),
					product_id2price: JSON.stringify(productId2price)
				},
				success: function(data) {
					$('.xa-integral').hide();
					$('.xa-order-integral').hide();
					var couponId = data['id'];
					var money = parseFloat(data['money']);
					var productid = data['productid'];
					if (parseInt(couponId) !== 0) {
						_this.onClickCloseCouponDialog(event);
						$('#coupon_id').val(couponId).data('money', money);
						$('#is_use_coupon')[0].checked = true;

						// 修改使用优惠券后的样式
						$('.xa-coupon-money').html('已抵用￥'+money);
						$('.xa-no-use-coupon-show').hide();
						$('.xa-use-coupon-show').show();
						var $target = _this.$el.find('.xa-couponItem');
						_this.editOrderPageView.prices();

						$(view.products).each(function(i, n){
							if(productid > 0 && n.id == productid){
								// 单品券对应商品显示原价
								n.member_discount = n.price;
								n.price = n.original_price;
								view.prices();
								$('[data-product-id="'+n.id+'"]').find('.xa-product-price').text(n.price.toFixed(2));
							}else if (productid <= 0 && n.member_discount){
								// 单品券对应商品显示原价
								n.price = n.member_discount;
								n.member_discount = null;
								view.prices();
								$('[data-product-id="'+n.id+'"]').find('.xa-product-price').text(n.price.toFixed(2));
							}
						});

					} else {
						$('.error-info').html(data['msg']);
						_this.recordErrorForTest(data['msg']);
					}
				},
				error: function(resp) {
					// console.log('error',resp);
					var errMsg = '';
					if (resp.errMsg) {
						errMsg = resp.errMsg;
					} else if (resp.data && resp.data['msg']) {
						errMsg = resp.data['msg']
					}
					$('.error-info').html(data['msg']);
					_this.recordErrorForTest(data['msg']);
				}
			});
		}
	},

	/**
	 * changeCouponStatus: 调整优惠券可用状态
	 */
	changeCouponStatus: function(price) {
		var coupons = $('#coupon_id').find('option');
		coupons.each(function(coupon) {
			var $el = $(this);
			var valid_restrictions = $el.attr('valid_restrictions');
			if (valid_restrictions != -1 && valid_restrictions > price) {
				$el.attr('disabled', "disabled");
			} else {
				$el.removeAttr('disabled');
			}
		});
	},
});

/**
 * PriceCutView: 满减View
 */
var PriceCutView = BackboneLite.View.extend({
    initialize: function(options) {
        this.$el = $(this.el);
        this.productGroups = options.productGroups;
    },

    render: function() {
        var $productGroup = this.$el;
        var productGroupId = parseInt($productGroup.data('productGroupId'));
        var productGroup = _.findWhere(this.productGroups, {"id": productGroupId});

        console.log('price_cut productGroup', productGroup)
        var priceCut = productGroup.promotion.detail;
        var products = productGroup.products;
        var totalPrice = 0.0;
        for (var i = 0; i < products.length; ++i) {
            var product = products[i];
            if (product.isSelect) {
                totalPrice += product.price * product.count;
            }
        }
        var totalCount = 0;
        for (var i = 0; i < products.length; i++ ) {
            var product = products[i];
            totalCount += product.count;
        }

        var count = 0;
        if (totalPrice >= priceCut.price_threshold) {
        	count = 1;
        }
        if (priceCut.is_enable_cycle_mode) {
            // 循环满减
            count = Math.floor(totalPrice / priceCut.price_threshold);
        }

        if (count > 0) {
	        var price = count * priceCut.price_threshold;
	        var cutMoney = count * priceCut.cut_money;
	        var priceCutInfo = '商品已购满<span class="xt-price">'+price+'</span>元，已减<span class="xt-cutMoney">'+cutMoney.toFixed(2)+'</span>元';
        }else{
        	var cutMoney = 0;
	        var priceCutInfo = '商品购满<span class="xt-price">'+priceCut.price_threshold+'</span>元，可减<span class="xt-cutMoney">'+priceCut.cut_money+'</span>元';
        }
        productGroup.promotion_result.subtotal = totalPrice - cutMoney;
        // productGroup.totalCount = totalCount;

        console.log('price cut totalCount', totalCount);
        $productGroup.find('.xa-promotion-info').html('共<span class="xt-subtotalCount">'+totalCount+'</span>件商品，');
        xlog($productGroup.find('.xa-price-cut-info'));
        $productGroup.find('.xa-price-cut-info').html(priceCutInfo);
        $productGroup.find('.xa-subtotal').text(productGroup.promotion_result.subtotal.toFixed(2));
    }
});


W.page.EditOrderPage = W.page.InputablePage.extend({
	events: _.extend({
		'click .xa-displayTrigger': 'onChangeDisplayTrigger',
		//发票
		'click .xa-choseBillType': 'onClickBillType',
		//支付方式
		'change #xa-choseInterfaces': 'onChangeInterface',
		//提交form
		'click .xa-submit': 'onClickSubmitButton',
		'click .xa-deleteButton': 'removeCantBuyProduct',
		'click .xa-deletePremiumButton': 'deletePremiumSubmit',
	}, W.page.InputablePage.prototype.events),

	initialize: function(options) {
		xlog('in EditOrderPage');
		this.postageCalculator = new PostageCalculator({
			el: 'body',
			postageFactor: options.postageFactor
		})
		this.productGroups = options.productGroups;
		this.products = this.collectProducts(this.productGroups);
		this.integralInfo = options.integralInfo;
		this.usedIntegral = 0;
		this.isChecked = false;

		//为integral sale创建view
		this.integralSaleViews = [];
		var _this = this;
		this.$('.xa-has-integral-sale-rule').each(function() {
			var view = new IntegralSaleView({
				el: this,
				integralInfo: _this.integralInfo,
				productGroups: _this.productGroups,
				integralManager: _this
			});
			view.on('use-integral', _.bind(_this.onUseIntegral, _this));
			view.on('cancel-use-integral', _.bind(_this.onCancelUseIntegral, _this));
			view.render();
			_this.integralSaleViews.push(view);
		});

		// 整单积分抵扣
		if($('.xa-order-integral').length > 0){
			this.orderIntegralView = new OrderIntegralSaleView({
				el: '.xa-order-integral',
				integralInfo: _this.integralInfo,
				orderPriceProvider: _this
			});
			this.orderIntegralView.on('use-integral', _.bind(_this.onUseOrderIntegral, _this));
			this.orderIntegralView.on('cancel-use-integral', _.bind(_this.onCancelUseOrderIntegral, _this));
			this.orderIntegralView.render();
			xlog(this.orderIntegralView)
		}

		//为premium sale创建view
		this.$('.xa-promotion-premium_sale').each(function(){
			var view = new W.common.PremiumSaleView({
				el: this,
				productGroups: _this.productGroups,
				integralManager: _this
			});
			view.render();
		});


		//为price cut创建view
		this.$('.xa-promotion-price_cut').each(function(){
			var view = new PriceCutView({
				el: this,
				productGroups: _this.productGroups
			});
			view.render();
		});

		//创建coupon manager
		this.couponManager = new CouponManager({
			el: this.el,
			editOrderPageView: this
		});
		this.couponManager.on('use-coupon', function() {
			_this.prices();
		});

		//创建product group price calculator
		this.productGroupPriceCalculator = new W.common.ProductGroupPriceCalculator({
			el: this.el
		});

		//创建weizoom card view
		this.weizoomCardView = new WeizoomCardView({
			el: this.el
		});
		this.weizoomCardView.on('use-weizoom-card', _.bind(this.onUseWeizoomCard, this));
		this.weizoomCardView.render();

		// 地区id
		this.provinceId = null;
		this.isOrderFromShoppingCart = options.isOrderFromShoppingCart;

		//内部状态变量
		this.enableSubmitOrder = true; //是否允许使用提交按钮
		this.prices();
		this.resetForm();

		//如果有微信支付，则默认选中；否则，默认选中第一个dd中的input
		if($('.xa-payOption').length != 0){
			if($('.xa-wxpay').length != 0){
				$('.xa-wxpay input').attr('checked', 'checked');
			}else{
				$('.xa-payOption dd:last-child').children('input').attr('checked', 'checked');
			}
		}
	},

	collectProducts: function(productGroups) {
		var products = [];
		for (var i = 0; i < productGroups.length; ++i) {
			var productGroup = productGroups[i];
			var productsInGroup = productGroup['products'];
			for (var j = 0; j < productsInGroup.length; ++j) {
				var product = productsInGroup[j];
				product.isSelect = true;
				products.push(product);
			}
		}

		return products;
	},
	onUseOrderIntegral:function(usedIntegral){
		this.usedIntegralMoney = usedIntegral.money;
		this.usedIntegralCount = usedIntegral.integral;
		this.prices();
	},

	onCancelUseOrderIntegral:function(usedIntegral){
		this.usedIntegralMoney = 0;
		this.usedIntegralCount = 0;
		this.prices();
	},


	onUseIntegral: function(usedIntegral) {
		this.usedIntegral += usedIntegral.integral;
		_.each(this.integralSaleViews, function(integralSaleView) {
			integralSaleView.render();
		});
		this.prices();
	},

	onCancelUseIntegral: function(usedIntegral) {
		this.usedIntegral -= usedIntegral.integral;
		_.each(this.integralSaleViews, function(integralSaleView) {
			integralSaleView.render();
		});
		this.prices();
	},

	onUseWeizoomCard: function() {
		this.prices();
	},

	getUsableIntegral: function() {
		return this.integralInfo.count - this.usedIntegral;
	},
	getOrderPromotionedPrice: function() {
		return this.orderPrice;
	},
	resetForm:function(){
		var $payInterface =  $('#xa-choseInterfaces');
		$payInterface.val("");
	},

	/**
     * getOrderAreaProvinceId: 获取地区id
     * 如：选择的地区是北京
     * return province_1
     */
    getOrderAreaProvinceId: function(){
        if (this.provinceId != null) {
            return this.provinceId;
        }

        var $area = this.$('#area');
        if ($area.val().length > 0) {
            var province_id = $area.val().split('_')[0];
            this.provinceId = 'province_' + province_id;
        }
        return this.provinceId;
    },

	/*
	*onClickBillType：选择发票类型
	*/
	onClickBillType:function(event){
		var $parent = $(event.target).parents('.xa-choseBillType');

		var $input = $parent.find('input[type="text"]');
		$input.attr('name', "bill");

	   $parent.find('input.xa-billInput').prop('checked','checked');
	   var brother = $parent.siblings().find('input[type="text"]');
	   $parent.siblings().find('input[type="text"]').attr('name', '').attr('disabled', 'disabled').val('');
	   $input.removeAttr('disabled').focus();
	},

	/**
	 * calculateTotalPrice: 计算商品总价
	 */
	calculateTotalPrice: function(options) {
		if (!options.products) {
			return 0.0;
		}

		var totalProductPrice = 0.0; //商品总价
		var totalPrice = 0.0;
		var totalPromotionPrice = 0.0; 	//促销优惠金额
		var totalPromotionedPrice = 0.0; //促销后的总价
		var integralMoney = 0.0; //积分抵扣金额
		//获得优惠券
		var couponMoney = 0;
		var couponProductId = 0;
		var couponId = this.$('[name="coupon_id"]').val();
		if (couponId) {
			couponMoney = parseFloat($('[name="coupon_id"]').data('money')) || 0;
			couponProductId = $('[name="coupon_id"]').data('productid');
			var maxCouponMoney = 0;
			if (couponProductId > 0) {// 单品券
				_.each(options.productGroups, function(group){
					_.each(group.products, function(product){
						if(product.id==couponProductId){
							maxCouponMoney += product.price * product.count;
						}
					});
				})
			}else{// 全店通用券
				_.each(options.productGroups, function(group){
					_.each(group.products, function(product){
						if(!product.forbidden_coupon){// TODO 不禁用全场优惠券商品
							maxCouponMoney += product.price * product.count;
						}
					});
				})
			}
			if(couponMoney > maxCouponMoney){
				couponMoney = maxCouponMoney;
				$('.xa-coupon-money').html('已抵用');
			}
		}
		if(this.orderType !== 'test') {
			var productGroupsPriceInfo = this.productGroupPriceCalculator.calculate(options.productGroups);
			xlog(productGroupsPriceInfo);
			totalProductPrice = productGroupsPriceInfo.productPrice;
			totalPromotionPrice = productGroupsPriceInfo.productPrice - productGroupsPriceInfo.promotionedPrice;
			if (this.usedIntegralMoney) {
				// 整单积分抵扣
				integralMoney = parseFloat(this.usedIntegralMoney);
			}else{
				// 积分应用
				integralMoney = productGroupsPriceInfo.integralMoney;
			}
			totalPromotionedPrice = productGroupsPriceInfo.promotionedPrice - integralMoney;

			// 计算运费
			var postage = this.postageCalculator.getPostage(options.products, this.getOrderAreaProvinceId());
			// 商品总价 = 促销后的总价 + 运费 - 优惠券
			// var totalPrice = totalPromotionedPrice + postage - couponMoney;
			var totalPrice = totalPromotionedPrice - couponMoney;
			if(totalPrice < 0){
				totalPrice = 0;
				couponMoney = totalPromotionedPrice;
				$('.xa-coupon-money').html('已抵用');
			}
			totalPrice += postage

			// 使用微众卡金额
			var weizoomCardPrice = this.weizoomCardView.useWeizoomCard(totalPrice);
			totalPrice -= weizoomCardPrice;
			// totalPrice -= integralMoney;

		} else {
			// 如果是测试够买，总价钱为0.01 by liupeiyu
			totalProductPrice = 0.01;
			var totalPrice = 0.01;
		}
		return {
			'totalProductPrice': totalProductPrice.toFixed(2),
			'totalPrice': totalPrice.toFixed(2),
			'totalPromotionPrice': totalPromotionPrice.toFixed(2),
			'totalPromotionedPrice': totalPromotionedPrice,
			'postage': postage.toFixed(2),
			'integralMoney': integralMoney.toFixed(2),
			'weizoomCardPrice': weizoomCardPrice.toFixed(2),
			'couponMoney':couponMoney.toFixed(2)
		};
	},

	/**
	 * prices: 所有价格的展示
	 */
	prices: function() {
		//获得商品列表
		// 补充促销信息
		//products = this.productsPromotionFill(products);

		//计算价格
		var priceInfo = this.calculateTotalPrice({
			products: this.products,
			productGroups: this.productGroups,
		});

		var totalProductPricePostage = priceInfo.postage + priceInfo.totalProductPrice;
		this.couponManager.changeCouponStatus(totalProductPricePostage);

		this.orderPrice = priceInfo.totalPromotionedPrice;

		if(this.orderIntegralView)
			this.orderIntegralView.render();

		//更新运费显示
		if (priceInfo.postage <= 0) {
			$('.xa-postageElement').text('0.00');
		}else{
			$('.xa-postageElement').text(priceInfo.postage);
		}

		//使用积分和优惠券，价格项改变
		if(priceInfo.integralMoney > 0){
			$('.xa-integralMoney').text(priceInfo.integralMoney).parents('p').removeClass('hidden');
		}else{
			$('.xa-integralMoney').parents('p').addClass('hidden');
		}

		// 更新促销抵扣显示
		if(priceInfo.totalPromotionPrice <= 0){
			$('.xa-promotionMoney').parents('p').addClass('hidden');
		}else{
			$('.xa-promotionMoney').text(priceInfo.totalPromotionPrice).parents('p').removeClass('hidden');
		}

		// 更新优惠券显示
		if(priceInfo.couponMoney == 0){
			$('.xa-couponMoney').parents('p').addClass('hidden');
		}else{
			$('.xa-couponMoney').text(priceInfo.couponMoney).parents('p').removeClass('hidden');
		}

		// 微众抵扣
		if (priceInfo.weizoomCardPrice > 0) {
			$('.xa-weizoomCardMoney').text(priceInfo.weizoomCardPrice).parents('p').removeClass('hidden');
		}else{
			$('.xa-weizoomCardMoney').parents('p').addClass('hidden');
		}

		//更新页面元素
		var $submitBtn = this.$el.find('#submit-order');
		if (priceInfo.totalPrice <= 0.0) {
			priceInfo.isValidPrice = false;
			$('.xa-totalPrice').text("0.00");
		} else {
			$('.xa-totalPrice').text(priceInfo.totalPrice);
			priceInfo.isValidPrice = true;
		}
		$('.xa-totalProductPrice').text(priceInfo.totalProductPrice);

		return priceInfo;
	},

	/**
	 * getProductsInfo: 获得订单中的商品信息
	 */
	getProductsInfo: function() {
		var productIds = [];
		var productCounts = [];
		var productModelNames = [];
		var promotionIds = [];
		$('.xa-product').each(function() {
			var $product = $(this);
			productIds.push($product.attr('data-product-id'));
			productCounts.push($product.attr('data-product-count'));
			productModelNames.push($product.attr('data-product-model-name'));
			promotionIds.push($product.attr('data-promotion-id'));
		});

		return {
			product_ids: productIds.join('_'),
			product_counts: productCounts.join('_'),
			product_model_names: productModelNames.join('$'),
			promotion_ids: promotionIds.join('_')
		}
	},

	/**
	 * getIntegralSaleInfo: 获得订单中的积分折扣信息
	 */
	getIntegralSaleInfo: function() {
		group2integralinfo = {};
		var _this = this;
		if(this.usedIntegralMoney){
			orderIntegralInfo = {}
			orderIntegralInfo["integral"] = this.usedIntegralCount
			orderIntegralInfo["money"] = this.usedIntegralMoney
			return {
				orderIntegralInfo: JSON.stringify(orderIntegralInfo)
			}
		}else{
			$('.xa-integral-checkbox').each(function() {
				var $checkbox = $(this);
				if (!$checkbox.prop('checked')) {
					return;
				}

				var $productGroup = $checkbox.parents('.xa-productGroup');
				var productGroupId = $productGroup.data('productGroupId');
				var productGroup = _.findWhere(_this.productGroups, {"id": productGroupId});
				if (productGroup.integral_sale_rule) {
					group2integralinfo[productGroup.uid] = _.clone(productGroup.integral_sale_rule);
					group2integralinfo[productGroup.uid]['integral'] = $productGroup.find('.xa-integral').val();
					group2integralinfo[productGroup.uid]['money'] = $productGroup.find('.xt-money').html();
				}
			});
		}
		return {
			group2integralinfo: JSON.stringify(group2integralinfo)
		}
	},

	/**
	 * onChangeInterface: 选择支付方式
	 */
	onChangeInterface:function(){
		var $payInterface =  $('#xa-choseInterfaces');
		var payInterfaceVal = $payInterface.val();
		var payInterfaceText = $payInterface.find('option:selected').text();
		$payInterface.siblings('.xa-selectedOpt').text(payInterfaceText);
	},

	/**
	 * submitOrder: 提交订单
	 */
	submitOrder: function(args) {
		var _this = this;
		W.getApi().call({
			app: 'webapp',
			api: 'project_api/call',
			method: 'post',
			args: _.extend({
				woid: W.webappOwnerId,
				module: 'mall',
				is_order_from_shopping_cart: this.isOrderFromShoppingCart,
				target_api: 'order/save',
				order_type: this.orderType
			}, args),
			success: function(data) {
				var orderId = data['id'];
				var order_id = data['order_id'];
				var final_price = parseFloat(data['final_price']);
				xlog(data)
				if(final_price <= 0 || !args['xa-choseInterfaces']){
					window.location.href = "./?woid="+ W.webappOwnerId+"&module=mall&model=pay_result_success&action=get&order_id="+order_id+"&workspace_id=mall&fmt="+W.curRequestMemberToken;
					// jz 2015-10-09
					// &isShowSuccess=true";
				}else if(data['pay_url']){
					window.location.href = data['pay_url']+"&fmt="+W.curRequestMemberToken;
				}else{
					// _this.payOrder(orderId);
					xerror('save order not return pay_url data:'+data)
				}
			},
			error: function(resp) {
				var errMsg = '下单失败';
				var speed = 1;
				if(resp.data.detail.length > 0){
					$tmpl = $('.xa-cantBuyDialog li').clone();
					$('.xa-cantBuyDialog ul').empty();
					// 是否弹赠品库存不足的窗口
					var premiumStockError = true;
					$.each(resp.data.detail, function(i, n){
						var src, name, price, count, model_name;
						$t = $tmpl.clone();
						if(n.name){
							src = n.pic_url;
							name = n.name;
							price = n.stocks;
							// count = n.need_stocks;
							count = n.stocks;
							$t.addClass('hidden')
						}else{
							$el = $('[data-product-id="'+n.id+'"]').filter('[data-product-model-name="'+n.model_name+'"]');
							src = $el.find('img').attr('src');
							name = $el.find('.xa-name').text();
							price = $el.find('.xa-product-price').text();
							count = $el.data('product-count');
							model_name = $el.find('.xt-model').html();
							$t.data('model-name', n.model_name);
							premiumStockError = false;
						}
						$t.data('id', n.id);
						$t.find('.xa-cantBuyReason').text(n.short_msg);
						$t.find('img').attr('src', src);
						$t.find('.xa-cantBuyProductName').text(name);
						$t.find('.xa-product-price').text(price);
						$t.find('.xa-count').text(count);
						$t.find('.xa-cantBuyProductModel').html(model_name);
						$('.xa-cantBuyDialog ul').append($t);
					})
					if(premiumStockError){
						// 弹出赠品库存不足的窗口
						$('.xa-cantBuyDialog .hidden').removeClass('hidden').show();
						$('.xa-cantBuyDialog .xa-cantBuyElement').hide();
					}else if($('li.xa-product').length == $('.xa-cantBuyDialog li').not('.hidden').length){
						// 全部商品
						$('.xa-deleteButton').hide();
					}
					if (/ipad|iphone|mac/i.test(navigator.userAgent)){
						if(resp.data.detail.length > 3){
	    					$('#cantBuyWrapper').css('height', '218px');
	        				var cantBuyWrapper = new iScroll('cantBuyWrapper',{checkDOMChanges: true});

						}
					}
					var query = parseUrl(location.href).query;
					var url = '/termite/workbench/jqm/preview/?woid='+query.woid+'&module=mall';
					if(location.href.indexOf('shopping_cart_order')<0){
						url += '&model=product&rid='+query.product_id;
					}else{
						url += '&model=shopping_cart&action=show';
					}
					url += '&fmt=' + query.fmt;
					$('.xui-goBackButton').attr('href', url);
					$('.xa-cantBuyDialog').show();
				}else{
					if (resp.errMsg) {
						errMsg = resp.errMsg;
					} else if (resp.data && resp.data['msg']) {
						errMsg = resp.data['msg']
					}
					speed = 2000;
				}
				$('body').alert({
					isShow: true,
					isError: true,
					info: errMsg,
					speed: speed,
					callBack: function() {
						_this.enableSubmitOrderButton();
						// window.location.reload();
					}
				});

				isSubmit = false;
			}
		});
	},

	deletePremiumSubmit: function(){
		$('.xa-cantBuyDialog').hide();
		var args = _.extend($('form').serializeObject(), this.getProductsInfo(), this.getIntegralSaleInfo());
		$('body').alert({
			isShow: true,
			info:'正在提交订单',
			speed: 200000
		});
		args.forcing_submit = 1;
		this.submitOrder(args);
	},

	removeCantBuyProduct: function(){
		// 删除不能购买的商品
		var query = parseUrl(location.href).query;
		var product_ids = query.product_ids.split('_');
		var product_counts = query.product_counts.split('_');
		var product_model_names = query.product_model_names.split('$');
		$('.xa-cantBuyDialog li').each(function(i,n){
			var id = $(n).data('id'), model_name = $(n).data('model-name'), id_index = -1;
			if(model_name && model_name!='standard'){
				// 根据规格删除
				id_index = product_model_names.indexOf(model_name);
			}else{
				// 没有规格时
				id_index = product_ids.indexOf(id+'');
			}
			if(id_index==-1){
				return;
			}
			product_ids.splice(id_index, 1);
			product_counts.splice(id_index, 1);
			product_model_names.splice(id_index, 1);
		});
		var url = '/termite/workbench/jqm/preview/?woid='+query.woid
			+'&module=mall&model=shopping_cart_order&action=edit&product_ids='+product_ids.join('_')
			+'&product_counts='+product_counts.join('_')+'&product_model_names='+product_model_names.join('$');
		location.href = url;
	},

	// payOrder: function(orderId){
	// 	var $link = $(this);
	// 	var $payInterface =  $('[name="xa-choseInterfaces"]:checked');
	// 	var interfaceType = $payInterface.val();
	// 	if(!interfaceType && parseFloat($('.xa-totalPrice').text())>0){
	// 		$('body').alert({
	// 			isShow: true,
	// 			speed: 2000,
	// 			info: '请使用优惠抵扣完成支付...'
	// 		});
	// 		return;
	// 	}
	// 	var interfaceId = $payInterface.attr('data-id');
	// 	var args = {order_id: orderId};
	// 	var _this = this;
	// 	if (interfaceType != 9) {//支付方式为货到付款，则不提示“正在支付”
	// 		$('body').alert({
	// 			isShow: true,
	// 			speed: 2000,
	// 			info: '正在去支付…'
	// 		});
	// 	}
	// 	W.getApi().call({
	// 		app: 'webapp',
	// 		api: 'project_api/call',
	// 		method: 'post',
	// 		args: _.extend({
	// 			webapp_owner_id: W.webappOwnerId,
	// 			module: 'mall',
	// 			target_api: 'order/pay',
	// 			interface_type: interfaceType,
	// 			interface_id: interfaceId
	// 		}, args),
	// 		success: function(data) {
	// 			order_id = data['order_id'];
	// 			if (data['msg'] != null) {
	// 				$('body').alert({
	// 					isShow: true,
	// 					speed: 2000,
	// 					info: data['msg'] || '操作失败!'
	// 				});
	// 				// _this.enableSubmitOrderButton();
	// 				window.location.reload();
	// 			} else {
	// 				window.location.href = data['url'];
	// 			}
	// 		},
	// 		error: function(resp) {
	// 			var errMsg = null;
	// 			if (resp.data) {
	// 				errMsg = resp.data['msg'];
	// 			}
	// 			if (!errMsg) {
	// 				errMsg = '操作失败!';
	// 			}
	// 			$('body').alert({
	// 				isShow: true,
	// 				info: errMsg,
	// 				speed:2000
	// 			});
	// 			// _this.enableSubmitOrderButton();
	// 			window.location.reload();
	// 		}
	// 	});
	// 	// }
	// },

	doSubmitOrder: function() {
		//提交表单
		var isUseBill = $('input[name="is_use_bill"]')[0].checked;
		if(isUseBill){
			var billVal = $('input[name="bill"]').val();
			if(billVal.length == 0){
				$("body").alert({
					isShow:true,
					info:"发票信息不能为空",
					speed:600
				});
				this.enableSubmitOrderButton();
				return false;
			}
		}

		$('#integral').val(this.useIntegral);
		var args = _.extend($('form').serializeObject(), this.getProductsInfo(), this.getIntegralSaleInfo());
		$('body').alert({
			isShow: true,
			info:'正在提交订单',
			speed: 3000
		});
		this.submitOrder(args);
	},

	/**
	 * enableSubmitOrderButton: 启用提交订单按钮
	 */
	enableSubmitOrderButton: function() {
		this.enableSubmitOrder = true;
	},

	/**
	 * disableSubmitOrderButton: 禁用提交订单按钮
	 */
	disableSubmitOrderButton: function() {
		this.enableSubmitOrder = false;
	},

	/**
	 * onChangeDisplayTrigger: 点击display trigger的响应函数
	 */
	onChangeDisplayTrigger: function(event) {
		var $trigger = $(event.currentTarget);
		var $checkbox = $trigger.siblings('input[type="checkbox"]');
		var targetId = $trigger.data('target');
		var $triggerGroup = $trigger.parents('.xa-triggerGroup');
		var $content = $triggerGroup.find(targetId);
		if ($content.length === 0) {
			var $content = $(targetId);
		}

		var displayMode = $content.data('mode');
		if (displayMode === 'dropDown') {
			if(!this.isChecked){
				$checkbox.attr('checked','checked');
				this.isChecked = true;
			}else{
				$checkbox.removeAttr('checked');
				this.isChecked = false;
			}
			var css = this.isChecked ? 'block' : 'none';
			var domTriggerGroup = $triggerGroup[0];
			var $content = $triggerGroup.find(targetId);
			var $title = $content.siblings();
			$content.css({
				display: css
			});
			if (css === 'none') {
				$title.find('.xui-icon').removeClass('xui-arrow-slideDown');
				$title.find('.xa-bill-status').fadeIn(100);
			}else{
				$title.find('.xui-icon').addClass('xui-arrow-slideDown');
				$title.find('.xa-bill-status').fadeOut(50);
			};

			var $textInput = $content.find('input[type="text"]');
			if ($textInput.length > 0) {
				$textInput.eq(0).focus();
			} else {
				$textInput = $content.find('input[type="number"]');
				$textInput.eq(0).focus();
			}
		}else {
			xerror('wrong display mode : ' + displayMode);
		}
	},

	/**
	 * onClickSubmitButton: 点击“提交”按钮的响应函数
	 */
	onClickSubmitButton: function(event) {
		var $payInterface =  $('[name="xa-choseInterfaces"]:checked');
		var interfaceType = $payInterface.val();
		if(!interfaceType && parseFloat($('.xa-totalPrice').text())>0){
			$('body').alert({
				isShow: true,
				speed: 2000,
				info: '请使用微众卡抵扣商品金额...'
			});
			return;
		}
		if (!this.enableSubmitOrder) {
			return;
		}
		this.disableSubmitOrderButton();
		var $form = $('form');
		if (W.validate($form)) {
			this.doSubmitOrder();
		} else {
			this.enableSubmitOrderButton();
		}
	}
});
})(W);
