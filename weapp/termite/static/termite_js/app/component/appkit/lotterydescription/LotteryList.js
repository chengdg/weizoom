/**
 * @class W.component.appkit.LotteryList
 * 奖项设置
 */
ensureNS('W.component.appkit');
W.component.appkit.LotteryList = W.component.Component.extend({
	type: 'appkit.lotterylist',
	selectable: 'yes',
	propertyViewTitle: '',

	dynamicComponentTypes: [{
        type: 'appkit.lotterylist',
        model: 3
    }],

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-LotteryList',
		fields: [{
			name: 'chance',
			type: 'text',
			displayName: '中奖率',
			isUserProperty: true,
			maxLength: 3,
			validate: 'data-validate="require-notempty::中奖率不能为空,,require-percent::请输入1-100之间的数字"',
			validateIgnoreDefaultValue: true
		}, {
			name: 'instruction',
			type: 'pure-text',
			text: '中奖率',
			isUserProperty: true
		},{
			name: 'type',
			type: 'radio',
			displayName: '重复中奖',
			isUserProperty: true,
			source: [{
				name: '是',
				value: 'true'
			}, {
				name: '否',
				value: 'false'
			}],
			default: 'true'
		}, {
            name: 'items',
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 2,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		chance: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		type: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		items: function($node, model, value) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
        }
	}
}, {
	indicator: {
		name: '文本调研',
		imgClass: 'componentList_component_product_list' // 控件icon
	}
});
