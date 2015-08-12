/**
 * @class W.component.wepage.Navbar
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.Navar = W.component.Component.extend({
	type: 'wepage.navbar',
	propertyViewTitle: '底部导航',
    selectable: 'no',

	properties: [
        {
            group: '',
            groupClass:'xui-propertyView-navbar-settings',
            fields: [{
                name: 'pages',
                type: 'checkbox',
                displayName: '将导航应用在以下页面',
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
                }, {
                    name: '商品列表页',
                    value: 'product_list_page',
                    columnName: 'product_list_page',
                }],
                default: {
                    home: {select:true}, 
                    wepage: {select:true}, 
                    user_center: {select:true},
                    product_list_page: {select:true}
                }
            }, {
                name: 'type',
                type: 'radio',
                displayName: '模板',
                isUserProperty: true,
                source: [{
                    name: '微信菜单',
                    value: 'weixin'
                }, {
                    name: '侧滑菜单',
                    value: 'slide'
                }],
                default: 'weixin'
            }]
        }, {
            group: '',
            groupClass:'xui-propertyView-navbar-navs',
            fields: []
        }
    ],

    propertyChangeHandlers: {
    	type: function($node, model, value) {
            this.refresh($node, {resize:true});
        }
    }
});
