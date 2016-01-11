ensureNS('W.view.mall');
W.view.mall.PromotionRedProductView = Backbone.View.extend({
	getTemplate: function() {
		$('#mall-promotion-red-product-view-tmpl-src').template('mall-promotion-select-product-view-tmpl');
		return 'mall-promotion-select-product-view-tmpl';
	},

	events: {
		'click .xa-search': 'onClickSearchButton',
		'click .xa-reset': 'onClickResetButton',
		'click .xa-delete': 'onClickDeleteProduct',
		'mouseenter .xa-vip-username': 'onMouseenterShow',
		'mouseleave .xa-vip-username': 'onMouseenterhide'
	},

	initialize: function(options) {
		this.$el = $(options.el);
        this.webapp_id = options.webapp_id;
	},

	render: function() {
        var _this = this;
        var args = {};
        args.webapp_id = this.webapp_id;
        args.filter_type = "member"
        W.getApi().call({
            app: 'mall2',
            resource: 'issuing_coupons_filter',
            args: args,
            success: function(data){
                var $node = $.tmpl(
                    _this.getTemplate(), 
                    {grades: $.parseJSON(data.member_grade),
                     tags: $.parseJSON(data.member_tags)}
                );

                _this.$('.xa-redEnevlopSelectConditionPanel').empty().append($node);
            }
        });
	},


	addVipInfo: function(products){
        var $form_submit = $('.xa-form');
        $('.xa-vip-headline').show();
        $('.xa-selectedProductList').empty();
        if(products.is_group){
            // 如果是全选， 显示选择条件
            for(var i=0; i< products.items_ids.length; ++i){
                $('.xa-selectedProductList').append("<span class='xa-vip-member-id' style='display:none;'>" +
                        products.items_ids[i].id+"</span>" );
            }
            // 显示分组查询条件
            for(var i=0; i< products.display_items.length; ++i){
                $('.xa-selectedProductList').append("<span class='xui-vip-username mr10 mb10'>"+products.display_items[i].name+"("+products.display_items[i].text+")"+"</span>");
            }
            $('.xa-selectedProductList').append("<div class='xa-vip-count' vip_count="+products.items_ids.length+">准备向"+products.items_ids.length+"人发放优惠券</div>");
        }else{
            // 如果是单选， 显示每个会员
            for(var i=0; i< products.items_ids.length; ++i){
                $('.xa-selectedProductList').append("<span class='xa-vip-username xui-vip-username mr10 mb10 pr'>"
                                                        +'<span>'+products.items_ids[i].username+'</span>'
                                                        +'<button class="xui-close xa-delete" type="button">'
                                                        +  '<span>x</span>'
                                                        +'</button>'
                                                        + "<span class='xa-vip-member-id' style='display:none;'>" + products.items_ids[i].id +"</span>"
                                                        +"</span>");
            }
            $('.xa-selectedProductList').append("<div class='xa-vip-count' vip_count="+products.items_ids.length+">准备向"+products.items_ids.length+"人发放优惠券</div>");
        }
    },
    onMouseenterShow:function(event){
    	$(event.target).find('.xa-delete').show();
    },

    onMouseenterhide:function(event){
    	$(event.target).find('.xa-delete').hide();
    },

    onClickDeleteProduct:function(event){
    	$(event.target).parents('.xa-vip-username').remove();
        var vip_count = parseInt($.trim(this.$el.find('.xa-vip-count').attr('vip_count'))) - 1;
        this.$el.find('.xa-vip-count').replaceWith("<div class='xa-vip-count' vip_count="+vip_count+">准备向"+vip_count+"人发放优惠券</div>");
    },

    validateIntegral: function(lower, upper){
        // 判断 lower, upper 是否同时为空， 或者同时
        // 为非负数！
        // 是返回: true
        // 否返回: false
        var validate_pattern = /^\d+$/;
        if(!lower && !upper){return true;}
        else if(lower && upper){
            return validate_pattern.test(lower) && validate_pattern.test(upper);
        }
    },

	onClickSearchButton: function(){
        var name = {}  // 会员名称
        name.name = $.trim(this.$('label[for="name"]').text()).split('：')[0];
		name.value = $.trim(this.$('[name="name"]').val());  // 会员名称
        name.text = $.trim(this.$('[name="name"]').val());  // 会员名称

        var grade_id = {} // 会员等级
        grade_id.name = $.trim(this.$('label[for="grade"]').text()).split('：')[0];
        grade_id.value = $.trim(this.$('[name="grade"]').val());  // 会员等级
        grade_id.text = $.trim(this.$('[name="grade"] :checked').text());

        var member_tag = {} // 会员分组
        member_tag.name = $.trim(this.$('label[for="member_tag"]').text()).split('：')[0];
        member_tag.value =  $.trim(this.$('[name="member_tag"]').val());  // 会员分组
        member_tag.text = $.trim(this.$('[name="member_tag"] :checked').text());

        var member_status = {} // 会员状态
        member_status.name = $.trim(this.$('label[for="status"]').text()).split('：')[0];
        member_status.value = $.trim(this.$('[name="status"]').val()); // 会员状态
        member_status.text = $.trim(this.$('[name="status"] :checked').text()); // 会员状态

        var member_source = {};
        member_source.name = $.trim(this.$('label[for="source"]').text()).split('：')[0];
        member_source.value = $.trim(this.$('[name="source"]').val()); // 会员来源
        member_source.text = $.trim(this.$('[name="source"] :checked').text()); // 会员来源
        // 积分范围过滤
        var integral = {}
        integral.name = $.trim(this.$('label[for="integral"]').text()).split('：')[0];
        var integral_lower = $.trim(this.$('[name="integral_lower"]').val());  // 积分下限
        var integral_upper = $.trim(this.$('[name="integral_upper"]').val());  // 积分下限

        if(!this.validateIntegral(integral_lower, integral_upper)){
            W.showHint('error', '积分请输入非负数!');
            return;
        }


        if(integral_upper&&integral_lower){
            integral.value = integral_lower + '-' + integral_upper;
            integral.text = integral_lower + '-' + integral_upper;
        }else{
            integral.value = '';
            integral.text = '';
        }
		var _this = this;
		W.dialog.showDialog('W.dialog.mall.SelectPromotionRedEnevlopDialog', 
                            {
                                name: name,
                                grade_id: grade_id,
                                member_tag: member_tag,
                                member_source: member_source,
                                member_status: member_status,
                                integral: integral,
                                success: function(data) {		
                                    // _this.addVipInfo(data);
                                    _this.trigger('finish-select-products', data);
                                },
                            });
	},

	onClickResetButton: function(){
        this.$('[name="name"]').val('');
        this.$('[name="grade"]').val(-1);
        this.$('[name="member_tag"]').val(-1);
        this.$('[name="status"]').val(-1);
        this.$('[name="source"]').val(-1);
        this.$('[name="integral_lower"]').val('');
        this.$('[name="integral_upper"]').val('')
	},
});

