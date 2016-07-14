/**
 * @class W.component.appkit.SwipeImageGroup
 * 
 */
ensureNS('W.component.appkit');
W.component.appkit.ImageGroup = W.component.Component.extend({
    type: 'appkit.image_group',
    propertyViewTitle: '图片广告',

    shouldIgnoreSubComponent: true,
    dynamicComponentTypes: [{
        type: 'appkit.imagegroup_image',
        model: {
            index: 1,
            image: '',
            target: ''
        }
    }],

    properties: [{
        group: 'Model属性',
        groupClass: '',
        fields: [
            {
                name: 'displayMode',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [
                    {
                        name: '轮播图',
                        value: 'swipe'
                    }, {
                        name: '分开显示',
                        value: 'sequence'
                    }
                ],
                default: 'swipe'
            }, /*{
                name: 'displaySize',
                type: 'radio',
                displayName: '显示大小',
                isUserProperty: true,
                source: [{
                    name: '大图',
                    value: 'big'
                }, {
                    name: '小图',
                    value: 'small'
                }],
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
            }*/
        ]
    }, {
        group: '',
        groupClass: 'xui-propertyView-imgAdjGroup',
        fields: [{
            name: 'items',
            type: 'dynamic-generated-control',
            isUserProperty: true,
            isShowCloseButton: true,
            minItemLength: 0,
            default: []
        }]
    }],

    propertyChangeHandlers: {
        items: function($node, model, value) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
        },
        displayMode: function($node, model, value) {
            this.refresh($node, {resize:true});
        }
    }
}, {
    indicator: {
        name: '图片广告',
        imgClass: 'componentList_component_image_adv'
    }
});
