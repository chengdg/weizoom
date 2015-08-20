/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.SelectItem = W.component.Component.extend({
	type: 'appkit.selectitem',
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
			validate: 'data-validate="require-notempty::选项不能为空,,require-letter::只能填入字母、数字、下划线"',
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
