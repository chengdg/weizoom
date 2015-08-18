/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 右侧的property视图
 * @class
 */
ensureNS('W.workbench');
W.workbench.PropertyView = Backbone.View.extend({
	el: '',

	events: {
        'input .propertyGroup_property_input > input': 'onChangeInputContent',
        'input .propertyGroup_property_input .xa-valueInput': 'onChangeInputContent',
        'input .propertyGroup_property_input > textarea': 'onChangeInputContent',
        'change .propertyGroup_property_input > select': 'onChangeSelection',
        'change .propertyGroup_property_input input[type="radio"]': 'onChangeSelection',
        'change .propertyGroup_property_input input[type="checkbox"]': 'onChangeCheckboxSelection',
        'click .btn-group > .btn': 'onClickRadioGroupButton',
        'click .propertyGroup_property_dynamicControlField_buttons > .xa-addDynamicComponent': 'onClickAddDynamicComponentButton',
        'click .propertyGroup_property_dynamicControlField_title': 'onClickDynamicComponentTitle',
        'click .propertyGroup_property_dynamicControlField_title .icon-remove': 'onClickRemoveDynamicComponentButton',
        'click .propertyGroup_property_dialogSelectField .btn': 'onClickOpenDialogButton',
        'click .xa-dialogTrigger': 'onClickOpenDialogButton',
        'click .xa-link-menu': 'onClickLinkMenuButton',
        'input .xa-selectLink-url': 'onManualInputUrl',
        'click .xa-selectLink-close': 'onClickCloseLinkButton',
        'click .propertyGroup_property_htmlEditorField .btn': 'onClickSaveHtmlEditorContentButton',
        'keypress .propertyGroup_property_htmlEditorField pre': 'onHtmlEditorKeypress',

        'click [data-action="editProperty"]': 'onClickEditPropertyButton',
        'click [data-action="editDatasource"]': 'onClickEditDatasourceButton',
        'click select.datasourceEditor_pageSelector': 'onChangeDatasourcePageSelection',
        'click #datasourceEditor_submitBtn': 'onClickSubmitDatasourceEditorButton',

        'click .xa-component': 'onClickComponent',
        'click .xa-removeImageButton': 'onClickRemoveDynamicComponentButton',
        'click .xa-protocol-deleteData':'onClickDeleteData',
        'mouseover .propertyGroup_property_dynamicControlField_control': 'onMouseoverField',
        'mouseout .propertyGroup_property_dynamicControlField_control': 'onMouseoutField',    

        'click .xa-colorPickerTrigger': 'onClickColorPickerTrigger'
	},

    getTemplate: function() {
        $('#workbench-property-view-tmpl-src').template('workbench-property-view-tmpl');
        return "workbench-property-view-tmpl";
    },

    getDatasourceFieldsTemplate: function() {
        $('#datasource-editor-fields-selector-tmpl-src').template('datasource-editor-fields-selector-tmpl');
        return "datasource-editor-fields-selector-tmpl";
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
        this.left = options.left || 0;
        this.template = this.getTemplate();
        this.component = null;
        this.actionReferenceComponent = null;
        this.onlyShowUserProperty = options.onlyShowUserProperty || false;

        this.type2initializer = {
            "wepage.block": this.initSliderView,
            "wepage.title":this.initDateTime, 
            "wepage.richtext": this.initRichTextView, 
            "wepage.item_group": this.initProductsView, 
            "wepage.item_list": this.initProductsView,
            "wepage.pageheader": _.bind(this.initPageHeader, this),
            "colorpicker": _.bind(this.initColorPicker, this),
            "secondnav": _.bind(this.initSecondNav, this)
        };


        //design page中切换component的响应函数
        /*
        W.util.changeComponentInDesignPageHandlers.push(function() {
            if (!W.validate(this.$el)) {
                W.getErrorHintView().show('请完成必填的property信息!');
                return false;
            }
            return true;
        });
        */

        W.Broadcaster.on('component:select', _.bind(this.onUpdatePropertyEditor, this));
        W.Broadcaster.on('component:display_error_hint', _.bind(this.onShowValidateError, this));
        W.Broadcaster.on('component:refresh_field_editor', _.bind(this.onUpdateFieldEditor, this));
        W.Broadcaster.on('mobilepage:delete-widget', _.bind(this.onDeleteMobilePageWidget, this));
        W.Broadcaster.on('designpage:drag_widget', _.bind(this.onDragWidgetInDesignPage, this));
        W.Broadcaster.on('component:cancel_linkMenu', _.bind(this.onCancelLinkMenu, this));

        W.Broadcaster.on('link-url:selected', _.bind(this.onSelectedLinkUrl, this));
        this.pageRegex = /\.page$/;
        this.isViewDisplayed = false;
        this.inValidateMode = false;
	},

    render: function() {
        /*
        this.$el.append($.tmpl(this.template, {}));
        */
    },

    /**
     * onCancelLinkMenu: 关闭linkMenu Div层
     */
    onCancelLinkMenu: function(){
        $('.xa-linkActionMenu').hide();
    },

    /**
     * onClickLinkMenuButton: 点击选择链接按钮
     */
    onClickLinkMenuButton: function(event){
        var el = $(event.currentTarget).parent('.xui-eidt-urlBox');
        // 实例化选择链接view
        this.linkView = W.getSelectWebSiteLinkView({
            el: el
        });
        this.linkView.onClickLinkMenu(event);
    },

    /**
     * onSelectedLinkUrl: 选择完成链接后，调用该函数
     */
    onSelectedLinkUrl: function(event, data){
        var $input = $(event.currentTarget).parent().find('input[type="hidden"]');
        $input.val(data).trigger('input');
    },

    /**
     * onManualInputUrl: 手工输入链接的响应函数
     */
    onManualInputUrl: function(event) {
        event.stopPropagation();
        event.preventDefault();

        var $input = $(event.currentTarget);
        var url = $input.val();
        if (url.length >= 7 && url.substr(0, 3) != './?' && url.substr(0, 7) != 'http://') {
            url = 'http://'+ url
            $input.val(url);
        };
        var linkData = {data:url, data_path:"", type:'manualInput'};
        var $targetInput = $input.parent().find('input[type="hidden"]');
        $targetInput.val(JSON.stringify(linkData)).trigger('input');
    },

    /**
     * onClickCloseLinkButton: 关闭已选择的链接
     */
    onClickCloseLinkButton: function(event){        
        event.stopPropagation();
        event.preventDefault();

        var $input = $(event.currentTarget).parents('div.propertyGroup_property_input').find('input[type="hidden"]');
        $input.val("").trigger('input');
    },

    /**
     * getTargetComponent: 获得要发送event的component
     */
    getTargetComponent: function($node) {
        var $parents = $node.parents('.propertyGroup_property_dynamicControlField_control');
        if ($parents.length > 0) {
            var cid = $parents.eq(0).attr('data-dynamic-cid');
            if (cid) {
                return W.component.CID2COMPONENT[cid];
            }
        } else {
            return this.component;
        }
    },

    /**
     * updateDynamicComponents: 更新dynamic component信息
     */
    updateDynamicComponents: function($item) {
        var orderedCids = [];
        this.$(".propertyGroup_property_dynamicControlField_control").each(function() {
            orderedCids.push(parseInt($(this).attr('data-dynamic-cid')));
        });
        xlog('[property view]: update ' + this.component.cid + "'s dynamic components to [" + orderedCids + "]");

        var $dynamicControl = null;
        if ($item) {
            $dynamicControl = $item.parents(".propertyGroup_property_dynamicControlField");
        } else {
            $dynamicControl = this.$(".propertyGroup_property_dynamicControlField");
        }
        
        var attr = $dynamicControl.attr('data-field');
        this.component.model.set(attr, orderedCids);
    },

    /**
     * enableSortDynamicComponent: 开启dynamic component的拖动排序功能
     */
    enableSortDynamicComponent: function() {
        var _this = this;
        this.$(".propertyGroup_property_dynamicControlField").sortable({
            axis: 'y',
            opacity: '0.4',
            cursor: 'move',
            handle: '.propertyGroup_property_dynamicControlField_title',
            start: function() {
                xlog('[property view]: start sort...');
            },
            stop: function(event, ui) {
                _this.updateDynamicComponents(ui.item);
            }
        });
    },

    /*********************************************************
     * onSwitchPage: 切换页面时，清空属性编辑器
     *********************************************************/    
    onSwitchPage: function(component) {
        this.$el.empty();
    },    

    /**
     * onDeleteMobilePageWidget: mobilepage:delete_widget事件的响应函数
     */
    onDeleteMobilePageWidget: function() {
        this.$el.hide().empty();
        this.isViewDisplayed = false;
    },

    onDragWidgetInDesignPage: function($mobilePage, itemUid, targetContainerUid) {
        var offset = $mobilePage.find('[data-cid="'+itemUid+'"]').offset();
        this.$el.css('margin-top', offset.top + 151 + 'px');
    },

    /*********************************************************
     * onUpdatePropertyEditor: 更新属性编辑器
     *********************************************************/    
    onUpdatePropertyEditor: function(component, offset, options) {
        xlog("[property view]: update property editor");
        //跳过对wepage.page的处理
        var isPage = this.pageRegex.test(component.type);
        if (isPage) {
            if (!_.isObject(offset)) {
                //当offset不是object，则可能是null，可能是mobilepage:wait_page，这时应该跳过property editor更新
                return true;
            }
        }

        var isRenderForNewComponent = this.component ? (this.component.cid !== component.cid) : true;

        if (!isRenderForNewComponent) {
            if (options && options.forceUpdatePropertyView) {
                //强制刷新
            } else {
                return;
            }
        }

        /*
        if (!(options && options.silent)) {
            this.component = component;
        }
        */
        this.component = component;
        if (options && options.actionReferenceComponent) {
            this.actionReferenceComponent = options.actionReferenceComponent;
        } else {
            this.actionReferenceComponent = component;
        }

        var dynamicComponents = _.sortBy(_.filter(component.components, function(component) {
            if (component.selectable === 'no') {
                return true;
            }

            if (component.forceDisplayInPropertyView == 'yes') {
                return true;
            }

            return false;
        }), function(component) {
            return component.model.get('index');
        });
        /*
        _.each(component.dynamicComponentTypes, function(componentType) {
            xlog(W.component.getPropertyViewTitleByType(componentType.type));
        });
        */

        //确定group的isUserProperty
        _.each(component.properties, function(property_group) {
            property_group.isUserProperty = false;
            var fieldCount = property_group.fields.length;
            for (var i = 0; i < fieldCount; ++i) {
                var field = property_group.fields[i];
                if (field.isUserProperty) {
                    property_group.isUserProperty = true;
                    break;
                }
            }
        });

        //合并component.dynamicComponentTypes中相同类型的sub component，支持添加按钮的显示
        var unifiedDynamicComponentTypes = {};
        _.each(component.dynamicComponentTypes, function(dynamicComponentType) {
            var type = dynamicComponentType['type'];
            if (!unifiedDynamicComponentTypes[type]) {
                unifiedDynamicComponentTypes[type] = dynamicComponentType;
            }
        });
        component.unifiedDynamicComponentTypes = _.values(unifiedDynamicComponentTypes);

        var title = component.propertyViewTitle;
        if (!this.onlyShowUserProperty) {
            title += ('(' + component.cid + ')');
        }

        //填充name2field
        /*
        var name2field = {};
        for (var i = 0; i < component.properties.length; ++i) {
            var propertyGroup = component.properties[i];
            var fields = propertyGroup.fields;
            for (var j = 0; j < fields.length; ++j) {
                var field = fields[j];
                name2field[field.name] = field;
            }
        }
        component.name2field = name2field;
        */

        xlog('[property view]: ' + component.type);
        xlog({
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            dynamicComponents: dynamicComponents, 
            title: title, 
            property_groups: component.properties, 
            model: component.model,
            datasourceProject: W.data.datasourceProject
        });
        var $node = $.tmpl(this.template, {
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            dynamicComponents: dynamicComponents, 
            title: title, 
            property_groups: component.properties, 
            model: component.model,
            datasourceProject: []
        });

        this.$(".propertyGroup_property_dynamicControlField").sortable('destroy');
        var top = offset.top;
        /*
        if (top < 0) {
            top = 0;
        }
        */
        this.$el.empty().append($node);
        if (isRenderForNewComponent || (options && options.forceUpdatePropertyView)) {
            this.$el.css('margin-top', top + 151 + 'px')
        }
        if (!this.isViewDisplayed) {
            this.isViewDisplayed = true;
            this.$el.show();
        }
        if (component.canEditHtml()) {
            W.data.htmlEditor = ace.edit("htmlEditor"+component.cid);
            W.data.htmlEditor.setTheme("ace/theme/monokai");
            W.data.htmlEditor.getSession().setMode("ace/mode/html");
            this.$('.propertyGroup_property_htmlEditorField').show();
        }

        if (this.type2initializer[component.type]) {
            this.type2initializer[component.type](this.$el);
        }

        //初始化第三方插件
        var _this = this;
        this.$el.find('.xa-thirdPartyPlugin').each(function() {
            var $el = $(this);
            var pluginName = $el.data('plugin');
            var initializer = _this.type2initializer[pluginName];
            if (initializer) {
                initializer($el);
            }
        });

        this.enableSortDynamicComponent();

        //this.$('input').eq(0).focus();   
        this.$el.show();     

        //判断是否进行输入检查
        if (isRenderForNewComponent) {
            this.inValidateMode = false;
        } else {
            if (this.inValidateMode) {
                this.onShowValidateError();
            }
        }

        this.onCancelLinkMenu();
    },

    /*********************************************************
     * onUpdateFieldEditor: 更新属性编辑器中field对应的区域
     *********************************************************/    
    onUpdateFieldEditor: function(fieldName) {
        var component = this.component;
        var property_groups = [{
            group: '',
            isUserProperty: true,
            fields: [component.getFieldByName(fieldName)]
        }];

        xlog('[property view]: update editor for component('+component.type+')-field('+fieldName+')');  
        xlog({
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            property_groups: property_groups, 
            model: component.model
        });  
        var $node = $.tmpl(this.template, {
            onlyShowUserProperty: this.onlyShowUserProperty,
            component: component,
            dynamicComponents: [], 
            title: '', 
            property_groups: property_groups, 
            model: component.model
        });

        var $target = this.$('[data-field-anchor="'+fieldName+'"]');
        $target.empty().append($node.find('.propertyGroup_property').children());
    },

    /*********************************************************
     * onShowValidateError: comopnent:validate的响应函数
     *********************************************************/    
    onShowValidateError: function(cid) {
        var _this = this;
        this.inValidateMode = true;
        W.validate(_this.$el);
        var scrollTop = _this.$el.offset().top - 50;
        window.scrollTo(0,scrollTop);
    },

    /*********************************************************
     * onChangeInputContent: 改变输入框中的内容
     *********************************************************/
    onChangeInputContent: function(event) {
        var $input = $(event.target); 
        var value = $input.val();
        var attr = $input.attr('data-field');
        this.getTargetComponent($input).model.set(attr, value);
    },

    /*********************************************************
     * onChangeSelection: 改变select的选项
     *********************************************************/
    onChangeSelection: function(event) {
        var $select = $(event.target);
        var value = $select.val();
        var attr = $select.attr('data-field');
        this.getTargetComponent($select).model.set(attr, value);
        $select.parent('label').siblings().removeClass('xui-selected');
        $select.parent('label').siblings().find('i').hide();
        $select.parent('label').addClass('xui-selected');
        $select.siblings('i').css('display','block');
    },

    /*********************************************************
     * onChangeTextCheckboxSelection: 改变text-checkbox下checkbox的select的选项
     *********************************************************/
    onChangeTextCheckboxSelection: function(event) {
        var $checkboxGroups = $(event.currentTarget).parents('div.propertyGroup_property_textCheckboxField');
        var results = {};
        $checkboxGroups.find('input[type="checkbox"]').each(function() {
            var $checkbox = $(this);
            results[$checkbox.attr('data-column-name')] = {select: $checkbox.is(':checked')};
        });

        var attr = $(event.currentTarget).attr('data-field');
        //this.component.model.set(attr, results);
        this.getTargetComponent($checkboxGroups).model.set(attr, results);
    },

    /*********************************************************
     * onChangeCheckboxSelection: 改变checkbox的select的选项
     *********************************************************/
    onChangeCheckboxSelection: function(event) {
        /*
        var $checkbox = $(event.currentTarget);
        var isSelected = $checkbox.prop('checked');

        var attr = $(event.currentTarget).attr('data-field');
        this.getTargetComponent($checkbox).model.set(attr, isSelected);
        */
        var $checkbox = $(event.currentTarget);
        var isSelected = $checkbox.prop('checked');

        var attr = $(event.currentTarget).attr('data-field');
        var column = $(event.currentTarget).attr('data-column-name');
        var attrValue = _.deepClone(this.getTargetComponent($checkbox).model.get(attr));
        attrValue[column] = {select:isSelected};
        this.getTargetComponent($checkbox).model.set(attr, attrValue);
    },

    /**
     * onClickRadioGroupButton: 点击radio group中的button后的响应函数
     */
    onClickRadioGroupButton: function(event) {
        var $node = $(event.currentTarget);
        var $groupNode = $node.parent();
        $groupNode.find('.btn-primary').removeClass('btn-primary');
        $groupNode.find('.icon-white').removeClass('icon-white');
        $node.addClass('btn-primary').find('i').addClass('icon-white');

        var attr = $groupNode.attr('data-field');
        var value = $node.attr('data-value');
        this.component.model.set(attr, value);
    }, 


    /**
     * onClickAddDynamicComponentButton: 点击dynamic component区域中的添加button后的响应函数
     */
    onClickAddDynamicComponentButton: function(event, modelData) {
        var $node = $(event.currentTarget);
        var componentType = $node.attr('data-component');
        var component = W.component.Component.create(componentType);
        if (modelData) {
            component.updateModel(modelData);
        }
        this.component.addComponent(component, {isAddDynamicComponent: true});

        xlog('[property view]: click add dynamic component button, and crete component' + component.type);
    },

    /**
     * onClickRemoveDynamicComponentButton: 点击dynamic component区域中的remove button后的响应函数
     */
    onClickRemoveDynamicComponentButton: function(event) {
        var $node = $(event.currentTarget);
        var $control = $node.parents('.propertyGroup_property_dynamicControlField_control').eq(0);
        var parentComponentCid = parseInt($control.attr('data-parent-cid'));
        var cid = parseInt($control.attr('data-dynamic-cid'));
        xlog('[property view]: remove ' + cid + ' from ' + parentComponentCid);
        $control.remove();
        W.component.getComponent(parentComponentCid).removeComponent(cid);

        this.updateDynamicComponents();
    },

    /**
     * onClickDynamicComponentTitle: 点击dynamic component区域的title bar后的响应函数
     */
    onClickDynamicComponentTitle: function(event) {
        var $titleBar = $(event.currentTarget);
        if ($titleBar.find('.icon-chevron-down').length > 0) {
            //收缩title
            var $propertyGroup = $titleBar.parents('.propertyGroup');
            $propertyGroup.find('.icon-chevron-down').removeClass('icon-chevron-down');
            $propertyGroup.find('.propertyGroup_property_dynamicControlField_activeContent').hide().removeClass('propertyGroup_property_dynamicControlField_activeContent');
        } else {
            //切换title
            var $propertyGroup = $titleBar.parents('.propertyGroup');
            $propertyGroup.find('.icon-chevron-down').removeClass('icon-chevron-down');
            $propertyGroup.find('.propertyGroup_property_dynamicControlField_activeContent').hide().removeClass('propertyGroup_property_dynamicControlField_activeContent');
            $titleBar.find('.icon-chevron-right').addClass('icon-chevron-down');
            $titleBar.next().addClass('propertyGroup_property_dynamicControlField_activeContent').show();
        }

        this.$el.scrollTop(10000); //确保dynamic component展开后，其编辑区域位于屏幕中
    },

    /**
     * onClickOpenDialogButton: 点击打开select dialog的按钮后的响应函数
     */
    onClickOpenDialogButton: function(event) {
        var $button = $(event.currentTarget);
        var dialog = $button.attr('data-target-dialog');

        var parameter = null;
        var parameterStr = $button.attr('data-dialog-parameter');
        
        if (parameterStr) {
            parameter = W.data.getData(parameterStr, this.component, $button);
        }

        var options = {
            success: _.bind(function(data) {
                        if ($button.hasClass('xa-addDynamicComponentTrigger')) {
                            var event = {currentTarget: $button.get(0)}
                            var datas = data;
                            _.each(datas, function(data) {
                                this.onClickAddDynamicComponentButton(event, data);
                            }, this);
                        } else {
                            var $input = $button.parent().find('input[type="hidden"]');
                            var data = data;
                            if (typeof(data) == 'object') {
                                data = JSON.stringify(data)
                            }
                            $input.val(data).trigger('input');
                        }
                    }, this),
            component: this.component,
            $button: $button
        }

        if (parameter) {
            _.extend(options, parameter);
        }
        
        W.dialog.showDialog(dialog, options);
    },

    /**
     * onClickDeleteData: 点击.xa-deleteData的按钮后的响应函数
     */
    onClickDeleteData: function(event) {
        var $link = $(event.currentTarget);
        var $input = $link.parents('.propertyGroup_property_input').find('.xa-valueInput');
        if ($input.length === 0) {
            $input = $link.parents('.propertyGroup_property_input').find('input[type="hidden"]');
        }
        var deletedValue = $link.data('protocolDeletedValue');
        $input.val(deletedValue).trigger('input');
    },

    /**
     * onClickSaveHtmlEditorContentButton: 点击保存html editor按钮后的响应函数
     */
    onClickSaveHtmlEditorContentButton: function(event) {
        var $button = $(event.currentTarget);
        var attr = $button.parents('.propertyGroup_property_htmlEditorField').find('pre').eq(0).attr('data-field');
        var value = W.data.htmlEditor.getValue();
        this.component.model.set(attr, value);
    },

    /**
     * onHtmlEditorKeypress: 在html editor中按下键盘的响应函数
     */
    onHtmlEditorKeypress: function(event) {
        if (event.ctrlKey && event.which === 115) {
            event.preventDefault();
            event.stopPropagation();

            var clickEvent = {};
            xlog($(event.currentTarget).parents('.propertyGroup_property_htmlEditorField').find('.btn'));
            clickEvent.currentTarget = $(event.currentTarget).parents('.propertyGroup_property_htmlEditorField').find('.btn').get(0);
            this.onClickSaveHtmlEditorContentButton(clickEvent);
        }    
    },

    /**
     * toggleEditor: 切换action button的active状态，切换editor
     */
    toggleEditor: function(event) {
        var $button = $(event.currentTarget);
        if ($button.hasClass('active')) {

        } else {
            this.$('.sectionActionBar a').removeClass('active');
            $button.addClass('active');
        }

        var $target = this.$($button.attr('data-target'));
        if ($target.length > 0) {
            this.$('.propertyView_actionTarget').hide();
            $target.show();
        }
    },

    /**
     * onClickEditPropertyButton: 点击header中“编辑属性”按钮的响应函数
     */
    onClickEditPropertyButton: function(event) {
        this.toggleEditor(event);

        this.$('input').eq(0).focus();
    },

    /**
     * onClickEditDatasourceButton: 点击header中“编辑数据源”按钮的响应函数
     */
    onClickEditDatasourceButton: function(event) {
        /*
        this.toggleEditor(event);

        var existedDatasource = this.component.model.get('datasource');
        var datasource_page_id = existedDatasource.__datasource_page_id;
        if (datasource_page_id && datasource_page_id !== 'null') {
            var $pageSelector = this.$('select[name="__datasource_page_id"]').eq(0);
            $pageSelector.val(__datasource_page_id);

            var event = {
                currentTarget: $pageSelector[0]
            }
            this.onChangeDatasourcePageSelection(event);
        }
        */
        var dialog = 'W.workbench.SelectDatasourceDialog';
        var options = {
            success: _.bind(function(datasource) {
                this.component.model.set('datasource', datasource);
            }, this),
            component: this.component
        }
        W.dialog.showDialog(dialog, options);
    },

    /**
     * onChangeDatasourcePageSelection: 点击header中“编辑数据源”按钮的响应函数
     */
    onChangeDatasourcePageSelection: function(event) {
        var datasource_page_id = $(event.currentTarget).val();
        if (datasource_page_id === 'null') {
            return;
        }
        
        var datasourcePage = _.findWhere(parent.W.data.datasourceProject, {id: datasource_page_id});        
        var $node = $.tmpl(this.getDatasourceFieldsTemplate(), {
            dataItems: this.component.datasource,
            fields: datasourcePage.fields,
            existedDatasource: this.component.model.get('datasource')
        });

        this.$('#datasrouceEditor_dateItems').empty().append($node);
    },

    /**
     * onClickSubmitDatasourceEditorButton: 点击header中“编辑数据源”按钮的响应函数
     */
    onClickSubmitDatasourceEditorButton: function(event) {
        var $datasourceEditor = this.$('#datasourceEditor');
        var datasource = {};
        $datasourceEditor.find('select').each(function() {
            $select = $(this);
            datasource[$select.attr('name')] = $select.val();
        });

        this.component.model.set('datasource', datasource);
    },

    onClickComponent: function(event) {
        var componentType = $(event.currentTarget).attr('data-component-type');
        xlog('create component with type ' + componentType);
        var newComponent = W.component.Component.create(componentType);
        W.Broadcaster.trigger('component:create', newComponent, this.actionReferenceComponent);
    },

    initSliderView: function($el){
        _.each($el.find('.xa-progress-bar'), function(item){
            var $item = $(item);
            var value = $item.val();
            $item.slider({
                min: 20,
                max: 100,
                step: 1,
                value: parseInt(value),
                formatter: function(value) {
                    return '像素' + value;
                }
            });

            $item.on("slide", function(event) {
                $(event.currentTarget).trigger("input");
            });
        });       
    },

    initRichTextView: function($el){
        var node = $el.find('.xa-rich-text');
		this.editor = new W.view.common.RichTextEditor({
    		el: node,
            maxCount: 10000,
    		type: 'full',
    		width:'100%',
            imgSuffix: "uid="+W.uid	
		});
		this.editor.bind('contentchange', function() {
            node.val(this.editor.getHtmlContent()).trigger('input');
			// this.textMessage.set('text', this.editor.getHtmlContent());
		}, this);
		//this.editor.setContent('this.answer');
		this.editor.render();

    },

    initProductsView: function($el){
        var type = $el.find('[name="type"]:checked').val();
        var cardType = $el.find('[name="card_type"]:checked').val();
        console.log('type', type, cardType);
        if (type == 3) {
            $el.find('.xa-nameBlock').hide();
        }
        if (type == 2 && cardType == 1) {
            $el.find('.xa-itemname').hide();
        }
        if (type == 1 && cardType == 1) {
            $el.find('.xa-itemname').hide();
        }
    },

    initPageHeader: function($el) {
        var $uploaderContainer = $el.find('.xa-imageUploader').eq(0);
        var $uploader = $uploaderContainer.find('.xa-imageUploader-uploader');
        //var $pageHeader = $el.find('.xa-imageUploader .xa-imageUploader-uploader').eq(0);
        this.imageUploader = new W.view.common.ImageView({
            el: $uploader.get(0),
            height: 640,
            width: 640,
            sizeLimit: 1024,
            autoShowHelp: true,
            help: '建议尺寸：160*160 像素',
            autoShowImage: false
        });
        this.imageUploader.bind('upload-image-success', function(path) {
            var $input = $el.find('.xa-imageUploader input[type="hidden"]');
            $input.val(path).trigger('input');
        });
        this.imageUploader.render();

        if($.trim($uploaderContainer.data('value'))) {
            $uploaderContainer.find('.uploadify-button').text('修改');
        }
    },

    initColorPicker: function($el) {
        _.delay(function() {
            var hex = $.trim($el.val());
            hex = hex.substring(1); //去掉#
            $el.colpick({
                layout: 'rgbhex',
                submitText: '确定',
                color: hex,
                onSubmit: function(hsb, hex, rgb, el) {
                    var $el = $(el);
                    $el.colpickHide();
                    $el.val('#'+hex).trigger('input');
                }
            })
        }, 100);
    },

    initSecondNav: function($el) {
        W.createWidgets($el.parent());

        var $input = $el.parent().find('input[name="second_navs"]');
        var view = $el.data('view');
        xwarn(view);

        view.bind('update-show-box', function($el, length){
            var urlBox = $el.parents('.propertyGroup_property_dynamicControlField_content').children('.propertyGroup_property_linkSelectField').find('.xui-eidt-urlBox');
            var secondeNavsPrompt = urlBox.next('.xa-seconde-navs-prompt');
            if (length == 0) {
                console.log('urlBox.show()', 'prompt.hide()')
                urlBox.show();
                secondeNavsPrompt.hide();
            }else{
                urlBox.hide();
                secondeNavsPrompt.css("display", "inline");
            }
        }, this)

        view.bind('update-data', function(data){
            $input.val(data).trigger('input');
        });
    },


    initDateTime:function($el){
        var $input =$el.find('.xa-time');
        var view = new W.view.common.DatePicker({
            el: $input.get(0)
        });
        view.render();
        view.bind('select-date', function(){
            $input.trigger('input');
        });
        $input.bind('change', function(){
            $input.trigger('input');
        });
    },

    onMouseoutField: function(event){
        this.$el.find('.propertyGroup_property_dynamicControlField_control').children('.close').hide();
    },

    onMouseoverField: function(event){
        var $el = $(event.currentTarget);
        this.$el.find('.propertyGroup_property_dynamicControlField_control').children('.close').hide();
        $el.children('.close').show();
    },

    onClickColorPickerTrigger: function(event){
        var $el = $(event.currentTarget);
        var $input = $el.parents('.propertyGroup_property_input').find('.xa-valueInput');
        $input.trigger('click');
    }
});