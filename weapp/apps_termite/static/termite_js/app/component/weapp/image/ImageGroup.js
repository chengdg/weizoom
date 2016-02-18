/**
 * @class W.component.weapp.SwipeImageGroup
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.ImageGroup = W.component.Component.extend({
	type: 'weapp.image_group',
	propertyViewTitle: '图片广告',

    dynamicComponentTypes: [
        {type: 'weapp.image', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
        {
            group: 'Model属性',
            fields: [
            /*{
                name: 'width',
                type: 'text',
                displayName: 'Width',
                default: '100%'
            }, */{
                name: 'displayMode',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [
                    // 可能存在问题暂时隐藏
                    {name:'轮播图', value:'swipe'},
                    {name:'分开显示', value:'sequence'}],
                default: 'sequence'
            }, {
                name: 'displaySize',
                type: 'radio',
                displayName: '显示大小',
                isUserProperty: true,
                source: [{name:'大图', value:'big'}, {name:'小图', value:'small'}],
                default: 'big'
            }, {
                name: 'uploadWidth',
                type: 'hidden',
                displayName: '图片width',
                isUserProperty: true,
                default: "200px"
            }, {
                name: 'uploadHeight',
                type: 'hidden',
                displayName: '图片height',
                isUserProperty: true,
                default: "200px"
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
        displayMode: function($node, model, value) {
            W.Broadcaster.trigger('designpage:refresh');
            if(value=='swipe'){
                $('[name="displaySize"]:first').click();
                $('[name="displaySize"]:last').parent().hide();
            }else{
                $('[name="displaySize"]:last').parent().show();
            }
            W.Broadcaster.trigger('component:resize', this);
        },
        displaySize: function($node, model, value) {
            
            if(value=='big') {
                $node.removeClass('ui-grid-a');
            }
            else {
                $node.addClass('ui-grid-a');
            }
            W.Broadcaster.trigger('designpage:refresh', this);
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
}, {
    indicator: {
        name: '图片广告',
        imgClass: 'componentList_component_image_adv'
    }
});