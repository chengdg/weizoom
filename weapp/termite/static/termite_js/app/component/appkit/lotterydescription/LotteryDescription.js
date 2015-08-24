/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.LotteryDescription = W.component.Component.extend({
	type: 'appkit.lotterydescription',
	selectable: 'yes',
	propertyViewTitle: '微信抽奖',

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-TextSurvey',
		fields: [
		//	{
		//	name: 'type',
		//	type: 'radio',
		//	displayName: '微信抽奖',
		//	isUserProperty: true,
		//	validateIgnoreDefaultValue: true,
		//	source: [{
		//		name: '刮刮乐',
		//		value: 'scratch',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-scratch'
		//	}, {
		//		name: '大转盘',
		//		value: 'roulette',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-roulette'
		//	}, {
		//		name: '微信红包',
		//		value: 'red',
		//		img: 'xui-propertyView-radioGroup xui-i-lottery-red'
		//	}],
		//	default: {roulette:{select:true}}
		//},
			{
			name: 'title',
			type: 'text',
			displayName: '活动标题',
			isUserProperty: true,
			maxLength: 20,
			validate: 'data-validate="require-notempty::页面标题不能为空,,require-word::只能填入汉字、字母、数字"',
			validateIgnoreDefaultValue: true,
			default: '',
			placeholder: '活动标题'
		}, {
			name: 'start_time',
			type: 'hidden',
			displayName: '开始时间',
			isUserProperty: false,
			default: ''
		}, {
			name: 'end_time',
			type: 'hidden',
			displayName: '结束时间',
			isUserProperty: false,
			default: ''
		}, {
			name: 'valid_time',
			type: 'date_range_selector',
			displayName: '有效时间',
			isUserProperty: true,
			validate: 'data-validate="require-notempty::有效时间不能为空"',
			validateIgnoreDefaultValue: true,
			default: ''
		}, {
			name: 'description',
			type: 'textarea',
			displayName: '活动说明',
			maxLength: 200,
			isUserProperty: true,
			default: ''
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		description: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		start_time: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		},
		end_time: function($node, model, value, $propertyViewNode) {
			this.refresh($node, {resize:true});
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
