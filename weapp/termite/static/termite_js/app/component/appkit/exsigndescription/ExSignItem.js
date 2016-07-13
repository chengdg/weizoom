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
			var len = $node.find('.wui-rules-serial'+curr_id).length;
			if (value != ''){
				if (len >0){
					$node.find('.wui-rules .wui-rules-serial'+curr_id).show();
					$node.find('.wui-rules-serial'+curr_id+' .wui-rules-days').html('连续签到'+value+'天：');
				}else{
					$node.find('.wui-rules').append(
						'<div class="wui-rules-serial'+curr_id+'">' +
							'<div class="wui-rules-days fl">连续签到'+value+'天：</div>' +
							'<div class="wui-rules-rule fl">' +
								'<ul>' +
									'<li class="wui-rules-serial-point"></li>' +
									'<li class="wui-rules-serial-prizes"></li>' +
								'</ul>' +
							'</div>' +
						'<div class="wui-clearf"></div>');
				}
			}
		},
		serial_count_points: function($node, model, value, $propertyViewNode){
			var curr_id = $propertyViewNode.attr('data-dynamic-cid');
			var len = $node.find('.wui-rules-serial'+curr_id).length;
			if(value == ''){
				model.set('serial_count_points', 0);
				$propertyViewNode.find('input[data-field="serial_count_points"]').val('0');
				$node.find('.wui-rules-serial'+curr_id+' .wui-rules-prizes ul .wui-rules-serial-point').hide()
			}else{
				if (len > 0) {
					$node.find('.wui-rules-serial'+curr_id+' .wui-rules-rule ul .wui-rules-serial-point').html('获得'+value+'积分');
				}else{
					$node.find('.wui-rules').append(
						'<div class="wui-rules-serial'+curr_id+'">' +
							'<div class="wui-rules-days fl"></div>' +
							'<div class="wui-rules-rule fl">' +
								'<ul>' +
									'<li class="wui-rules-serial-point">获得'+value+'积分</li>' +
									'<li class="wui-rules-serial-prizes"></li>' +
								'</ul>' +
							'</div>' +
						'<div class="wui-clearf"></div>');
					$node.find('.wui-rules .wui-rules-serial'+curr_id).hide();
				}

			}
		},
		serial_count_prizes: function($node, model, value, $propertyViewNode){
			var curr_id = $propertyViewNode.attr('data-dynamic-cid');
			var len = $node.find('.wui-rules-serial'+curr_id).length;
			var coupon_str = '';
			for (var i in value){
				coupon_str += '<div>获得'+value[i].name+'</div>'
			}
			if (len > 0) {
					$node.find('.wui-rules-serial'+curr_id+' .wui-rules-rule ul .wui-rules-serial-prizes').html(coupon_str);
				}else{
					$node.find('.wui-rules').append(
						'<div class="wui-rules-serial'+curr_id+'">' +
							'<div class="wui-rules-days fl"></div>' +
							'<div class="wui-rules-rule fl">' +
								'<ul>' +
									'<li class="wui-rules-serial-point"></li>' +
									'<li class="wui-rules-serial-prizes">'+coupon_str+'</li>' +
								'</ul>' +
							'</div>' +
						'<div class="wui-clearf"></div>');
					$node.find('.wui-rules .wui-rules-serial'+curr_id).hide();
				}

		}
	}
});
