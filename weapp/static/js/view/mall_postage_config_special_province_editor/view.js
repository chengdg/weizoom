/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 一个微信会话的view
 * @constructor
 */
ensureNS('W.view.mall');
W.view.mall.PostageConfigSpecialProvinceEditor = Backbone.View.extend({
	getTemplate: function() {
		$('#mall-postage-config-special-province-editor-tmpl-src').template('mall-postage-config-special-province-editor-tmpl');
		return 'mall-postage-config-special-province-editor-tmpl';
	},

	getValueTemplate: function() {
		$('#mall-postage-config-special-province-editor-province-select-tmpl-src').template('mall-postage-config-special-province-editor-province-select-value-tmpl');
		return 'mall-postage-config-special-province-editor-province-select-value-tmpl';
	},
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.template = this.getTemplate();
		this.valueTemplate = this.getValueTemplate();
		this.cid = -1;
		this.values = options.values;
		var checked_values = [];
		for (v in this.values) {
			var provinces = this.values[v].province;
			var province_names = [];
			var province_values = [];
			for (p in provinces) {
				province_names.push(provinces[p].name);
				province_values.push(provinces[p].id);
				checked_values.push(provinces[p].id+'');
			}
			this.values[v].province_names = province_names.join('，')
			this.values[v].province_values = province_values.join(',')
		}
		this.isImageMode = options.initImageMode;
		this.areaDataCache = '';
		this.areaSelectView = W.getPostAreaSelectView();
		this.areaSelectView.checkedValue = checked_values;
	},
	
	events: {
		'click .xa-addValueBtn': 'onClickAddValueButton',
		'click .xa-removeValueBtn': 'onClickRemoveValueButton',
		'click .xa-selectIcon': 'onClickSelectIconLink',
		'click .xa-changeIcon': 'onClickChangeIconLink',
		'keypress input[type="text"]': 'onPressKeyInInput',
		'click .xa-areaSelect': 'selectArea'
	},
	
	selectArea: function(event) {
		if (!this.areaDataCache) {
			var _this = this;
			W.getApi().call({
	            app: 'tools',
	            api: 'regional/provinces',
	            success: function(data) {
	            	_this.areaDataCache = data;
	            	// W.dialog.showDialog('W.weapp.dialog.PostageAreaDialog', {})
	            	_this.areaSelectView.show({
	            		$action: $(event.currentTarget),
	            		data: _this.areaDataCache

	            	});
	            },
	            error: function(response) {
	            	alert('获取数据失败！');
	            }
	        });
		} else {
			this.areaSelectView.show({
	    		$action: $(event.currentTarget),
	    		data: this.areaDataCache
	    	});
		}
		
	},

	render: function() {
		this.$el.html($.tmpl(this.template, {values: this.values, isImageMode: this.isImageMode}));
	},

	onClickAddValueButton: function(event) {
		var $node = $.tmpl(this.valueTemplate, {cid: this.cid, isImageMode: this.isImageMode});
		this.$('tbody').append($node);
		$node.find('input[type="text"]').focus();
		this.cid -= 1;
		event.stopPropagation();
	},

	onClickRemoveValueButton: function(event) {
		var $btn = $(event.currentTarget);
		$btn.parents('tr').eq(0).remove();
		event.stopPropagation();
	},

	onClickSelectIconLink: function(event) {
		var $link = $(event.currentTarget);
		W.dialog.showDialog('W.dialog.common.SelectUserIconDialog', {
			success: function(data) {
				var $td = $link.parents('td');
				$td.find('input[type="hidden"]').val(data);
				$td.find('img').attr('src', data);
				$td.find('.xa-selectZone').hide();
				$td.find('.xa-imageZone').show();
			}
		});
	},

	onClickChangeIconLink: function(event) {
		var $link = $(event.currentTarget);
		var $td = $link.parents('td');
		$td.find('input[type="hidden"]').val('');
		$td.find('.xa-imageZone').hide();
		$td.find('.xa-selectZone').show();
		
		W.dialog.showDialog('W.dialog.common.SelectUserIconDialog', {
			success: function(data) {
				$td.find('input[type="hidden"]').val(data);
				$td.find('img').attr('src', data);
				$td.find('.xa-selectZone').hide();
				$td.find('.xa-imageZone').show();
			}
		});
	},

	onPressKeyInInput: function(event) {
		var keyCode = event.keyCode;
        if(keyCode === 13) {
            event.stopPropagation();
            event.preventDefault();
        }
	},

	enterImageValueMode: function(event) {
		this.$('.xa-imageColumn').show();
		this.isImageMode = true;
	},

	enterTextValueMode: function(event) {
		this.$('.xa-imageColumn').hide();
		this.isImageMode = false;
	}
});

