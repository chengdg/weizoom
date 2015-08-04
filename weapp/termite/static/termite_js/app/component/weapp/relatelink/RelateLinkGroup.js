/**
 * @class W.component.weapp.RelateLinkGroup
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.RelateLinkGroup = W.component.Component.extend({
	type: 'weapp.relatelink_group',
	propertyViewTitle: '关联链接',

    dynamicComponentTypes: [
        {type: 'weapp.relatelink', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
       {
            group: '关联链接',
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
        name: '关联链接',
        imgClass: 'componentList_component_relate_link'
    }
});