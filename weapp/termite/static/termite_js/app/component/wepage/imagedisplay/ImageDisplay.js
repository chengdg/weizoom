/**
 * @class W.component.wepage.ImageDisplay
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.ImageDisplay = W.component.Component.extend({
	type: 'wepage.image_display',
	propertyViewTitle: '橱窗',

    dynamicComponentTypes: [
        {type: 'wepage.imagedisplay_image', model: 3, noAdd: 1}
    ],

	properties: [
        {
            group: 'Model属性',
            groupClass: 'xui-propertyView-imgDisplay',
            fields: [
            {
                name: 'title',
                type: 'text',
                displayName: '橱窗标题名',
                isUserProperty: true,
                maxLength: 15,
                default: ""
            }, {
                name: 'displayMode',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [{name:'默认', value:'default'}, {name:'3列', value:'three'}],
                default: 'default'
            }, {
                name: 'contentTitle',
                type: 'text',
                displayName: '内容区标题',
                isUserProperty: true,
                maxLength: 15,
                default: ""
            }, {
                name: 'content',
                type: 'textarea',
                displayName: '内容区说明',
                isUserProperty: true,
                maxLength: 50,
                default: ""
            }]
        },{
            group: '',
            groupClass: 'xui-propertyView-imgDisplayGroup',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
        displayMode: function($node, model, value){
            this.refresh($node, {resize:true});
        },
        title:function($node, model, value){
            $node.find('.wa-display-title').html(value);
            if(value)
                $node.find('.wa-display-title').show();
            else
                $node.find('.wa-display-title').hide();
            W.Broadcaster.trigger('component:resize', this);
        },
        contentTitle:function($node, model, value){
            $node.find('.wa-inner-contentTitle').html(value);
            if(value)
                $node.find('.wa-inner-contentTitle').show();
            else
                $node.find('.wa-inner-contentTitle').hide();
            W.Broadcaster.trigger('component:resize', this);
        },
        content:function($node, model, value){
            $node.find('.wa-inner-content').html(value);
            if(value)
                $node.find('.wa-inner-content').show();
            else
                $node.find('.wa-inner-content').hide();
            W.Broadcaster.trigger('component:resize', this);
            this.refresh($node, {resize:true});
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '橱窗',
        imgClass: 'componentList_component_showcase'
    }
});