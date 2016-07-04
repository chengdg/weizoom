/**
 * @class W.component.appkit.ExlottertItem
 * 奖项
 */
ensureNS('W.component.appkit');
W.component.appkit.ExlottertItem = W.component.Component.extend({
	type: 'appkit.exlotteryitem',
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
			validate: 'data-validate="require-natural::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: '0'
		},{
			name: 'prize',
			type: 'prize_selector_v3',
			displayName: '活动奖励',
			isUserProperty: true,
			default: {type:"integral", data:0}
		},{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '上传图片',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '格式：建议jpg.png 尺寸：50*50 不超过1M',
			default: ''
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
		image: function($node, model, value, $propertyViewNode) {
			var image = {url:''};
			var data = {type:null};
			if (value !== '') {
				data = $.parseJSON(value);
				image = data.images[0];
			}
			model.set({
				image: image.url
			}, {silent: true});

			if (data.type === 'newImage') {
				W.resource.termite2.Image.put({
					data: image,
					success: function(data) {
					},
					error: function(resp) {
					}
				})
			}
			var currCid = $propertyViewNode.attr('data-dynamic-cid');
			var targetClass,alt;
			switch (currCid){
				case '4':
					targetClass = '.xa-lottery-first';
					alt = '一等奖';
					break;
				case '5':
					targetClass = '.xa-lottery-second';
					alt = '二等奖';
					break;
				case '6':
					targetClass = '.xa-lottery-third';
					alt = '三等奖';
					break;
				default:
					targetClass = '.xa-lottery-first';
					alt = '一等奖';
					break;
			}

			var $target = $('#phoneIFrame').contents().find(targetClass);//找到子frame中的相应元素
			if (value) {
				//更新propertyView中的图片
				//$propertyViewNode.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
				//$propertyViewNode.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
				//更新phoneView中的图片
				//$target.html("<img style='height:50px;width:50px;vertical-align:middle;' src='"+image.url+"' alt='"+alt+"'>");
				$target.html("<img src='"+image.url+"'>");
			}
			this.refresh($node, {refreshPropertyView: true, dynamicComponentId: $propertyViewNode.attr('data-parent-cid')});
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
			//
			var data_cid = $propertyViewNode.attr('data-dynamic-cid');
			var $li_b = $node.find('.wui-i-settingData li[data_cid="' + data_cid + '"]').find('p');

			if (total_prize_count['status'] == "进行中"){
				$propertyViewNode.find('input[data-field="prize_count"]').attr('data-validate','"require-notempty::选项不能为空,,require-natural::只能填入数字,,require-countcontrol::请输入大于"'+total_prize_count[prize_title]['control_prize_count']+'"的数字"');
			}
			if ((/^[0-9]*$/g).exec(value) != null){
				//奖品数量为0时该奖项在奖项设置里不显示
				if (Number(value) == 0) {
					$li_b.parent().hide();
				} else {
					$li_b.parent().show();
				}
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
