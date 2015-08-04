/**
 * @class W.component.jqm.SwipeImageGroup
 * 
 */
W.component.jqm.SwipeImageGroup = W.component.Component.extend({
	type: 'jqm.swipeimage_group',
	propertyViewTitle: '轮播图',

    dynamicComponentTypes: [
        {type: 'jqm.swipeimage', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'width',
                type: 'text',
                displayName: 'Width',
                default: '100%'
            }, {
                name: 'uploadWidth',
                type: 'text',
                displayName: '图片宽度',
                isUserProperty: true,
                default: "200px"
            }, {
                name: 'uploadHeight',
                type: 'text',
                displayName: '图片高度',
                isUserProperty: true,
                default: "200px"
            }]
        }, {
            group: '',
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
        },
        width: function($node, model, value) {
            W.Broadcaster.trigger('mobilepage:refresh');
        },
        image_width: function($node, model, value) {
            W.Broadcaster.trigger('mobilepage:refresh');
        },
        image_height: function($node, model, value) {
            W.Broadcaster.trigger('mobilepage:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '轮播图',
        imgClass: 'componentList_component_swipe_image'
    }
});