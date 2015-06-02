/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * shop message编辑面板
 * @class
 */
W.EditShopRulePanel = Backbone.View.extend({
	el: '#edit-shop-rule-panel',

	events: {
		'click #submit-btn': 'onSubmit',
        'change #shopSelect': 'onUpdatePhone',
        'change #displayCountSelect': 'onUpdatePhone'
	},
	
	initialize: function(options) {
		this.$el = $(this.el);

		/**
		 * 初始化模拟器
		 */
        this.phone = new W.common.EmbededPhoneView({
            el: $('#embeded-phone-box')
        });
        this.phone.render();

        this.categoryId = options.categoryId || -1;
        this.ruleId = options.ruleId || -1;
		this.productCategoryId = options.productCategoryId || -1;

        var onUpdatePhone = _.bind(this.onUpdatePhone, this);
        this.categories = new W.ProductCategories();
        this.categories.bind('add', this.addProductCategory, this);
        this.categories.fetch({
            success: function(collection, resp) {
               if (this.productCategoryId != -1) {
                   onUpdatePhone(null, true);
               }
            }
        });

        this.categorySelect = $('#shopSelect');

        this.optionTmpl = new W.Template('<option value="${value}">${name}</option>');
        this.selectedOptionTmpl = new W.Template('<option value="${value}" selected="selected">${name}</option>');
    },

    /**
     * 加载shop的分类
     */
    addProductCategory: function(category, collection, resposne) {
        var context = {
            name: category.get('name'),
            value: category.get('id')
        };

        var tmpl = this.optionTmpl;
        if (category.get('id') == this.productCategoryId) {
            tmpl = this.selectedOptionTmpl;
        }

        this.categorySelect.append(tmpl.render(context));
    },

    /**
     * 响应改变category或display count的函数，更新微信模拟器中的显示
     * @param event
     */
    onUpdatePhone: function(event, hideNewTag) {
        var categoryIds = $("#shopSelect").val();
        if (!categoryIds || categoryIds.length == 0) {
            //没有选中category，直接返回
            return;
        }

        var categoryId = categoryIds[0];
        var category = this.categories.get(categoryId);
        var displayCount = parseInt($('#displayCountSelect').val());

        category.getProducts(function(products) {
            if (hideNewTag) {
                category.flushProducts();
            }
            this.updatePhone(products, displayCount);
            category.renewProducts();
        }, this);
    },

    /**
     * 更新微信模拟器显示
     * @param newses
     * @param displayCount
     */
    updatePhone: function(newses, displayCount, patterns) {
        if (!newses) {
            return;
        }

        //清空微信模拟器
        this.phone.reset();

        this.phone.disableRefresh();

        //添加接收到的文本
        if (!patterns) {
            patterns = $.trim($('#patterns').val());
        }
        if (patterns) {
            var pattern = patterns.split('|')[0];
            if (pattern) {
                var message = W.common.Message.createTextMessage();
                message.set('text', pattern);
                this.phone.receiveTextMessage(message);
            }
        }

        //添加发出的news
        var count = newses.length;
        for (var i = 0; i < count; ++i) {
            if (i >= displayCount) {
                //控制显示数量
                break;
            }

            var news = newses[i];
            var newsMessage = W.common.Message.createNewsMessage();
            newsMessage.set(news);
            if (0 == i) {
                this.phone.addNews(newsMessage);
            } else {
                this.phone.appendNews(newsMessage);
            }
        }
        this.phone.enableRefresh();
        this.phone.refresh();
    },

	/**
	 * 提交按钮的响应函数
	 * @param event
	 */
	onSubmit: function(event) {
        if (!W.validate()) {
            return;
        }
		var patternsInput = $('#patterns');
		var patterns = $.trim(patternsInput.val());

        var categoryId = $("#shopSelect").val()[0];
        var displayCount = parseInt($('#displayCountSelect').val());
        var answer = JSON.stringify({
            category_id: categoryId,
            display_count: displayCount
        });

        var api = 'shop_rule/update'
        if (this.ruleId == -1) {
            api = 'shop_rule/add';
        }

        W.getLoadingView().show();
		var task = new W.DelayedTask(function() {
			W.getApi().call({
				app: 'qa',
				api: api,
				method: 'post',
				args: {
					rule_id: this.ruleId,
	                category_id: this.categoryId,
					answer: answer,
					patterns: patterns
				},
				success: function(rule) {
                    window.location.href = '/qa/rules/'+this.categoryId+'/';
				},
				error: function(response) {
                    alert('添加规则失败');
	                W.getLoadingView().hide();
				},
				scope: this
			});
		}, this);
		task.delay(300);
	}
});