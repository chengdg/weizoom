/**
 * @class W.component.appkit.SignItem
 * 签到动态组件
 */
ensureNS('W.component.appkit');
W.component.appkit.ExSignItem = W.component.Component.extend({
	type: 'appkit.exsignitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		groupClass: 'xa-serial-points-settings',
		fields: [{
			name: 'serial_count',
			type: 'text_with_annotation_v2',
			displayName: '连续签到',
			isUserProperty: true,
			maxLength: 5,
			size: '70px',
			annotation: '天',
			validate: 'data-validate="require-notempty::选项不能为空,,require-nonnegative::只能填入数字"',
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
			default: '0'
		},{
			name: 'serial_count_prizes',
			type: 'prize_selector_v5',
			displayName: '送优惠券',
			isUserProperty: true,
			default:[]
		}]
	}],

	propertyChangeHandlers: {
		serial_count: function($node, model, value, $propertyViewNode){
			var curr_id = $propertyViewNode.attr('data-dynamic-cid');
			$node.find('.wui-rules-serial'+curr_id).find('.wui-rules-days span').text(value);
		},
		serial_count_points: function($node, model, value, $propertyViewNode){
			var curr_id = $propertyViewNode.attr('data-dynamic-cid');
			$node.find('.wui-rules-serial'+curr_id).find('.wui-rules-serial-point span').text(value);
		},
		serial_count_prizes: function($node, model, value, $propertyViewNode){
			var curr_id = $propertyViewNode.attr('data-dynamic-cid');
			var coupon_str = '';
			for (var i in value){
				coupon_str += '<div>获得'+value[i].name+'</div>';
			}
			$node.find('.wui-rules-serial'+curr_id).find('.wui-rules-serial-prizes').html(coupon_str);
		}
	}
});
