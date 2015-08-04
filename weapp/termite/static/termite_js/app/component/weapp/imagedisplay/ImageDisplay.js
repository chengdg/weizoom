/**
 * @class W.component.weapp.ImageDisplay
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.ImageDisplay = W.component.Component.extend({
	type: 'weapp.image_display',
	propertyViewTitle: '橱窗',

    dynamicComponentTypes: [
        {type: 'weapp.image', model: 3, noAdd: 1}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [
            {
                name: 'title',
                type: 'text',
                displayName: '橱窗标题名',
                isUserProperty: true,
                default: ""
            }, {
                name: 'displayMode',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [{name:'默认', value:'default'}, {name:'3列', value:'three'},{name:'2列', value:'two'},{name:'1列', value:'one'}],
                default: 'default'
            }, {
                name: 'contentTitle',
                type: 'text',
                displayName: '内容区标题',
                isUserProperty: true,
                default: ""
            }, {
                name: 'content',
                type: 'textarea',
                displayName: '内容区说明',
                isUserProperty: true,
                default: ""
            }]
        }, {
            group: '已选图片',
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
        displayMode: function($node, model, value){
            console.log(value, 'value')
            if(value=='one'){
                 $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-e');
                 $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-a');
                 $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-b');
                 $node.find('.wa-inner-imgbox').parent().parent().parent().addClass('wui-grid-f');
            }else if(value=='two'){
                $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-e');
                $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-f');
                $node.find('.wa-inner-imgbox').parent().parent().parent().removeClass('wui-grid-b');
                $node.find('.wa-inner-imgbox').parent().parent().parent().addClass('wui-grid-a');
            }else if(value=='three'){
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-e');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-a');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-f');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().addClass('wui-grid-b');
            }else{
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-b');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-a');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().removeClass('wui-grid-f');
                $node.find('.wa-inner-imgbox:first').parent().parent().parent().addClass('wui-grid-e');
            }
            W.Broadcaster.trigger('component:resize', this);
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