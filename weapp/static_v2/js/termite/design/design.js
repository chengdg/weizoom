/*
Copyright (c) 2011-2012 Weizoom Inc
*/
_.extend(W, {
	workbench: {dialog:{}},
	mobile: {},
	model: {},
	component: {jqm:{}, viper:{}},
	data: {mobile:{}, viper:{}},
	design: {},
	util: {
		$M:null, //$M是iframe中的jQuery
		mobilePageDragComponentHandler: $.noop,
		changeComponentInDesignPageHandlers: [], //design page中切换component的响应函数集合
		getInsertIndicatorLayoutInMobilePage: $.noop
	},
	view: {
		cssEditorView: null,
	}
});

//ImagePositions: 图标位置
W.data.ImagePositions = [
    {img: 'icon-circle-arrow-left', value: 'left'},
    {img: 'icon-circle-arrow-up', value: 'top'},
    {img: 'icon-circle-arrow-down', value: 'bottom'},
    {img: 'icon-circle-arrow-right', value: 'right'},
];

W.data.ThemeSwatchs = [
	{name:'Default', value:''}, 
	{name:'Swatch A', value:'a'}, 
	{name:'Swatch B', value:'b'}, 
	{name:'Swatch C', value:'c'}, 
	{name:'Swatch D', value:'d'},
	{name:'Swatch E', value:'e'},
	{name:'Swatch X', value:'x'}
];
W.data.getWorkbenchPages = function() {
    var items = [{name: '选择页面...', value: '#'}, {name: '上一页面', value: 'page-$back$'}];
    _.each(W.data.pageManager.getPages(), function(page) {
        items.push({name: page.model.get('title'), value: "page-"+page.cid});
    });
    return items;
}
W.data.getEntityProperty = function(component) {
	var pageCid = component.model.get('target').split('-')[1];
	if (!pageCid) {
		return [];
	}

	if (pageCid[0] == '$') {
		return [];
	}

	return W.data.getWorkbenchPageFields(pageCid);
}
W.data._extractComponentFields = function(component, items) {
	var sub_component_count = component.components ? component.components.length : 0;
	if (sub_component_count === 0) {
		var field = component.model.get('name');
		if (field) {
			items.push({name: field, value: field});
		}
	} else {
		var field = component.model.get('name');
		if (field) {
			items.push({name: field, value: field});
		}
		_.each(component.components, function(sub_component) {
			W.data._extractComponentFields(sub_component, items);
		});	
	}
}
W.data.getWorkbenchPageFields = function(cid) {
	var items = [{name: '选择属性...', value: '#'}];
	var page = W.data.pageManager.getPageByCid(cid);
	W.data._extractComponentFields(page, items);

	items.push({name: 'created_at', value: 'created_at'})
	return items;
}
W.data.getCurrentPageFields = function() {
	return W.data.getWorkbenchPageFields(W.workbench.PageManagerView.currentActivePage.cid);
}
W.data.getWorkbenchPageFields_bak = function(cid) {
	var items = [{name: '选择属性...', value: '#'}];
	var page = W.data.pageManager.getPageByCid(cid);
	_.each(page.components, function(component) {
		var field = component.model.get('name');
		if (field) {
			items.push({name: field, value: field});
		}
	});

	return items;
}
W.data.getDatasourcePages = function() {
	return [];
	//return W.data.datasourceProjectPages;
}

