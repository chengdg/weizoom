/**
 * @class W.component.appkit.SignItem
 * 签到动态组件
 */
ensureNS('W.component.appkit');
W.component.appkit.SignItem = W.component.Component.extend({
	type: 'appkit.signitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		groupClass: '',
		fields: [{
			name: 'serial_count',
			type: 'text_with_annotation_v2',
			displayName: '连续签到',
			isUserProperty: true,
			maxLength: 5,
			size: '70px',
			annotation: '天',
			//validate: 'data-validate="require-notempty::选项不能为空,,require-nonnegative::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'serial_count_points',
			type: 'text_with_annotation_v2',
			displayName: '送积分',
			isUserProperty: true,
			maxLength: 5,
			size: '70px',
			annotation: '积分',
			//validate: 'data-validate="require-notempty::选项不能为空,,require-nonnegative::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'serial_count_prizes',
			type: 'prize_selector_v4',
			displayName: '送优惠券',
			isUserProperty: true,
			default:""
		}]
	}],

	propertyChangeHandlers: {

	}
});
