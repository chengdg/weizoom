/**
 * @class W.component.weapp.ItemList
 * 
 */
ensureNS('W.component.weapp');
W.component.weapp.ItemList = W.component.Component.extend({
	type: 'weapp.item_list',
	propertyViewTitle: '商品列表',

	properties: [
       {
            group: '关联链接',
            fields: [{
                name: 'type',
                type: 'radio',
                displayName: '显示方式',
                isUserProperty: true,
                source: [{name:'大图', value:'0'},{name:'小图', value:'1'},{name:'一大两小', value:'2'},{name:'列表', value:'3'}],
                default: '2'
            },{
                name: 'itemname',
                type: 'checkbox',
                displayName: '商品名称',
                isUserProperty: true,
                source: [{name:'显示商品名', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'}}
            },{
                name: 'price',
                type: 'checkbox',
                displayName: '价格',
                isUserProperty: true,
                source: [{name:'显示价格', value:'0',columnName:'c0'}],
                default: {c0:{select:'True'},c1:{select:'True'}}
            },{
                name: 'style',
                type: 'radio',
                displayName: '购物车图标',
                isUserProperty: true,
                source: [{name:'无', value:''},{name:'样式一', value:'0'},{name:'样式二', value:'1'},{name:'样式三', value:'2'},{name:'样式四', value:'3'}],
                default:'2'
            },{
                name: 'count',
                type: 'radio',
                displayName: '显示个数',
                isUserProperty: true,
                source: [{name:'6', value:'6'},{name:'12', value:'12'},{name:'18', value:'18'}],
                default: '6'
            },{
                name: 'target',
                type: 'dialog_select',
                displayName: '内容来源',
                isUserProperty: true,
                dialogParameter: '{"workspace_filter":"mall", "data_category_filter":"category"}',
                triggerButton: '选择内容...',
                dialog: 'W.dialog.workbench.SelectLinkTargetDialog'
            }]
        }
    ],

    propertyChangeHandlers: {
        itemname: function($node, model, value){
            if(value.c0.select)
                $node.find('.wa-inner-title').show();
            else
                $node.find('.wa-inner-title').hide();
        },
        price: function($node, model, value){
            if(value.c0)
                if(value.c0.select)
                    $node.find('.wa-inner-price').show();
                else
                    $node.find('.wa-inner-price').hide();

            if(value.c1)
                if(value.c1.select)
                    $node.find('.wa-inner-shopCar').show();
                else
                    $node.find('.wa-inner-shopCar').hide();
        },
        type: function($node, model, value){
            for(var i=0; i<4; i++)
                      $node.find('>ul').removeClass('wui-block-type'+i);
                  $node.find('>ul').addClass('wui-block-type'+value);
                  W.Broadcaster.trigger('component:resize', this);
        },
        style: function($node, model, value){
            for(var i=0; i<4; i++)
                $node.find('.wa-inner-shopCar').removeClass('wui-shopCar-style'+i);
            $node.find('.wa-inner-shopCar').addClass('wui-shopCar-style'+value);
        },
        target: function($node, module, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            var productName = data['meta']['name'];
            $('.x-targetText').text(data.data_path);
            var categoryId = data['meta']['id'];

            W.getLoadingView().show();
            api = '';
            data_type = data['meta']['type'];
            if (data_type == 'article_category') {
                api = 'articles_by_category_id/get';
            } else if (data_type == 'product_category') {
                api = 'products_by_category_id/get';
            }
            W.getApi().call({
                app: 'webapp',
                api: api,
                args: {
                    id: categoryId,
                    count: module.get('count')
                },
                success: function(apidata) {
                    W.getLoadingView().hide();
                    $node.find('li').each(function(i,n){
                        if(apidata.length > i){
                            t_data = apidata[i]
                            var $innerPic = $(n).find('.wui-inner-pic');
                            var $img = $innerPic.find('img');
                            var imgSrc = t_data.pic;
                            if ($img.length === 0) {
                                $innerPic.empty().append('<img src="'+imgSrc+'" />');
                            } else {
                                $img.attr('src', imgSrc);
                            }
                            $(n).find('.wa-inner-title').text(t_data.name);
                            $(n).find('.wa-inner-price').text('¥'+t_data.price);
                        }else{
                            $(n).find('.wui-inner-pic').html($('<p/>').append(data['data_path']));
                            $(n).find('.wa-inner-title').text(data['data_path']);
                        }
                        

                    });
                },
                error: function(resp) {
                    W.getLoadingView().hide();
                    W.getErrorHintView().show('加载分类数据失败!');
                }
            })
        }
    }
}, {
    indicator: {
        name: '商品列表',
        imgClass: 'componentList_component_product_list'
    }
});