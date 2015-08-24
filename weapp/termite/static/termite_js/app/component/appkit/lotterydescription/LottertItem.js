/**
 * @class W.component.appkit.LottertItem
 * 奖项
 */
ensureNS('W.component.appkit');
W.component.appkit.LottertItem = W.component.Component.extend({
	type: 'appkit.lotteryitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		gropuClass: '',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '选项',
			isUserProperty: true,
			maxLength: 20,
			validate: 'data-validate="require-notempty::选项不能为空,,require-word::只能填入汉字、字母、数字"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: ''
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			$node.find('.xa-itemTitle').text(value);
		}
	}
});