W.PostageAreaSelectView = W.DropBox.extend({
	SUBMIT_EVENT: 'submit',
	
	CLOSE_EVENT: 'close',
	
	isArrow: true,
	
	isTitle: false,

	position: 'down-left',
	
	events:{
		'click .xa-submit': 'submit'
	},
	
	submit: function() {
		var selectedCheckboxStr = this.$action.attr('data-value') || '';
		var selectedCheckboxValues = selectedCheckboxStr.split(',');
		for (i in selectedCheckboxValues) {
			delete this.checkedValue[this.checkedValue.indexOf(selectedCheckboxValues[i]+'')];
		}
		
		var checkboxs = this.$('input[name="PostageAreaType"]');
		var provinces = [];
		var dataValues = [];
		var _this = this;
		checkboxs.each(function() {
			if ($(this).attr('checked')) {
				var province = $(this).attr('data-name');
				var dataValue = $(this).attr('data-value');
				_this.checkedValue.push(dataValue);
				provinces.push(province);
				dataValues.push(dataValue);
			}
		})
		provinces = provinces.join('，');
		dataValues = dataValues.join(',');
		this.$action.val(provinces);
		this.$action.attr('data-value', dataValues);
		this.$action.parents('td:eq(0)').find('.xa-areaSelectValue').val(dataValues);
		this.hide();
	},
	
	getTemplate: function(data) {
		return '<div class="xa_info xui-area-container" style="width: 700px;padding-top:15px;"></div>';
	},

	initializePrivate: function(options) {
		this.$el = $(this.el);
		this.checkedValue = [];
		this.render(options);
	},
	
	render: function(data) {
		html = this.getTemplate(data);
		this.$content.html(html);
	},
	
	showPrivate: function(options) {
		this.$('.xa_info').html(this.getPrivateTemplate(options));
		// this.setPosition();
	},
	
	getPrivateTemplate: function(data) {
		var selectedCheckboxStr = this.$action.attr('data-value') || '';
		var selectedCheckboxValues = selectedCheckboxStr.split(',');
		// for (i in selectedCheckboxValues) {
			// delete this.checkedValue[this.checkedValue.indexOf(selectedCheckboxValues[i]+'')];
		// }
		var data = data.data || [];
		var html = '';
		for (i in data) {
			if (selectedCheckboxValues.indexOf(i+'')>-1) {
				html += '<label class="checkbox inline" style="width: 200px"><input type="checkbox" checked="true" data-name="'+data[i]+'" data-value="'+i+'" name="PostageAreaType"><span style="margin-left: -65px;" class="checkbox">'+data[i]+'</span></label>';
			} else{
				if (this.checkedValue.indexOf(i+'')>-1 ){
					html += '<label class="checkbox inline" style="width: 200px"><input type="checkbox" disabled data-name="'+data[i]+'" data-value="'+i+'" name="PostageAreaType"><span style="margin-left: -65px;" class="checkbox">'+data[i]+'</span></label>';
				} else {
					html += '<label class="checkbox inline" style="width: 200px"><input type="checkbox" data-name="'+data[i]+'" data-value="'+i+'" name="PostageAreaType"><span style="margin-left: -65px;" class="checkbox">'+data[i]+'</span></label>';
				}
			}
			
		}
		html += '<div class="tc mt10 mb10"><button class="btn btn-success xa-submit">确定</button></div>';
		return html;
	},
	
	closePrivate: function() {
		this.$('.tx_submit').bottonLoading({status:'hide'});
		this.trigger(this.CLOSE_EVENT);
	}
});

W.getPostAreaSelectView = function(options) {
	var dialog = W.registry['PostageAreaSelectView'];
	if (!dialog) {
		//创建dialog
		xlog('create PostageAreaSelectView');
		dialog = new W.PostageAreaSelectView(options);
		W.registry['PostageAreaSelectView'] = dialog;
	}
	return dialog;
};

W.registerUIRole('[data-ui-role="postage-config-special-province-editor"]', function() {
    var $container = $(this);
    var values = $.parseJSON($container.attr('data-values'));
    var initImageMode = ($.trim($container.attr('data-init-image-mode')) === 'true');
    var view = new W.view.mall.PostageConfigSpecialProvinceEditor({
        el: this,
        values: values,
        initImageMode: initImageMode
    });
    view.render();

    $container.data('view', view);
});