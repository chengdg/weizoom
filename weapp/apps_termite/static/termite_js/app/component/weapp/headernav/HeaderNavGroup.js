/**
 * @class W.component.weapp.HeaderNav
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.HeaderNavGroup = W.component.Component.extend({
	type: 'weapp.headernav_group',
	propertyViewTitle: '页头导航',

    dynamicComponentTypes: [
        {type: 'weapp.headernav', model: 6}
    ],
	properties: [
       {
            group: '页头导航栏',
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
        name: '页头导航',
        imgClass: 'componentList_component_header_nav'
    }
});