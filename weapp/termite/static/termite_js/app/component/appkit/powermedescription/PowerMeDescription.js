/**
 * @class W.component.appkit.PowerMeDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.PowerMeDescription = W.component.Component.extend({
	type: 'appkit.powermedescription',
	selectable: 'yes',
	propertyViewTitle: '微助力',

    dynamicComponentTypes: [],

	properties: [{
		group: '活动名称',
		groupClass: 'xui-propertyView-app-PowerMeGroup',
		fields: [{
			name: 'title',
			type: 'text_with_annotation',
			displayName: '活动名称',
			isUserProperty: true,
			maxLength: 30,
			validate: 'data-validate="require-notempty::活动名称不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			annotation: '将作为活动的标题使用',
			default: ''
		},{
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
		},{
			name: 'valid_time',
			type: 'date_range_selector',
			displayName: '活动时间',
			isUserProperty: true,
			validate: 'data-validate="require-notempty::有效时间不能为空"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'timing',
			type: 'checkbox-group',
			displayName: '',
			isUserProperty: true,
			source: [{
				name: '显示倒计时',
				value: 'timing',
				columnName: 'timing'
			}],
			default: {timing:{select:true}}
		}, {
			name: 'timing_value',
			type: 'hidden',
			displayName: '倒计时',
			isUserProperty: true,
			default: {
				day:'00',
				hour:'00',
				minute:'00',
				second:'00'
			}
		},{
			name: 'description',
			type: 'text_with_annotation',
			displayName: '活动描述',
			maxLength: 30,
			isUserProperty: true,
			annotation: '将显示在页面按钮的下方位置',
			default: ''
		},{
			name: 'reply_content',
			type: 'text',
			displayName: '参与活动回复语',
			isUserProperty: true,
			placeholder: '触发获取图文信息，如：抢礼物',
			default: ""
		},{
			name: 'material_image',
			type: 'image_dialog_select',
			displayName: '链接图文小图',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示：建议图片长宽20px*20px，正方形图片',
			validate: 'data-validate="require-notempty::请添加一张图片"',
			default: ""
		},{
			name: 'background_image',
			type: 'image_dialog_select',
			displayName: '顶部背景图',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示:图片格式jpg/png, 图片宽度640px, 高度自定义, 请上传风格与背景配色协调的图片',
			validate: 'data-validate="require-notempty::请添加一张图片"',
			default: ""
		},{
			name: 'color',
			type: 'radio',
			displayName: '背景配色',
			isUserProperty: true,
			source: [{
				name: '冬日暖阳',
				value: 'yellow'
			}, {
				name: '玫瑰茜红',
				value: 'red'
			}, {
				name: '热带橙色',
				value: 'orange'
			}],
			default: 'yellow'
		},{
			name: 'rules',
			type: 'textarea',
			displayName: '活动规则',
			maxLength: 200,
			isUserProperty: true,
			placeholder: '请简略描述活动具体规则，譬如获取助力值前多少名可以获得特殊资格，以及活动起止时间，客服联系电话等。',
			default: ""
		}]}],
	propertyChangeHandlers: {
		title: function($node, model, value) {
			parent.W.Broadcaster.trigger('powerme:change:title', value);
		},
		start_time: function($node, model, value, $propertyViewNode) {
			var end_time_text = $node.find('.wui-i-end_time').text();
			$node.find('.wui-i-start_time').text(value);
			if (end_time_text != ""){
				getDateTime($node,value,end_time_text,model);
			}
		},
		end_time: function($node, model, value, $propertyViewNode) {
			var start_time_text = $node.find('.wui-i-start_time').text();
			$node.find('.wui-i-end_time').text(value);
			if (start_time_text != ""){
				getDateTime($node,start_time_text,value,model);
			}

		},
		timing: function($node, model, value, $propertyViewNode) {
			$node.find('.wa-timing').toggle();
		},
		timing_value:function($node, model, value, $propertyViewNode){
		},
		description: function($node, model, value, $propertyViewNode) {
			model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-description .wui-i-description-content').html(value.replace(/\n/g,'<br>'));
		},
		material_image: function($node, model, value, $propertyViewNode) {
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
			if (value) {
				//更新propertyView中的图片
				var $target = $propertyViewNode.find($('[data-field-anchor="material_image"]'));
				$target.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
				$target.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
			}
		},
		background_image: function($node, model, value, $propertyViewNode) {
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
			if (value) {
				//更新propertyView中的图片
				var $phone_target = $('#phoneIFrame').contents().find('.wui-i-background-image');
				var $target = $propertyViewNode.find($('[data-field-anchor="background_image"]'));
				$target.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
				$target.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
				$phone_target.html("<img src='"+image.url+"'>");
			}
		},
		color: function($node, model, value, $propertyViewNode) {
			switch (value){
				case 'yellow':
					value = '0';
					break;
				case 'red':
					value = '1';
					break;
				case 'orange':
					value = '2';
					break;
				default :
					value = '0';
					break;
			}
			if(value == '0'){
				$node.find("#css_yellow")[0].disabled = false;
				$node.find("#css_red")[0].disabled = true;
				$node.find("#css_orange")[0].disabled = true;
			}else{
				if(value == '1'){
					$node.find("#css_yellow")[0].disabled = true;
					$node.find("#css_red")[0].disabled = false;
					$node.find("#css_orange")[0].disabled = true;
				}else{
					$node.find("#css_yellow")[0].disabled = true;
					$node.find("#css_red")[0].disabled = true;
					$node.find("#css_orange")[0].disabled = false;
				}
			}
		},
		rules: function($node, model, value, $propertyViewNode) {
			model.set({rules:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-rules .wui-i-rules-content').html(value.replace(/\n/g,'<br>'));
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
var getDateTime = function($node,start_time_text,end_time_text,model){
	var start_date = new Date(start_time_text.toString()).getTime();
	var end_date = new Date(end_time_text.toString()).getTime();

	var dif_time = end_date - start_date;

	var day = Math.floor(dif_time / (1000 * 60 * 60 * 24)); //天数
	var h_time = dif_time % (1000 * 60 * 60 * 24);
	var hour = Math.floor(h_time / (1000 * 60 * 60));//小时
	var m_time = h_time % (1000 * 60 * 60);
	var minute = Math.floor(m_time / (1000 * 60));//分钟
	var second = Math.floor((m_time % (1000 * 60))/1000); //秒
	console.log(minute.length);
	$node.find('.wui-i-timing .xa-day').text(day.toString().length != 1 ? day : '0'+day);
	$node.find('.wui-i-timing .xa-hour').text(hour.toString().length == 2 ? hour : '0'+hour);
	$node.find('.wui-i-timing .xa-minute').text(minute.toString().length == 2 ? minute : '0'+minute);
	$node.find('.wui-i-timing .xa-second').text(second.toString().length == 2 ? second : '0'+second);
	model.attributes.timing_value=({
		day: $node.find('.wui-i-timing .xa-day').text(),
		hour: $node.find('.wui-i-timing .xa-hour').text(),
		minute: $node.find('.wui-i-timing .xa-minute').text(),
		second: $node.find('.wui-i-timing .xa-second').text()
	});
};
