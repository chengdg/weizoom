/**
 * @class W.component.appkit.LottertItem
 * 奖项
 */
ensureNS('W.component.appkit');
W.component.appkit.EggItem = W.component.Component.extend({
	type: 'appkit.eggitem',
	selectable: 'no',
	propertyViewTitle: '',

	properties: [{
		group: '',
		gropuClass: '',
		fields: [{
			name: 'title',
			type: 'text',
			displayName: '奖项名称',
			isUserProperty: true,
			default: ''
		},{
			name: 'prize_count',
			type: 'text_with_annotation',
			displayName: '奖品总数',
			isUserProperty: true,
			maxLength: 5,
			size: '70px',
			annotation: '个 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;剩余：<b class="xa-leftCount" style="color:red">0</b>&nbsp;&nbsp;个',
			validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'prize',
			type: 'prize_selector_v3',
			displayName: '活动奖励',
			isUserProperty: true,
			default: {type:"integral", data:0}
		}]
	}],

	propertyChangeHandlers: {
		title: function($node, model, value, $propertyViewNode) {
			var currCid = $propertyViewNode.attr('data-dynamic-cid');
			var bak;
			switch (currCid){
				case '4':
					bak = '一等奖';
					break;
				case '5':
					bak = '二等奖';
					break;
				case '6':
					bak = '三等奖';
					break;
				default:
					bak = '';
					break;
			}
			$propertyViewNode.find('input').eq(0).val(bak);
		},
		prize: function($node, model, value, $propertyViewNode) {
			var data_cid = $propertyViewNode.attr('data-dynamic-cid');
			var $li_b = $node.find('.wui-i-settingData li[data_cid="' + data_cid + '"]').find('p');
			if(value && value.data) {
				if (value.type == 'coupon') {
					$li_b.html(value.data.name);
				} else {
					if (value.type == 'integral') {
						$li_b.html(value.data + ' 积分');
					} else if (value.type == 'entity') {
						$li_b.html(value.data);
					}
				}
			}else{
				if (value.type == 'integral') {
					$li_b.html('' + ' 积分');
				}else{
					$li_b.html('');
				}

			}
		},
		prize_count:function($node, model, value, $propertyViewNode) {
			var total_prize_count = parent.window.total_prize_count;
			var prize_title = $propertyViewNode.find('input[data-field="title"]').val();
			var prize_count = total_prize_count[prize_title]['total_prize_count'];
			var left_count = total_prize_count[prize_title]['left_count'];
			if (total_prize_count['status'] == "进行中"){
				$propertyViewNode.find('input[data-field="prize_count"]').attr('data-validate','"require-notempty::选项不能为空,,require-natural::只能填入数字,,require-countcontrol::请输入大于"'+total_prize_count[prize_title]['control_prize_count']+'"的数字"');
			}
			if ((/^[0-9]*$/g).exec(value) != null){
				var leftCount = Number(value) - Number(prize_count) + Number(left_count);
				if (leftCount == -1){
					$propertyViewNode.find('.xa-leftCount').text(0);
				} else{
					$propertyViewNode.find('.xa-leftCount').text(leftCount);
				}
				total_prize_count[prize_title]['total_prize_count'] = value;
				total_prize_count[prize_title]['left_count'] = leftCount;
				model.set({prize_count: value},{silent: true});
			}
		}
	}
});
