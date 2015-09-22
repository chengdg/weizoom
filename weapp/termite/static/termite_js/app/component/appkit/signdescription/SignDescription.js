/**
 * @class W.component.appkit.SignDescription
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.SignDescription = W.component.Component.extend({
	type: 'appkit.signdescription',
	selectable: 'yes',
	propertyViewTitle: '微信抽奖',

    //dynamicComponentTypes: [{
    //    type: 'appkit.signitem',
    //    model: 3
    //}],

	properties: [{
		group: '文本调研项',
		groupClass: 'xui-propertyView-app-Selection',
		fields: [
			{
			name: 'title',
			type: 'text',
			displayName: '活动名称',
			isUserProperty: true,
			maxLength: 10,
			validate: 'data-validate="require-notempty::活动不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'description',
			type: 'textarea',
			displayName: '签到说明',
			maxLength: 200,
			isUserProperty: true,
			default: ''
		},{
			name: 'share',
			type: 'text',
			displayName: '分享图片',
			isUserProperty: true,
			maxLength: 10,
			//validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'share_description',
			type: 'textarea',
			displayName: '分享描述',
			maxLength: 200,
			isUserProperty: true,
			default: '签到赚积分啦！'
		},{
			name: 'keyword',
			type: 'text',
			displayName: '关键字',
			isUserProperty: true,
			maxLength: 10,
			//validate: 'data-validate="require-notempty::页面标题不能为空,,require-word"',
			validateIgnoreDefaultValue: true,
			default: ''
		},{
			name: 'reply',
			type: 'textarea',
			displayName: '回复内容',
			maxLength: 200,
			isUserProperty: true,
			default: '建议填写垫付近期活动通知，签到奖励等内容……'
		},{name: 'items',//动态组件

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
		//title: function($node, model, value, $propertyViewNode) {
		//	$node.find('.xa-title').text(value);
		//},
		//start_time: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-start_time').text(value);
		//},
		//end_time: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-end_time').text(value);
		//},
		//description: function($node, model, value, $propertyViewNode) {
		//	model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
		//	$node.find('.xa-description .wui-i-description-content').html(value.replace(/\n/g,'<br>'));
		//},
		//expend: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-lotterydescription .xa-remainedIntegral strong').text(value);
		//},
		//delivery: function($node, model, value, $propertyViewNode) {
		//	$node.find('.wui-i-prize>.xa-delivery').html(value);
		//},
		//limitation: function($node, model, value, $propertyViewNode) {
		//	switch (value){
		//		case 'once_per_user':
		//			value = '1';
		//			break;
		//		case 'once_per_day':
		//			value = '1';
		//			break;
		//		case 'twice_per_day':
		//			value = '2';
		//			break;
		//		case 'no_limit':
		//			value = '-1';
		//			break;
		//		default :
		//			value = '0';
		//			break;
		//	}
		//	var $header = $node.find('.wui-lotterydescription').find('.xa-header');
		//	if(value == '-1'){
		//		$header.addClass('wui-lotterydescription-hide');
		//	}else{
		//		$header.removeClass('wui-lotterydescription-hide').find('p b').html(value);
		//	}
        //
		//}
	},

	initialize: function(obj) {
		this.super('initialize', obj);
	}
});
