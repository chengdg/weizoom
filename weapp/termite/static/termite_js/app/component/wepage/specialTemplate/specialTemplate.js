/**
 * @class W.component.wepage.PageHeader
 * 
 */
ensureNS('W.component.wepage');
W.component.wepage.specialTemplate = W.component.Component.extend({
	type: 'wepage.specialTemplate',
    selectable: 'no',
	propertyViewTitle: '一个导航',

	properties: [
        {
            group: '属性1',
            groupClass:'',
            fields: [{
                name: 'title',
                type: 'text',
                displayName: '导航名称',
                validate: 'data-validate="require-notempty::导航名称不能为空"',
                validateIgnoreDefaultValue: true,
                maxLength:4,
                isUserProperty: true,
                placeholder:'',
                default: ''
            }, {
                name: 'target',
                type: 'select_link',
                displayName: '导航链接',
                isUserProperty: true,
                validate: 'data-validate="require-notempty::链接地址不能为空"',
                triggerButton: '从微站选择'
            },{
                name: 'image',
                displayName:'选择图标',
                type: 'dialog_select',
                isUserProperty: true,
                triggerButton: '选择图片...',
                validate: 'data-validate="require-notempty::请添加一张图片"',
                selectedButton: '修改',
                help: '建议尺寸：64*64',
                dialog: 'W.dialog.termite.SelectImagesDialog',
                dialogParameter: '{"multiSelection": false, "dialogType": 2}',
                default: ''
            }]
        }
    ],

    propertyChangeHandlers: {
         image: function($node, model, value, $propertyViewNode) {
            var data = $.parseJSON(value);
            var image = data.images[0];
            
            if ($node.get(0).tagName.toLowerCase() === 'body') {
                //图片对应的node没有被渲染，不修改图片
            } else {
                var $img = $node.find('img');
                $img.attr('src', image.url).css({
                    width: 33,
                    height: 33
                });;
                $node.find('.xa-placeholder').hide();
                if (!$img.is(':visible')) {
                    $img.show();
                }
            }

            model.set({
                image: image.url,
                width: image.width,
                height: image.height
            }, {silent: true});

            $propertyViewNode.find('.xa-dynamicComponentControlImgBox img').attr('src', image.url);
            $propertyViewNode.find('.xa-dialogTrigger').removeClass('xui-imgDisplayBtn').addClass('xui-dialogSelectedBtn').html('修改');
            $propertyViewNode.find('.xa-dynamicComponentControlImgBox').show();
            $propertyViewNode.find('.xa-dynamicComponentControlImgBox img').parents('.xa-errorHintContainer').find('.errorHint').hide();

            _.delay(function() {
                W.Broadcaster.trigger('component:resize', this);
            }, 100);
            
            // if (data.type === 'newImage') {
            //     W.resource.termite2.Image.put({
            //         data: image,
            //         success: function(data) {

            //         },
            //         error: function(resp) {

            //         }
            //     })
            // }
        },
        title: function($node, model, value, $propertyViewNode) {
              $node.find('.xa-inner-title').text(value);
        },       
        target: function($node, model, value, $propertyViewNode) {
            xwarn(value);
            if (value.length > 0) {
                var linkData = $.parseJSON(value);
                if (linkData.type === 'manualInput') {

                } else {
                    $propertyViewNode.find('.xa-selected-title-box').show();
                    $propertyViewNode.find('.xa-selectLink-url').val(linkData.data).attr('disabled','disabled');
                    $propertyViewNode.find('.xa-selectLink-name').text(linkData.data_path);
                    $propertyViewNode.find('.xa-link-menu').html('修改<span class="glyphicon glyphicon-menu-down"></span>');
                }

                $node.find('a').attr('href', linkData.data);
            }else{
                $propertyViewNode.find('.xa-selected-title-box').hide();
                $propertyViewNode.find('.xa-selectLink-url').val('').removeAttr('disabled');
                $propertyViewNode.find('.xa-selectLink-name').text('');
                $propertyViewNode.find('.xa-link-menu').html('从微站选择<span class="glyphicon glyphicon-menu-down"></span>');

                $node.find('a').attr('href', "#")
            }
        }
    },

    initialize: function(obj) {
    	this.super('initialize', obj);
    }
 });