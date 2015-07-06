/**
 * @class W.component.wepage.PageHeader
 * 
 */
W.component.wepage.PageHeader = W.component.Component.extend({
	type: 'wepage.shopheader',
	propertyViewTitle: '',

	properties: [
        {
            group: '属性1',
            groupClass:'xui-propertyView-shopHeader',
            fields: [{
                name: 'backgroud',
                type: 'dialog_select',
                displayName: '背景图片',
                isUserProperty: true,
                triggerButton: {nodata:'选择图片', hasdata:'修改'},
                dialog: 'W.dialog.termite.SelectImagesDialog',
                help: '建议尺寸：640*200像素\n尺寸不匹配，图片将会被拉伸或压缩',
                isShowCloseButton: true,
                default: ''
            },{
                name: 'title',
                type: 'text',
                displayName: '店铺名称',
                maxLength: 15,
                // validate:true,js报错
                isUserProperty: true,
                placeholder:'店铺名称',
                default: '店铺名称'
            }]
        }
    ],

    propertyChangeHandlers: {
       backgroud: function($node, model, value, $propertyViewNode) {
            var image = {url:''};
            var data = {type:null};
            if (value !== '') {
                data = $.parseJSON(value);
                image = data.images[0];
            }
            model.set({
                backgroud: image.url
            }, {silent: true});

            this.refresh($node, {refreshPropertyViewForField:'backgroud'});

            if (data.type === 'newImage') {
                W.resource.termite2.Image.put({
                    data: image,
                    success: function(data) {

                    },
                    error: function(resp) {

                    }
                })
            }
        },
        title: function($node, model, value) {
            this.refresh($node, {resize: true});
        },
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: 'ShopHeader',
        imgClass: 'componentList_component_shop_header'
    },
    isManagerComponent: true
 });