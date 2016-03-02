/**
 * @class W.component.appkit.GroupDescription
 *
 */
ensureNS('W.component.appkit');
W.component.appkit.GroupDescription = W.component.Component.extend({
	type: 'appkit.groupdescription',
	selectable: 'yes',
	propertyViewTitle: '团购活动',

    dynamicComponentTypes: [{
		type:'appkit.groupitem',
		model:1
	}],

    properties: [{
		group: '',//团购配置
        groupClass: 'xui-propertyView-app-GroupSetting',
        fields: [{
            name: 'title',
            type: 'text_with_annotation',
            displayName: '团购名称',
            isUserProperty: true,
            maxLength: 30,
            //validate: 'data-validate="require-notempty::活动名称不能为空,,require-word"',
            //validateIgnoreDefaultValue: true,
            annotation: '请简要输入团购名称',
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
            displayName: '起止时间',
            isUserProperty: true,
            //validate: 'data-validate="require-notempty::有效时间不能为空"',
            //validateIgnoreDefaultValue: true,
            default: ''
        },{
            name: 'select_product',
            type: 'text_with_annotation',
            displayName: '选择商品',
            maxLength: 30,
            isUserProperty: true,
            annotation: '',
            //validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
            //validateIgnoreDefaultValue: true,
            default: ''
        }]},{
        group: '',//团购列表
        groupClass: 'xui-propertyView-app-GroupDynamicGroup',
        fields: [{
            name: 'group_frame_title',
            type: 'title_with_nothing',
			//validate:'data-validate="require-notempty::选项不能为空',
            displayName: '拼团人数',
			annotation:'1个团购可创建多种拼团人数供顾客选择',
			isUserProperty:true

        },

        {
            name:'default_group',
            className:'xui-app-Group-i-type',
            type:'apps_group_selector',
            isUserProperty:true,

            typeClassName:'xui-i-groupType',
            typeLabel:'1.',
            typeName:'group_type',
            typeSource:[{
                typeName:'5人团',
                typeValue:'5'
            },{
               typeName:'10人团',
                typeValue:'10'
            }],

            daysClassName:'xui-i-groupDays',
            daysLabel:'拼团时间:',
            days_name:'group_days',
            days_size:'50px',
            days_placeholder:"",
            days_maxLength:5,
            days_annotation:'天',
            // days_validate:'',

            priceClassName:'xui-i-groupPrice',
            priceLabel:'团购价:',
            price_size:'50px',
            price_name:'group_price',
            price_placeholder:"",
            price_maxLength:5,
            price_annotation:'元'
            // price_validate:''


        }


   //      ,{
   //          name: 'group_type',
   //          className:'xui-app-Group-i-type',
   //          type: 'selector_v1',
   //          displayName: '1.',
   //          isUserProperty: true,
   //          source:[{
   //              name:'5人团',
   //              value:'5'
   //          },{
   //              name:'10人团',
   //              value:'10'
   //          }],
			// //validate: 'data-validate="require-notempty::选项不能为空',
   //          default: '5'
   //      },{
   //          name: 'group_days',
   //          className:'xui-app-Group-i-days',
   //          type: 'text_with_annotation',
   //          displayName: '拼团时间',
   //          isUserProperty: true,
   //          maxLength: 5,
   //          size: '70px',
   //          annotation: '天',
   //          //validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
   //          //validateIgnoreDefaultValue: true,
   //          default: ''
   //      },{
   //          name: 'group_price',
   //          className:'xui-app-Group-i-price',
   //          type: 'text_with_annotation',
   //          displayName: '团购价',
   //          isUserProperty: true,
   //          maxLength: 5,
   //          size: '70px',
   //          annotation: '元',
   //          //validate: 'data-validate="require-notempty::选项不能为空,,require-natural::只能填入数字"',
   //          //validateIgnoreDefaultValue: true,
   //          default: ''
   //      }

        ,{
            name: 'group_items',//动态组件
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 0,
            maxItemLength: 1,
            isUserProperty: true,
            default: []
        }

        ]},{
        group: '',//团购信息
        groupClass: 'xui-propertyView-app-GroupInfo',
        fields: [{
            name: 'rule_title',
            type: 'title_with_nothing',
			//validate:'data-validate="require-notempty::选项不能为空',
            displayName: '团购说明',
			annotation:'注：请修改【发货时间】、【开团截止日期】、【商品数量】顾客会查看团购说明，请谨慎填写。',
			isUserProperty:true

        },{
            name: 'rules',
            type: 'textarea',
            displayName: '',
            maxLength: 800,
            isUserProperty: true,
            //validate: 'data-validate="require-notempty::选项不能为空"',
            annotation: '注：请修改【发货时间】、【开团截止日期】、【商品数量】顾客会查看团购说明，请谨慎填写。',
            placeholder: '请简略描述活动具体规则，譬如获取助力值前多少名可以获得特殊资格，以及活动起止时间，客服联系电话等。',
            default: "1.开团和拼团的顾客需要先已团购价支付商品<br>2.到达团购人数上限或到达团购指定时间后，团购结束<br>到达团购人数上限 - 团购成功<br>成功后,在该商品团购结束 20 天内进行发货.<br>在指定时间未到达团购人数上线 - 团购失败<br>失败后, 5~7个工作日完成退款<br>3.本次活动商品数量为 100 份，售完活动结<br>束。开团截止日期 2014-04-12<br>4.已关注的用户可在我的团购中找到参与过<br>的团购，也可以继续创建其他的团购。<br>"
        },{
			name: 'material_image',
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
		},{
            name: 'share_description',
            type: 'text_with_annotation',
            displayName: '分享描述',
            isUserProperty: true,
            maxLength: 26,
            //validate: 'data-validate="require-notempty::活动名称不能为空,,require-word"',
            //validateIgnoreDefaultValue: true,
            annotation: '',
            placeholder:'最多可输入26个字',
            default: ''
        }]

        }],
	propertyChangeHandlers: {
		title: function($node, model, value) {
			//parent.W.Broadcaster.trigger('powerme:change:title', value);
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
		description: function($node, model, value, $propertyViewNode) {
			//model.set({description:value.replace(/\n/g,'<br>')},{silent: true});
			//$node.find('.xa-description .wui-i-description-content').html(value.replace(/\n/g,'<br>'));
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

		rules: function($node, model, value, $propertyViewNode) {
			//model.set({rules:value.replace(/\n/g,'<br>')},{silent: true});
			//$node.find('.xa-rules .wui-i-rules-content').html(value.replace(/\n/g,'<br>'));
		},
		group_items: function($node, model, value) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
		 	var view = $('[data-ui-role="apps-prize-keyword-pane"]').data('view');
			view && view.render(W.weixinKeywordObj);
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
