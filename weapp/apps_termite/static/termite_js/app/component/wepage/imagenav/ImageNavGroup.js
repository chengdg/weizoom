/**
 * @class W.component.wepage.ImageNav
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ImageNavGroup = W.component.Component.extend({
	type: 'wepage.imagenav_group',
	propertyViewTitle: '图片导航',

    dynamicComponentTypes: [
        {type: 'wepage.image_nav', model: 4, noAdd: 1}
    ],

	properties: [
        {
            group: '已选图片',
            groupClass: 'xui-propertyView-imageNavGroup',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                isShowCloseButton: false,
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
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '图片导航',
        imgClass: 'componentList_component_image_nav'
    }
});