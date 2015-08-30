/**
 * @class W.component.appkit.LottertItem
 * 奖项
 */
ensureNS('W.component.appkit');
W.component.appkit.LottertItem = W.component.Component.extend({
	type: 'appkit.lotteryitem',
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
			annotation: '注：奖品数量为0时，不设此奖项',
			validate: 'data-validate="require-notempty::选项不能为空,,require-nonnegative::只能填入数字"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'prize',
			type: 'prize_selector_v3',
			displayName: '活动奖励',
			isUserProperty: true,
			default: {type:"no_prize", data:null}
		},{
			name: 'image',
			type: 'image_dialog_select',
			displayName: '上传图片',
			isUserProperty: true,
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
				$propertyViewNode.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
				$propertyViewNode.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
				//更新phoneView中的图片
				$target.html("<img style='height:50px;width:50px;vertical-align:middle;' src='"+image.url+"' alt='"+alt+"'>");
			}
		},
		prize: function($node, model, value, $propertyViewNode) {
			if(value && value.data){
				var data_cid = $propertyViewNode.attr('data-dynamic-cid');
				var $li_b = $node.find('.wui-i-settingData li[data_cid="'+data_cid+'"]').find('b');
				if(value.type == 'coupon'){
					$li_b.html(value.data.name);
				}else{
					$li_b.html(value.data);
				}
			}
		}
	}
});
