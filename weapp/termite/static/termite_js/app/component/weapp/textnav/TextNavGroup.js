/**
 * @class W.component.weapp.TextNavGroup
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.TextNavGroup = W.component.Component.extend({
	type: 'weapp.textnav_group',
	propertyViewTitle: '文本导航',

    dynamicComponentTypes: [
        {type: 'weapp.textnav', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
       {
            group: '文本列表',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
    	items: function($node, model, value) {
            var index = 1;
            var orderedCids = value;
            _.each(orderedCids, function(cid) {
                W.component.CID2COMPONENT[cid].model.set('index', index++, {silent: true});
            });

            var task = new W.DelayedTask(function() {
                W.Broadcaster.trigger('component:finish_create', null, this);
            }, this);
            task.delay(100);
        }
    }
}, {
    indicator: {
        name: '文本导航',
        imgClass: 'componentList_component_text_nav'
    }
});