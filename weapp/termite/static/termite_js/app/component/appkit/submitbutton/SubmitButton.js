/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.SubmitButton = W.component.Component.extend({
	type: 'appkit.submitbutton',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		groupClass: '',
		fields: [{
			name: 'text',
			type: 'text',
			displayName: '文字',
			isUserProperty: false,
			default: "提交"
		}]
	}],

	propertyChangeHandlers: {
	}
});
