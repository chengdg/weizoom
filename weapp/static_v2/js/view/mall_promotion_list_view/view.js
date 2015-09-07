/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.PromotionListView = Backbone.View.extend({
	getModelInfoTemplate: function() {
		$('#mall-product-list-view-model-info-tmpl-src').template('mall-product-list-view-model-info-tmpl');
		return 'mall-product-list-view-model-info-tmpl';
	},

	initialize: function(options) {
		this.options = options || {};
		this.$el = $(this.el);
		this.table = this.$('[data-ui-role="advanced-table"]').data('view');
		this.promotionType = options.promotionType || 'all';
		this.modelInfoTemplate = this.getModelInfoTemplate();
	},

	events: {
		'click .xa-finish': 'onClickFinishLink',
		'click .xa-start': 'onClickFinishLink',
		'click .xa-delete': 'onClickDeleteLink',
		'click .xa-batchDelete': 'onClickBatchDeleteLink',
		'click .xa-batchFinish': 'onClickBatchFinishLink',
		'click .xa-showAllModels': 'onClickShowAllModelsButton',
		'click .xa-selectAll': 'onClickSelectAll',
		'click .xa-select': 'onClickSelect'
	},

	render: function() {
		this.filterView = new W.view.mall.PromotionFilterView({
			el: '.xa-promotionFilterView',
			promotionType: this.promotionType,
			templateName: this.options.templateFilterName
		});
		this.filterView.on('search', _.bind(this.onSearch, this));
		this.filterView.render();

		this.$('input[type="text"]').eq(0).focus();
		$('.xa-batchFinish').attr("disabled",true);

		$('.xa-batchDelete').attr("disabled",true);
	},

	finishPromotions: function($trs, promotionIds, start) {
		var _this = this;
		W.getApi().call({
			method: 'post',
			app: 'mall2',
			resource: 'promotion',
			args: {ids: promotionIds, type: this.promotionType, start: start},
			scope: this,
			success: function(data) {
				W.showHint('success', '结束成功!');
				$trs.find('.xa-remained-count').text("库存0");
				$trs.css('background-color', 'yellow');
				_.delay(function() {
					$trs.css('background-color', '#FFF');
				}, 300);
				_.each(promotionIds, function(promotionId) {
					var promotion = this.table.getDataItem(promotionId);
					promotion.set('status', '已结束');
				}, this);
				_this.table.reload();
			},
			error: function(resp) {
				W.showHint('error', '结束失败!');
			}
		});
	},

	deletePromotions: function($trs, promotionIds) {
		var _this = this;
		W.getApi().call({
			method: 'delete',
			app: 'mall2',
			resource: 'promotion',
			args: {
				ids: promotionIds,
				type: this.promotionType
			},
			success: function(data) {
				W.showHint('success', '删除成功!');
				for(var i = 0; i < promotionIds.length; ++i) {
					var id = promotionIds[i];
					$('tr[data-id="'+id+'"]').remove();
				}
				_this.table.reload();
			},
			error: function(resp) {
				W.showHint('error', '删除失败!');
			}
		});
	},

	onSearch: function(data) {
		this.table.reload(data, {
			emptyDataHint: '没有符合条件的促销活动'
		});
	},

	onClickFinishLink: function(event) {
		var $link = $(event.currentTarget);
		var msg = $link.text().replace('|','').trim();
		var warning_msg = '';
		var $tr = $link.parents('tr');
		var promotionId = $tr.data('id');
		var _this = this;
		if (msg == "使失效") {
			warning_msg = "<div class='xui-couponsLinkDialog'><p>已被领取的优惠券优惠码在有效期内还可以继续使用<p></div>"
		}
		W.requireConfirm({
			$el: $link,
			width: 388,
			position:'top',
			isTitle: false,
			msg: '确认'+msg+'活动？',
			warning_msg: warning_msg,
			confirm: function() {
				_this.finishPromotions($tr, [promotionId], msg=='开始');
				//_this.filterView.onClickSearchButton(); // 刷新商品列表
				//_this.table.reload();
			}
		});
	},

	onClickDeleteLink: function(event) {
		var $link = $(event.currentTarget);
		var $tr = $link.parents('tr');
		var promotionId = $tr.data('id');
		var _this = this;
		var $trs = this.$('[data-id="'+promotionId+'"]');
		W.requireConfirm({
			$el: $link,
			width: 373,
        		position:'top',
			isTitle: false,
			msg: '确认删除活动？',
			confirm: function() {
				_this.deletePromotions($tr, [promotionId]);
				//_this.onSearch(_this.filterView.getFilterData()); //onClickSearchButton(); // 刷新商品列表
				//_this.filterView.onClickSearchButton(); // 刷新商品列表
				//_this.table.reload();
			}
		});
	},

	onClickBatchFinishLink: function(event) {
		var $link = $(event.currentTarget);
		var ids = this.table.getAllSelectedDataIds();

		for (var i = 0; i < ids.length; ++i) {
			var id = ids[i];
			var promotion = this.table.getDataItem(id);
			if (promotion.get('status') === '已结束') {
				W.showHint('error', '不能同时进行删除和结束操作');
				return;
			}
		}

		for(var i = 0; i < ids.length; ++i) {
			var id = ids[i];
			$('[data-id="'+id+'"]').addClass('xa-actionTarget');
		}
		var $trs = $('.xa-actionTarget');
		$trs.removeClass('.xa-actionTarget');

		var _this = this;
		W.requireConfirm({
			$el: $link,
			width: 398,
        	position:'top',
			isTitle: false,
			msg: '确认结束全部活动？',
			confirm: function() {
				_this.finishPromotions($trs, ids);
			}
		});
	},

	onClickBatchDeleteLink: function(event) {
		var $link = $(event.currentTarget);
		var ids = this.table.getAllSelectedDataIds();

		for (var i = 0; i < ids.length; ++i) {
			var id = ids[i];
			var promotion = this.table.getDataItem(id);
			if (promotion.get('status') === '未开始' || promotion.get('status') === '进行中') {
				W.showHint('error', '有未结束的活动，请先结束活动。');
				return;
			}
		}

		for(var i = 0; i < ids.length; ++i) {
			var id = ids[i];
			$('[data-id="'+id+'"]').addClass('xa-actionTarget');
		}
		var $trs = $('.xa-actionTarget');
		$trs.removeClass('.xa-actionTarget');

		var _this = this;
		W.requireConfirm({
			$el: $link,
			width: 398,
        	position:'top',
			isTitle: false,
			msg: '确认删除全部活动？',
			confirm: function() {
				_this.deletePromotions($trs, ids);
			}
		});
	},

	/**
	 * onClickSelectAll: 点击“全选”复选框的响应函数
	 */
	onClickSelectAll: function(event) {
		var $checkbox = $(event.currentTarget);
		var isSelect = $checkbox.is(':checked');
		this.table.selectAll(isSelect);
		this.onClickSelect();
	},
	onCheckedSelect: function(){
		var flag=0;
		$(".xa-select").each(function () {
			if ($(this).attr("checked")) {
				flag=1;
			}
		});
		return flag;
	},

	onClickSelect: function(event) {
		var is_checked = this.onCheckedSelect();
		if(is_checked){
			$('.xa-batchFinish').attr("disabled",false);
			$('.xa-batchDelete').attr("disabled",false);
		}
		else{
			$('.xa-batchFinish').attr("disabled",true);
			$('.xa-batchDelete').attr("disabled",true);
		}
	},

	/**
	 * onClickShowAllModelsButton: 鼠标点击“查看规格”区域的响应函数
	 */
	onClickShowAllModelsButton: function(event) {
		var $target = $(event.currentTarget);
		var $tr = $target.parents('tr');
		var id = $tr.data('id');
		var promotion = this.table.getDataItem(id);
		var product = promotion.get('product');
		if (!product || product.length === 0) {
			//有多个product的promotion
			var products = promotion.get('products');
			var productId = parseInt($target.data('productId'));
			var product = _.find(products, function(product) { return product.id == productId; });
		}
		var models = product['models'];
		var properties = _.pluck(models[0].property_values, 'propertyName');
		var $node = $.tmpl(this.modelInfoTemplate, {properties: properties, models: models});
		W.popup({
			$el: $target,
			position:'top',
			isTitle: false,
			msg: $node
		});
	},
});