W.view.mall.RedAdvancedTable = W.view.common.AdvancedTable.extend({
    //     W.view.mall.RedAdvancedTable.__super__.load.call(this, from_goto, options);
    afterload:function(){
        var $allin =  $('.xa-allin:checked');
        $('.xui-selectUserDialog .xa-allin').parent().replaceWith('<label class="pa" style="right:25px;">' + 
            '<input class="xa-allin pr" style="top:3px;right:3px;" type="checkbox">' + 
            '筛选出来的' + this.paginationView.pageinfo.object_count + 
            '人(已取消关注的除外)</label>');
        if($allin.length==1){
            $('.xui-advancedTableContent :checkbox').attr('disabled', 'disabled').attr('checked', true);
            $('.xa-allin').prop('checked', true);
        }
    }
})

W.registerUIRole('div[data-ui-role="red-advanced-table"]', function() {
    var $div = $(this);
    var app = $div.attr('data-app');
    var api = $div.attr('data-api');
    var args = $div.attr('data-args');
    var template = $div.attr('data-template-id');
    var initSort = $div.attr('data-init-sort');
    var enablePaginator = !!($div.attr('data-enable-paginator') === 'true');
    var enableSort = !!($div.attr('data-enable-sort') === 'true');
    var sortApi = $div.attr('data-sort-api');
    var itemCountPerPage = $div.attr('data-item-count-per-page');
    var userWebappId = $div.attr('data-user-webapp-id');
    if (itemCountPerPage) {
        itemCountPerPage = parseInt(itemCountPerPage);
    } else {
        itemCountPerPage = 15;
    }

    var advancedTable = new W.view.mall.RedAdvancedTable({
        el: $div[0],
        template: template,
        app: app,
        api: api,
        args: args,
        initSort: initSort,
        itemCountPerPage: itemCountPerPage,
        enablePaginator: enablePaginator,
        enableSort: enableSort,
        sortApi: sortApi,
        userWebappId: userWebappId
    });
    advancedTable.render();

    $div.data('view', advancedTable);
});
