/**
 * @class W.component.jqm.SwipeImage
 * 
 */
W.component.jqm.SwipeImage = W.component.Component.extend({
	type: 'jqm.swipeimage',
    selectable: 'no',
	propertyViewTitle: '图片',

	properties: [
        {
            group: 'Model属性',
            fields: [{
                name: 'text',
                type: 'hidden',
                displayName: '',
                default: '图片',
            }, {
                name: 'image',
                type: 'dialog_select',
                isUserProperty: true,
                displayName: '图片',
                triggerButton: '选择图片...',
                dialog: 'W.workbench.SelectImageDialog',
                default: ''
            }, {
                name: 'target',
                type: 'select',
                displayName: '链接',
                source: W.data.getWorkbenchPages,
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
        image: function($node, model, value, $propertyViewNode) {
            var parentComponent = W.component.getComponent(this.pid);
            $propertyViewNode.find('.dynamicComponentControlImgBox img').attr('src', value);
            W.Broadcaster.trigger('design:refresh');
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
});