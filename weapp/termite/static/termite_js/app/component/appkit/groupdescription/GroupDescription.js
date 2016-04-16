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
		model: 1
	}],

    properties: [{
		group: '',//团购配置
        groupClass: 'xui-propertyView-app-GroupSetting',
        fields: [
        {
            name: 'title',
            type: 'text_with_annotation',
            displayName: '团购名称：',
            isUserProperty: true,
            maxLength: 30,
            validate: 'data-validate="require-notempty::活动名称不能为空,,require-word"',
            validateIgnoreDefaultValue: true,
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
            displayName: '起止时间：',
            isUserProperty: true,
            validate:'data-validate=""',
            default: ''
        },{
			name: 'product',
			type: 'product_dialog_select',
			displayName: '选择商品：',
			isUserProperty: true,
			isShowCloseButton: true,
			selectedButton: '选择商品',
			dialog: 'W.dialog.termite.SelectProductDialog',
			dialogParameter: '{"multiSelection": false}',
            validate:'data-validate=""',
			default: {productId:'',productImg:'',productName:'',productPrice:'',productSocks:'',productSales:'',productCreate_at:'',productUsercode:''}
		}]},{

        group: '',//团购标题
        groupClass: 'xui-propertyView-app-GroupTitle',
        fields: [{
            name: 'group_title',
            type: 'title_with_nothing',
			validate:'data-validate=""',
            displayName: '拼团人数：',
			annotation:'注：1个团购可创建多种拼团人数供顾客选择',
			isUserProperty:true

        }]},
		{
		group:'',//列表
		groupClass: 'xui-propertyView-app-DynamicGroupList xa-propertyView-app-DynamicGroupList',
        fields: [
			{
            name: 'group_items',//动态组件
            displayName: '',
            type: 'dynamic-generated-control',
            isShowCloseButton: true,
            minItemLength: 1,
            maxItemLength: 2,
            isUserProperty: true,
            default: []
        }]},{
        group: '',//团购信息
        groupClass: 'xui-propertyView-app-GroupInfo',
        fields: [{
            name: 'rule_title',
            type: 'title_with_nothing',
			validate:'data-validate=""',
            displayName: '团购说明：',
			annotation:'注：请修改【发货时间】、【开团截止日期】、【商品数量】顾客会查看团购说明，请谨慎填写。',
			isUserProperty:true

        },{
            name: 'rules',
            type: 'textarea',
            displayName: '',
            maxLength: 800,
            isUserProperty: true,
            validate: 'data-validate="require-notempty::选项不能为空"',
            annotation: '注：请修改【发货时间】、【开团截止日期】、【商品数量】顾客会查看团购说明，请谨慎填写。',
            placeholder: '请简略描述活动具体规则，以及活动起止时间，客服联系电话等。',
            default: "1.开团和拼团的顾客需要先已团购价支付商品\n2.到达团购人数上限或到达团购指定时间后，团购结束。到达团购人数上限 - 团购成功。成功后,在该商品团购结束【20】天内进行发货。在指定时间未到达团购人数上线 - 团购失败。失败后, 【5~7】个工作日完成退款\n3.本次活动商品数量为【100】份，售完活动结束。开团截止日期【201x-0x-xx】\n4.已关注的用户可在 个人中心 - 全部订单 中找到支付的团购订单和进入团购活动的入口。"
        },{
			name: 'material_image',
			type: 'image_dialog_select_v2',
			displayName: '分享图片：',
			isUserProperty: true,
			isShowCloseButton: true,
			triggerButton: {nodata:'选择图片', hasdata:'修改'},
			selectedButton: '选择图片',
			dialog: 'W.dialog.termite.SelectImagesDialog',
			dialogParameter: '{"multiSelection": false}',
			help: '格式：建议jpg.png 尺寸：50*50 不超过1M',
			default: '',
            validate: 'data-validate="require-notempty::请插入分享图片"',
            // validateIgnoreDefaultValue: true

		},{
            name: 'share_description',
            type: 'text_with_annotation',
            displayName: '分享描述：',
            isUserProperty: true,
            maxLength: 26,
            validate: 'data-validate="require-notempty::活动名称不能为空"',
            annotation: '',
            placeholder:'最多可输入26个字',
            default: ''
        }]

        }],
	propertyChangeHandlers: {
		// title: function($node, model, value,$propertyViewNode) {
  //       },
        start_time: function($node, model, value, $propertyViewNode) {
            var end_time_text = $node.find('.wui-i-end_time').text();
            $node.find('.wui-i-start_time').text(value);
            if (end_time_text != ""){
                getDateTime($node,value,end_time_text,model);
            }
        },
        end_time: function($node, model, value, $propertyViewNode) {
            var start_time_text = $node.find('.wui-i-start_time').text();
            $node.find('.wui-i-end_time').text(value.split(' ')[0]);
            if (start_time_text != ""){
                getDateTime($node,start_time_text,value,model);
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
                // var $target = $propertyViewNode.find($('[data-field-anchor="material_image"]'));
                // $target.find('.propertyGroup_property_dialogSelectField .xa-dynamicComponentControlImgBox').removeClass('xui-hide').find('img').attr('src',image.url);
                // $target.find('.propertyGroup_property_dialogSelectField .propertyGroup_property_input').find('.xui-i-triggerButton').text('修改');
             }
            this.refresh($node, {refreshPropertyView: true});
        },
        group_items: function($node, model, value,$propertyViewNode) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
            $ul = $node.find('.wui-i-description ul');

            var n4li = $ul.children('li').length;
            var n4li_hide = $ul.children('.xui-hide').length;
            var n4li_show = n4li-n4li_hide;

            if(n4li_show==0){
                $ul.find('.wui-i-group1').removeClass('xui-hide');
            }else if(n4li_show==1){
                $ul.find('.wui-i-group2').removeClass('xui-hide');
			}else if(n4li_show==2){
				$ul.find('.wui-i-group2').addClass('xui-hide');
			}
        },
        share_description:function($node, model, value, $propertyViewNode){
            model.set({share_description:value.replace(/\n/g,'<br>')},{silent: true});
        },
        rules:function($node, model, value, $propertyViewNode){
            model.set({rules:value.replace(/\n/g,'<br>').replace(/"\n"/,'<br>')},{silent: true});

        },
		product:function($node, model, value, $propertyViewNode){
			var data;
			if (value !== '') {
				data = $.parseJSON(value);
				product = data[0];
			}

			model.set({
				product:{
					productId:product.id,
					productImg: product.thumbnails_url,
					productName:product.name,
					productPrice:product.display_price,
                    productSocks:product.stocks,
					productSales:product.sales,
                    productUsercode:product.user_code
				}
			}, {silent: true});



			if (value[0]) {
				//更新propertyView中的图片
				console.log(value[0]);

				var $target = $propertyViewNode.find($('table.xa-productList')).removeClass('xui-hide');
				$target.find('.productImg').attr('src',product.thumbnails_url);
				$target.find('.productName').html(product.name);
				$target.find('.productUserCode').html('商品编码:'+product.user_code);
				$target.find('.productPrice').html(product.display_price);
				$target.find('.productSocks').html(product.sales);

				$node.find('.wui-i-product-img > img').attr('src',product.thumbnails_url);
			}
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