// 根据动态对话框的类型选择html代码，嵌入field代码部分(在workbench_property_view/template.html中用)
W.data.getDynamicComponentDataForDialogSelectControl = function(dynamicComponent, dynamicComponentField) {
	var html = "";
	if (dynamicComponentField.dialog === 'W.dialog.workbench.SelectLinkTargetDialog') {
		var value = dynamicComponent.model.get(dynamicComponentField.name, "");
		if (value.length > 0) {
			html = '<span class="x-targetText" style="color: blue;">'+$.parseJSON(dynamicComponent.model.get(dynamicComponentField.name))['data_path']+'</span>';
		} else {
			html = '<span class="x-targetText" style="color: blue;"></span>';
		}
	} else if (dynamicComponentField.dialog === 'W.workbench.SelectImageDialog') {
		var src = dynamicComponent.model.get(dynamicComponentField.name);
		if (src.length > 0) {
			html = '<div class="dynamicComponentControlImgBox"><img src="' + src +'" width="90"/></div>';
		} else {
			html = '<div class="dynamicComponentControlImgBox xui-hide"><img src="" width="90"/></div>';;
		}
	} else if (dynamicComponentField.dialog === 'W.dialog.workbench.SelectColorDialog') {
		var color = dynamicComponent.model.get(dynamicComponentField.name, '');
		if ((color.length > 0) && (color !== 'none')) {
			html = '<div class="x-dynamicComponentColorField xa-dynamicComponentColorField mb5" style="width: 30px; height: 30px; background-color:#'+color+'"></div>';	
		} else {
			html = '<div class="x-dynamicComponentColorField xa-dynamicComponentColorField xa-noneColor"></div>';	
		}		
	} else if (dynamicComponentField.dialog === 'W.dialog.workbench.SelectNavIconDialog') {
		var icon = dynamicComponent.model.get(dynamicComponentField.name, '');
		if (icon.length > 0) {
			html = '<div class="x-dynamicComponentIconField" style="width: 60px; height: 60px; background-color: #AAAAAA; background-image: url('+icon+')"></div>';
		} else {
			html = '<div class="x-dynamicComponentIconField"></div>';
		}
	} else if (dynamicComponentField.dialog === 'W.dialog.termite.SelectCategoriesDialog') {
		var value = dynamicComponent.model.get(dynamicComponentField.name, "");
		if (value.length > 0) {
			html = '<span class="xui-categoryName xa-categoryName" style="display:inline-block;">'+$.parseJSON(dynamicComponent.model.get(dynamicComponentField.name))[0]['title']+'</span>';
		} else {
			html = '<span class="xui-categoryName xa-categoryName xui-hide"></span>';
		}
	} else if (dynamicComponentField.dialog === 'W.dialog.termite.SelectImagesDialog') {
		var src = dynamicComponent.model.get(dynamicComponentField.name);
		if (src.length > 0) {
			if (dynamicComponent.type === 'appkit.lotteryitem' || dynamicComponent.type === 'appkit.imageitem'){
				html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox"><img src="' + src + '"/></div>';
			}else {
				html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox"><img src="' + src + '"/><button type="button" class="close xa-protocol-deleteData xui-removeImageButton" data-protocol-deleted-value=""><span>&times;</span></button></div>';
			}
		} else {
			if (dynamicComponent.type === 'appkit.lotteryitem' || dynamicComponent.type === 'appkit.powermedescription' || dynamicComponent.type === 'appkit.imageitem'){
				html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox xui-hide"><img src=""/></div>';
			}
			else {
				html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox xui-hide"><img src=""/><button type="button" class="close xa-protocol-deleteData xui-removeImageButton"  data-protocol-deleted-value=""><span>&times;</span></button></div>';
			}
		}
	} else if (dynamicComponentField.dialog === 'W.dialog.termite.SelectQrcodeDialog') {
		var qrcode = dynamicComponent.model.get(dynamicComponentField.name);
		if (qrcode['ticket'] != '') {
			html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox xa-qrcodeImgBox"><img src="'+ qrcode.ticket +'"/></div><div class="qrcodeName">'+qrcode.name+'</div>';
		} else {
			html = '<div class="xui-dynamicComponentControlImgBox xa-dynamicComponentControlImgBox xa-qrcodeImgBox xui-hide"><img src=""/></div><div class="qrcodeName"></div>';
		}
	}else if (dynamicComponentField.dialog === 'W.dialog.termite.SelectProductDialog') {
        var product = dynamicComponent.model.get(dynamicComponentField.name);

        if (product.productId != "") {
			html = '<table class="table table-bordered xb-stripedTable xa-productTable propertyGroup_property_dialogSelectField  xa-productList"><thead style="background:#c8d2e5;"><tr><th width="165">商品信息</th><th width="105">商品价格(元)</th><th width="70">总销量</th></tr></thead><tbody><tr data-id="${product.id}"><td class="text_nowrap" style="min-width:180px;"><img class="productImg" id="productImg" style="width: 60px;height: 60px;float: left;margin: 2px;" src="'+product.productImg+'"><p class="productName" style="color: #1360B8;width: 95px;float: left;text-align: left;padding-left: 0.5rem;word-wrap: break-word;word-break: break-all;white-space: normal;">'+product.productName+'</p><p class="productBarCode" style="line-height: 16px;color: #676767;width: 95px;float: left;text-align: left;">商品编码:'+product.productBarcode+'</p></td><td class="productPrice" >'+product.productPrice+'</td><td class="productSocks">'+product.productSocks+'</td></tr></tbody></table>';
        } else {
			html = '<table class="table table-bordered xb-stripedTable xa-productTable propertyGroup_property_dialogSelectField  xa-productList xui-hide"><thead style="background:#c8d2e5;"><tr><th width="165">商品信息</th><th width="105">商品价格(元)</th><th width="70">总销量</th></tr></thead><tbody><tr data-id="${product.id}"><td class="text_nowrap" style="min-width:180px;"><img class="productImg" id="productImg" style="width: 60px;height: 60px;float: left;margin: 2px;" src="'+product.productImg+'"><p class="productName" style=";color: #1360B8;width: 95px;float: left;text-align: left;padding-left: 0.5rem;word-wrap: break-word;word-break: break-all;white-space: normal;">'+product.productName+'</p><p class="productBarCode" style="line-height: 16px;color: #676767;width: 95px;float: left;text-align: left;">商品编码:'+product.productBarcode+'</p></td><td class="productPrice" >'+product.productPrice+'</td><td class="productSocks">'+product.productSocks+'</td></tr></tbody></table>';
		}
    }

	return html;
};

