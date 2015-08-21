/**
 * @class W.component.appkit.TextItem
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.TextItem = W.component.Component.extend({
	type: 'appkit.textitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		gropuClass: '',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '填写项',
			isUserProperty: true,
			maxLength: 20,
			validate: 'data-validate="require-notempty::选项不能为空,,require-word::只能填入汉字、字母、数字"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: ''
		},{
			name: 'is_mandatory',
			type: 'radio',
			displayName: '是否必填',
			isUserProperty: true,
			source: [{
				name: '是',
				value: 'true'
			}, {
				name: '否',
				value: 'false'
			}],
			default: 'false'
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			console.log('=======================11');
			console.log($node);
			$node.find('.wui-i-label').text(value);
			$node.find('.wui-i-input').attr("placeholder", "请输入" + value);
		},
		is_mandatory: function($node, model, value, $propertyViewNode) {
			if("true" === value){
				$node.find('.wui-i-label ').addClass('xui-mandatory');
			}else{
				$node.find('.wui-i-label ').removeClass('xui-mandatory');
			}
		}
	}
});
