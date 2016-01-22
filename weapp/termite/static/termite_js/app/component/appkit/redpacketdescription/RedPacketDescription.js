/**
 * @class W.component.appkit.RedPacketDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.RedPacketDescription = W.component.Component.extend({
	type: 'appkit.redpacketdescription',
	selectable: 'yes',
	propertyViewTitle: '拼手气',

    dynamicComponentTypes: [],

	properties: [{
		group: '活动名称',
		groupClass: 'xui-propertyView-app-RedPacketGroup',
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
			name: 'random_total_money',
			type: 'hidden',
			displayName: '拼手气红包总金额',
			isUserProperty: false,
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'random_packets_number',
			type: 'hidden',
			displayName: '拼手气红包红包个数',
			isUserProperty: false,
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'regular_packets_number',
			type: 'hidden',
			displayName: '普通红包红包个数',
			isUserProperty: false,
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'regular_per_money',
			type: 'hidden',
			displayName: '普通红包单个金额',
			validateIgnoreDefaultValue: true,
			isUserProperty: false,
			default: ''
		},{
			name: 'red_packet_type',
			type: 'red_packet_selector',
			displayName: '红包方式',
			isUserProperty: true,
			source: [{
				name: '拼手气红包',
				value: 'random'
			}, {
				name: '普通红包',
				value: 'regular'
			}],
			default: 'random'
		},{
			name: 'start_money',
			type: 'hidden',
			displayName: '最小金额',
			validate: 'data-validate="require-float::请输入正整数或小数"',
			validateIgnoreDefaultValue: true,
			isUserProperty: false,
			default: ''
		},{
			name: 'end_money',
			type: 'hidden',
			displayName: '最大金额',
			validate: 'data-validate="require-float::请输入正整数或小数"',
			validateIgnoreDefaultValue: true,
			isUserProperty: false,
			default: ''
		},{
			name: 'money_range',
			type: 'money_range_selector',
			displayName: '好友贡献金额区间',
			isUserProperty: true,
			validate: 'data-validate="require-notempty::金额区间不能为空"',
			validateIgnoreDefaultValue: true,
			annotation: '好友贡献金额区间，为分享好友后，每个好友贡献的金额区间。该区间会影响到一个红包会被几个好友拼满。需根据总金额与红包个数设置适当的区间。',
			groupHelp:{
				className:'xui-propertyView-app-RedPacketSettingGroupName-helper',
				id:'propertyView-app-RedPacketSettingGroupName-helper',
				link:{
					className:'xui-outerFunctionTrigger xa-outerFunctionTrigger',
					id:'outerFunctionTrigger',
					text:'设置说明',
					handler: 'W.component.appkit.RedPacketDescription.handleHelp'
				}
			},
			default: ''
		},{
			name: 'reply_content',
			type: 'text_with_annotation',
			displayName: '参与活动回复语',
			isUserProperty: true,
			maxLength: 5,
			placeholder: '触发获取图文信息，如：拼红包',
			validate: 'data-validate="require-notempty::回复语不能为空"',
			validateIgnoreDefaultValue: true,
			annotation: '请在 微信-自动回复 创建该关键词',
			default: ""
		},{
			name: 'qrcode',
			type: 'qrcode_dialog_select',
			displayName: '用户识别二维码',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择带参数二维码', hasdata:'修改'},
			selectedButton: '选择带参数二维码',
			dialog: 'W.dialog.termite.SelectQrcodeDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '此处若空缺，则使用公众号二维码代替',
			default: {ticket:'',name:''}
		},{
			name: 'wishing',
			type: 'text_with_annotation',
			displayName: '开现金红包文字',
			isUserProperty: true,
			maxLength: 15,
			placeholder: '点赞帮好友赢现金红包',
			annotation: '拼红包成功后，开启现金红包时显示文字',
			default: "点赞帮好友赢现金红包"
		},
		//	{
		//	name: 'color',
		//	type: 'radio',
		//	displayName: '背景皮肤',
		//	isUserProperty: true,
		//	source: [{
		//		name: '默认背景',
		//		value: 'yellow'
		//	}, {
		//		name: '新年快乐',
		//		value: 'red'
		//	}],
		//	default: 'yellow'
		//},
			{
			name: 'rules',
			type: 'textarea',
			displayName: '活动规则',
			maxLength: 500,
			isUserProperty: true,
			placeholder: '请简略描述活动具体规则，譬如获取助力值前多少名可以获得特殊资格，以及活动起止时间，客服联系电话等。',
			default: ""
		},{
			name: 'material_image',
			type: 'image_dialog_select',
			displayName: '分享图标',
			isUserProperty: true,
			isShowCloseButton: false,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '提示：建议图片长宽100px*100px,仅支持jpg,png',
			validate: 'data-validate="require-notempty::请添加一张图片"',
			default: ""
		},{
			name: 'share_description',
			type: 'textarea',
			displayName: '分享描述',
			maxLength: 26,
			isUserProperty: true,
			placeholder: '最多可输入26个字',
			validate: 'data-validate="require-notempty::分享描述不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ""
		}]}],
	propertyChangeHandlers: {
		title: function($node, model, value) {
			parent.W.Broadcaster.trigger('red_packet:change:title', value);
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
		red_packet_type: function($node, model, value, $propertyViewNode) {

		},
		qrcode:function($node, model, value, $propertyViewNode){
			var data;
			if (value !== '') {
				data = $.parseJSON(value);
				qrcode = data[0];
			}
			var ticket ='https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='+qrcode.ticket;
			model.set({
				qrcode:{
					ticket: ticket,
					name: qrcode.name
				}
			}, {silent: true});

			if (value) {
				//更新propertyView中的图片
				var $target = $propertyViewNode.find($('[data-field-anchor="qrcode"]'));
				$target.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',ticket);
				$target.find('.propertyGroup_property_dialogSelectField').find('.qrcodeName').removeClass('xui-hide').html(qrcode.name);
				$target.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
				$target.find('.propertyGroup_property_dialogSelectField').find('.qrcode_help').css({
					'height': '100px',
					'line-height': '100px'
				});
			}
		},
		material_image: function($node, model, value, $propertyViewNode) {
			var image = {url:''};
			var data = {type:null};
			if (value !== '') {
				data = $.parseJSON(value);
				image = data.images[0];
			}
			model.set({
				material_image: image.url
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
		//color: function($node, model, value, $propertyViewNode) {
		//	switch (value){
		//		case 'yellow':
		//			$node.find(".wui-red_packet-container").addClass('yellow');
		//			$node.find(".wui-red_packet-container").removeClass('red orange new_year_red');
		//			break;
		//		case 'red':
		//			$node.find(".wui-red_packet-container").addClass('red');
		//			$node.find(".wui-red_packet-container").removeClass('yellow orange new_year_red');
		//			break;
		//		default :
		//			$node.find(".wui-red_packet-container").addClass('yellow');
		//			$node.find(".wui-red_packet-container").removeClass('red orange new_year_red');
		//			break;
		//	}
		//},
		rules: function($node, model, value, $propertyViewNode) {
			model.set({rules:value.replace(/\n/g,'<br>')},{silent: true});
			$node.find('.xa-rules .wui-i-rules-content').html(value.replace(/\n/g,'<br>'));
		},
		share_description: function($node, model, value){
			model.set({share_description:value.replace(/\n/g,'')},{silent: true});
		}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
var getDateTime = function($node,start_time_text,end_time_text,model){
	var s_date =start_time_text.replace(" ","-").replace(/-/g,"/").split(/\/|\:|\ /);
	var e_date =end_time_text.replace(" ","-").replace(/-/g,"/").split(/\/|\:|\ /);

	var start_date = new Date(s_date[0], s_date[1] - 1, s_date[2], s_date[3], s_date[4]).getTime();
	var end_date = new Date(e_date[0], e_date[1] - 1, e_date[2], e_date[3], e_date[4]).getTime();

	var dif_time = end_date - start_date;
	var day = Math.floor(dif_time / (1000 * 60 * 60 * 24)); //天数
	var h_time = dif_time % (1000 * 60 * 60 * 24);
	var hour = Math.floor(h_time / (1000 * 60 * 60));//小时
	var m_time = h_time % (1000 * 60 * 60);
	var minute = Math.floor(m_time / (1000 * 60));//分钟
	var second = Math.floor((m_time % (1000 * 60))/1000); //秒

	var text_day = day.toString().length != 1 ?day : '0'+day;
	var text_hour = hour.toString().length != 1 ?hour : '0'+hour;
	var text_minute = minute.toString().length != 1 ?minute : '0'+minute;
	var text_second = second.toString().length != 1 ?second : '0'+second;

	$node.find('.wui-i-timing .xa-day').text(text_day);
	$node.find('.wui-i-timing .xa-hour').text(text_hour);
	$node.find('.wui-i-timing .xa-minute').text(text_minute);
	$node.find('.wui-i-timing .xa-second').text(text_second);
	model.attributes.timing_value=({
		day: text_day,
		hour: text_hour,
		minute: text_minute,
		second: text_second
	});
};

W.component.appkit.RedPacketDescription.handleHelp = function(){
	//初始化好友贡献区间设置说明
	ensureNS('W.dialog.red_packet');
	W.dialog.red_packet.InstructionDialog = W.dialog.Dialog.extend({
		getTemplate: function() {
			$('#red_packet-money-dialog-tmpl-src').template('red_packet-money-dialog-tmpl');
			return "red_packet-money-dialog-tmpl";
		}
	});
};