/**
 * @class W.component.wepage.specialTemplateGroup
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.specialTemplateGroup = W.component.Component.extend({
	type: 'wepage.specialTemplate_group',
	propertyViewTitle: '个性模板2',
    hideSelectIndicator: true,

    dynamicComponentTypes: [
        {type: 'wepage.specialTemplate', model: 3}
    ],

	properties: [
        {
            group: 'Model属性',
            groupClass: 'xui-propertyView-specialTemplate',
            fields: [
            {
                name: 'backgroud',
                type: 'dialog_select',
                displayName: '背景图片',
                isUserProperty: true,
                triggerButton: {nodata:'选择图片', hasdata:'修改'},
                dialog: 'W.dialog.termite.SelectImagesDialog',
                help: '建议尺寸：640*1080像素\n尺寸不匹配，图片将会被拉伸或压缩',
                default: ''
            }]
        },{
            group: '',
            groupClass: 'xui-propertyView-specialTemplateGroup',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                isShowCloseButton: true,
                minItemLength: 3,
                maxItemLength: 7,
                default: []
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
   
    	items: function($node, model, value) {
            /*
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });
            */

            // var task = new W.DelayedTask(function() {
            //     W.Broadcaster.trigger('component:finish_create', null, this);
            // }, this);
            // task.delay(100);
            this.refresh($node, {resize:true, refreshPropertyView:true});
            /*
            _.delay(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, 100);
            */
        }
    }
}, {
    indicator: {
        name: 'specialTemplate',
        imgClass: 'componentList_component_special_template'
    },
    isManagerComponent: true
});