/**
 * @class W.component.wepage.TextNavGroup
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.TextNavGroup = W.component.Component.extend({
	type: 'wepage.textnav_group',
	propertyViewTitle: '文本导航',

    dynamicComponentTypes: [
        {type: 'wepage.textnav', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
       {
            group: '文本列表',
            groupClass: 'xui-propertyView-textNavGroup',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                isShowCloseButton: true,
                minItemLength: 1,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
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
        name: '文本导航',
        imgClass: 'componentList_component_text_nav'
    }
});