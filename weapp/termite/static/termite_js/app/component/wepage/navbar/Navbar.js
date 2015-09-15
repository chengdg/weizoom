/**
 * @class W.component.wepage.Navbar
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.Navar = W.component.Component.extend({
	type: 'wepage.navbar',
	propertyViewTitle: '底部导航',
    selectable: 'no',

    dynamicComponentTypes: [
        {type: 'wepage.navbar_firstnav', model: {index: 1, image: '', target: ''}}
    ],

	properties: [
        {
            group: '',
            groupClass:'xui-propertyView-navbar-settings',
            fields: [{
                name: 'pages',
                type: 'checkbox-group',
                displayName: '将导航应用在以下页面：',
                isUserProperty: true,
                source: [{
                    name: '店铺主页',
                    value: 'home',
                    columnName: 'home',
                }, {
                    name: '微页面',
                    value: 'wepage',
                    columnName: 'wepage',
                }, {
                    name: '个人中心',
                    value: 'user_center',
                    columnName: 'user_center',
                // }, {
                //     name: '商品列表页',
                //     value: 'product_list_page',
                //     columnName: 'product_list_page',
                }],
                default: {
                    home: {select:true}, 
                    wepage: {select:false}, 
                    user_center: {select:false},
                    product_list_page: {select:false}
                }
            }, {
                name: 'type',
                type: 'radio',
                displayName: '选择模板：',
                isUserProperty: true,
                source: [{
                    name: '自定义菜单样式',
                    value: 'weixin'
                }, {
                    name: 'APP导航模式',
                    value: 'slide'
                }],
                default: 'weixin'
            }]
        }, {
            group: '',
            groupClass:'xui-propertyView-navbar-navs',
            fields: [{
                name: 'items',
                type: 'dynamic-generated-control',
                isUserProperty: true,
                isShowCloseButton: true,
                minItemLength: 1,
                maxItemLength: 3,
                default: []
            }]
        }
    ],

    propertyChangeHandlers: {
    	type: function($node, model, value) {
            W.WEAPAGE_NAVBARTYPE = value;
            var oldType = model.previous('type');

            this.type2items[oldType] = model.get('items');
            this.type2components[oldType] = this.components;

            var items = this.type2items[value];
            if (!items) {
                model.set('items', [], {silent:true});
                this.components = [];
                _.each(this.dynamicComponentTypes, function(componentType) {
                    if (componentType.model) {
                        //只有在提供model的情况下才创建dynamic component
                        if (isNaN(componentType.model)) {
                            var component = W.component.Component.create(componentType.type, componentType.model);
                            this.addComponent(component);;
                        } else {
                            for (var i = 0; i < componentType.model; i++) {
                                var component = W.component.Component.create(componentType.type, {});
                                this.addComponent(component);
                            }
                        }
                    }
                }, this);
            } else {
                model.set('items', this.type2items[value], {silent:true})
                this.components = this.type2components[value];
            }
            xwarn('-------------------')
            xwarn(model.get('items'));

            // 修改 一级菜单 限制
            var titleMaxLength = 5;
            var propertyViewTitle = "";
            var otherUpdateDisplayName = "";
            if (oldType == 'weixin') {
                this.name2field['items'].maxItemLength = 999;
                titleMaxLength = 10;
                propertyViewTitle = '一级分类';
                otherUpdateDisplayName = '分类';
            } else {
                this.name2field['items'].maxItemLength = 3;
                titleMaxLength = 5;
                propertyViewTitle = '一级菜单';
                otherUpdateDisplayName = '菜单';
            }
            // 修改 一级菜单 标题的字数限制
            _.each(this.components, function(subComponent) {
                if (subComponent.setLimitation) {
                    subComponent.setLimitation({
                        titleMaxLength: titleMaxLength
                    });
                    subComponent.updateViewTitle({
                        propertyViewTitle: propertyViewTitle,
                        otherUpdateDisplayName: otherUpdateDisplayName
                    })
                }
            });
            this.refresh($node, {resize:true, refreshPropertyView:true});
        },
        items: function($node, model, value) {
            this.refresh($node, {resize:true, refreshPropertyView:true});
        }
    },

    initialize: function(obj) {
        this.super('initialize', obj);

        if (this.model.get('type') == 'slide') {
            this.name2field['items'].maxItemLength = 999;
        }
        W.WEAPAGE_NAVBARTYPE = this.model.get('type');
        this.type2items = {};
        this.type2components = {};
    }
});
