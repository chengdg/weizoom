/**
 * @class W.component.appkit.SurveyDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.LotteryDescription = W.component.Component.extend({
	type: 'appkit.lotterydescription',
	selectable: 'yes',
	propertyViewTitle: '微信抽奖',

	dynamicComponentTypes: [{
        type: 'appkit.lotteryitem',
        model: 3
    }],

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
			validate: 'data-validate="require-notempty::页面标题不能为空,,require-word::请输入除\' . \' , \' _ \'和\' $ \'以外的字符"',
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
		}, {
			name: 'delivery',
			type: 'text_with_annotation',
			displayName: '参与送积分',
			maxLength: 4,
			size: '70px',
			isUserProperty: true,
			default: ''
		}, {
			name: 'delivery_setting',
			type: 'radio',
			displayName: '送积分规则',
			isUserProperty: true,
			source: [{
				name: '仅限未中奖用户',
				value: 'true'
			}, {
				name: '所有用户',
				value: 'false'
			}],
			default: 'true'
		},{
			name: 'limitation',
			type: 'radio',
			displayName: '抽奖限制',
			isUserProperty: true,
			source: [{
				name: '一人一次',
				value: 'once_per_user'
			}, {
				name: '一天一次',
				value: 'once_per_day'
			}, {
				name: '一天两次',
				value: 'twice_per_day'
			}],
			default: 'once_per_user'
		},{
			name: 'chance',
			type: 'text_with_annotation',
			displayName: '中奖率',
			isUserProperty: true,
			maxLength: 3,
			size: '70px',
			annotation: "%  <b style='color:#1262b7' title='1.中奖概率'>中奖率详细规则</b>",
			validate: 'data-validate="require-notempty::中奖率不能为空,,require-percent::请输入1-100之间的数字"',
			validateIgnoreDefaultValue: true
		}, {
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
            isShowCloseButton: false,
            minItemLength: 3,
			maxItemLength: 3,
            isUserProperty: true,
            default: []
        }]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			$node.find('.xa-title').text(value);
		},
		description: function($node, model, value, $propertyViewNode) {
			console.log('------------------------------------');
			console.log($node[0]);
			console.log('------------------------------------');
			$node.find('.xa-description').html(value.replace(/\n/g,'<br>'));
		},
		delivery: function($node, model, value, $propertyViewNode) {
			$node.find('.wui-i-prize').html(value+'积分');
		},
		//delivery_setting: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-prize').html(value+'积分');
		//},
		//chance: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-prize').html(value+'积分');
		//},
		//type: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-prize').html(value+'积分');
		//},
		limitation: function($node, model, value, $propertyViewNode) {
			console.log('------------------------------------');
			console.log($node[0], value);
			console.log('------------------------------------');
			switch (value){
				case 'once_per_user':
					value = '1';
					break;
				case 'once_per_day':
					value = '1';
					break;
				case 'twice_per_day':
					value = '2';
					break;
				default :
					value = '0';
					break;
			}
			$node.siblings('.wui-lotterydescription').find('.xa-header p b').html(value);
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
