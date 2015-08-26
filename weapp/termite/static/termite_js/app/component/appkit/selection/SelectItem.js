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
			validate: 'data-validate="require-notempty::选项不能为空,,require-word::请输入除\' . \' , \' _ \'和\' $ \'以外的字符"',
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
