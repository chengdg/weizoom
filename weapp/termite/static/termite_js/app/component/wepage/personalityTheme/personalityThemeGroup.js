/**
 * @class W.component.wepage.personalityThemeGroup
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.personalityThemeGroup = W.component.Component.extend({
	type: 'wepage.personalityTheme_group',
	propertyViewTitle: '页面导航',
    selectable: "yes",
    hideSelectIndicator: true,

    dynamicComponentTypes: [
        {type: 'wepage.personalityTheme', model: 2}
    ],

	properties: [
        {
            group: 'Model属性',
            groupClass: 'xui-propertyView-personalityTheme',
            fields: [
            {
                name: 'backgroud',
                type: 'dialog_select',
                displayName: '背景图片',
                isUserProperty: true,
                triggerButton: {nodata:'选择图片', hasdata:'修改'},
                dialog: 'W.dialog.termite.SelectImagesDialog',
                help: '建议尺寸：640*1008像素',
                default: ''
            }]
        },{
            group: '',
            groupClass: 'xui-propertyView-personalityThemeGroup',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                isShowCloseButton: true,
                minItemLength: 2,
                maxItemLength: 4,
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
        name: 'personalityTheme',
        imgClass: 'componentList_component_personality_theme'
    },
    isManagerComponent: true
});