W.data.TextInputType = [
	{name: 'Text', value: 'text'},
	{name: 'Password', value: 'password'},
	{name: 'Email', value: 'email'},
	{name: 'Url', value: 'url'},
	{name: 'Phone Number', value: 'tel'}
];

W.data.DatePickerType = [
	{name: 'Date', value: 'date'},
	{name: 'Time', value: 'time'},
	{name: 'Month', value: 'month'},
	{name: 'Week', value: 'week'},
	{name: 'Datetime', value: 'datetime'}
];

W.data.RadioButtonOrientations = [
    {name: '水平方向', value: 'horizontal'},
	{name: '垂直方向', value: 'vertical'}
];

W.data.ButtonIcons = [
	{name: '选择图标...', value: ''},
	{name: '加号', value: 'plus'},
	{name: '减号', value: 'minus'},
	{name: '删除', value: 'delete'},
	{name: '左箭头', value: 'arrow-l'},
	{name: '右箭头', value: 'arrow-r'},
	{name: '上箭头', value: 'arrow-u'},
	{name: '下箭头', value: 'arrow-d'},
	{name: '选中', value: 'check'},
	{name: '配置', value: 'gear'},
	{name: '刷新', value: 'refresh'},
	{name: '向前', value: 'forward'},
	{name: '向后', value: 'back'},
	{name: '网格', value: 'grid'},
	{name: '星号', value: 'star'},
	{name: '警告', value: 'alert'},
	{name: '信息', value: 'info'},
	{name: 'Home', value: 'home'},
	{name: '搜索', value: 'search'},
	{name: '列表', value: 'bars'},
	{name: '编辑', value: 'edit'},
]

W.data.PanelDisplayModes = [
	{name: 'Reveal', value: 'reveal'},
	{name: 'Overlay', value: 'overlay'},
	{name: 'Push', value: 'push'}
]

W.data.PanelPositions = [
	{name: 'Left', value: 'left'},
	{name: 'Right', value: 'right'},
]

W.data.FixedPositions = [
	{name: '不固定', value: 'none'},
	{name: '顶部', value: 'top'},
	{name: '底部', value: 'bottom'},
]

W.data.getIntegerRanges = function(from, to) {
	var func = function() {
		var items = [];
		for (var i = from; i <= to; ++i) {
			var iStr = i + '';
			items.push({name: iStr, value: iStr});
		}

		return items;
	}

	return func;
}


// 扩展underscore
_.deepClone = function(obj) {
	if (!_.isObject(obj)) return obj;
	if (_.isFunction(obj)) return obj;
	var isArr = (_.isArray(obj) || _.isArguments(obj));
	var func = function (memo, value, key) {
		if (isArr) {
			memo.push(_.deepClone(value));
		} else {
			memo[key] = _.deepClone(value);
		}
		return memo;
	};
	return _.reduce(obj, func, isArr ? [] : {});
}

// 系统错误码