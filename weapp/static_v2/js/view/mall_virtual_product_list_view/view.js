/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 运费模板编辑器
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.VirtualProductListView = Backbone.View.extend({
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
		'click .xa-activeFinish':'onClickActiveFinish',
		'click .xa-select': 'onClickSelect'
	},

	render: function() {
		this.filterView = new W.view.mall.PromotionFilterView({
			el: '.xa-virtualFilterView',
			promotionType: this.promotionType,
			templateName: this.options.templateFilterName, 
			promotionStatus: this.options.promotionStatus || '',  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
			startDate: this.options.startDate || '',  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
			endDate: this.options.endDate || ''  //支持从首页店铺提醒“即将到期的活动”过来的请求 duhao 20150925
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
		this.table.curPage = 1;
		this.table.reload(data, {
			emptyDataHint: '没有符合条件的促销活动'
		});
	},

	finishAndDeleteProducts:function($tr, itemId){
		var _this = this;
		W.getApi().call({
			method: 'delete',
			app: 'mall2',
			resource: 'virtual_product',
			args: {virtual_product_id: JSON.stringify(itemId)},
			scope: this,
			success: function(data) {
				W.showHint('success', '结束成功!');
				_.each(itemId, function(itemId) {
					var item = this.table.getDataItem(itemId);
						item.set('status', '已结束');
						$tr.remove();
				}, this);
				_this.table.reload();
			},
			error: function(resp) {
				W.showHint('error', '结束失败!');
			}
		});
	},
	onClickActiveFinish:function(event){
		var $link = $(event.currentTarget);
		var $tr = $link.parents('tr');
		var itemId = $tr.data('id');
		var _this = this;
		W.requireConfirm({
			$el: $link,
			width: 455,
        	position:'top',
			isTitle: false,
			msg: '是否确定结束该活动!',
			confirm: function() {
				_this.finishAndDeleteProducts($tr, itemId);
			}
		});
	},


	onCheckedSelect: function(){
		var flag=0;
		$(".xa-select").each(function () {
			if ($(this).attr("checked")) {
				flag=1;
			}
		});
		return flag;
	}


	
});
