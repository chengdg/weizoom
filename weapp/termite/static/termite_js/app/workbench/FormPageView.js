/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * form页面视图
 * @class
 */
W.workbench.FormPageView = Backbone.View.extend({
	el: '',

	events: {
        'click .componentOverlay': 'onClickComponent',
        'click #formPage_closeCoverBtn': 'onClickCloseCoverBtn',
        'click .formPage_removeComponentBtn': 'onClickRemoveComponentBtn',
        'mouseenter .componentOverlay': 'onMouseEnterComponent',
        'mouseleave .componentOverlay': 'onMouseLeaveComponent',
        'click .componentMetaInfoContainer': 'onClickPageMetaInfo',
        'click .componentListInfoContainer': 'onClickPageListInfo'
	},

    getTemplate: function() {
        $('#form-page-tmpl-src').template('form-page-tmpl');
        return "form-page-tmpl";
    },
	
	initialize: function(options) {
        this.template = this.getTemplate();
        this.type = "form";
        this.render();

        this.activeComponentNode = null;
        this.tabIndex = -1;

        W.Broadcaster.on('pagetabs:switch', _.bind(this.onSwitchPage, this));

        this.enableComponentSortable();
	},

    render: function() {
        this.el = $.tmpl(this.template, {})[0];
        this.$el = $(this.el);

        this.$newElementIndicator = this.$('.formPage_newElement');
        this.$form = this.$('form');

        var _this = this;
        var dropOptions = {
            accept: function(el) {
                return el.hasClass('btn-component');
            },
            activeClass: 'xui-droppable-active',
            over: function() {
                _this.$newElementIndicator.css({visibility: 'visible'});
            },
            out: function() {
                _this.$newElementIndicator.css({visibility: 'hidden'});
            },
            drop: function(event, ui) {
                _this.$newElementIndicator.css({visibility: 'hidden'});

                var component = W.getComponent(ui.draggable);
                if (!component) {
                    return;
                }

                //绑定component的model的change事件
                component.model.on('change', function(model) {
                    xlog('handle change event, re render component');
                    this.activeComponentNode.find('.control-group').remove();
                    this.activeComponentNode.prepend($.tmpl(component.template, model.toJSON()));
                }, _this);

                var node = $('<div class="componentContainer xui-oneComponent">');
                node.data('component', component);
                node.append($.tmpl(component.template, component.model.toJSON()));
                node.append('<div class="componentOverlay"><a href="#" class="formPage_removeComponentBtn btn btn-danger btn-mini"><i class="icon-remove icon-white"></i></a></div>')
                if (component.extraClass) {
                    node.addClass(component.extraClass);
                }
                _this.$form.append(node);

                //将新建node设置为active的node
                var event = {};
                event.currentTarget = node.find('.componentOverlay');
                _this.onClickComponent(event);

                //更新所有component的index
                var index = 1;
                _this.$('.componentContainer').each(function() {
                    //使用silent，以避免激发change事件
                    $(this).data('component').model.set({index: index++}, {silent: true});
                });

                _this.$form.parent().scrollTop(100000);
            }
        }
        this.$('.formPage').droppable(dropOptions);

        this.addMetaInfoComponent();
        this.addListInfoComponent();
    },

    /***********************************************************
     * enableComponentSortable: 设置component为可拖动排序
     ***********************************************************/
    enableComponentSortable: function() {
        this.$form.sortable({
            axis: 'y',
            placeholder: "ui-state-highlight",
            stop: _.bind(function() {
                //更新所有component的index
                var index = 1;
                this.$('.componentContainer').each(function() {
                    //使用silent，以避免激发change事件
                    $(this).data('component').model.set({index: index++}, {silent: true});
                });
            }, this)
        });
    },

    /***********************************************************
     * addMetaInfoComponent: 创建metainfo组件
     ***********************************************************/
    addMetaInfoComponent: function() {
        var component = W.getComponent('page_metainfo');
        component.model.set({pageType: 'form_page'}, {silent: true});

        var node = $('<div class="componentMetaInfoContainer xui-oneComponent">');
        node.data('component', component);
        node.append($.tmpl(component.template, {}));
        this.$form.append(node);
    },

    /***********************************************************
     * addListInfoComponent: 创建listinfo组件
     ***********************************************************/
    addListInfoComponent: function() {
        var component = W.getComponent('list_info');

        var node = $('<div class="componentListInfoContainer xui-oneComponent">');
        node.data('component', component);
        node.append($.tmpl(component.template, {}));
        this.$form.append(node);

        this.$(".formPage_cover_contentContainer thead tr").css({cursor:'move'});
        this.$(".formPage_cover_contentContainer thead tr").sortable({
            axis: 'x',
            stop: _.bind(function(options) {
                //alert('stop now');
            }, this)
        }).disableSelection();
    },

    /***********************************************************
     * selectMetaInfo: 选中meta info component
     ***********************************************************/
    selectMetaInfoComponent: function() {
        this.$('.componentMetaInfoContainer').eq(0).click();
    },

    /***********************************************************
     * getComponents: 获取页面中的组件集合
     ***********************************************************/
    getComponents: function() {
        var components = [];
        this.$('.xui-oneComponent').each(function() {
            components.push($(this).data('component'));
        });

        return components;
    },

    /***********************************************************
     * getPageContent: 获得page内容
     ***********************************************************/
    getPageContent: function() {
        this.$el.data('page', this);
        return this.$el;
    },

    /*********************************************************
     * onSwitchPage: 切换页面时，清空选中的component
     *********************************************************/    
    onSwitchPage: function(component) {
        this.activeComponentNode = null;
        this.$('.componentOverlay-active').removeClass('componentOverlay-active');
    },

    /***************************************************************
     * onClickComponent：点击component区域的响应函数
     ***************************************************************/
    onClickComponent: function(event) {
        var $componentOverlay = $(event.currentTarget);
        if ($componentOverlay.hasClass('componentOverlay-active')) {
            return;
        }

        this.$('.componentOverlay-active').removeClass('componentOverlay-active');
        $componentOverlay.removeClass('componentOverlay-hover').addClass('componentOverlay-active');

        this.activeComponentNode = $componentOverlay.parent();
        var component = $componentOverlay.parent().data('component');
        W.Broadcaster.trigger('component:select', component);
    },

    /***************************************************************
     * onClickPageMetaInfo: 点击page metainfo区域的响应函数
     ***************************************************************/
    onClickPageMetaInfo: function(event) {
        var $metainfo = $(event.currentTarget);
        if ($metainfo.hasClass('componentOverlay-active')) {
            xlog('return directly');
            return;
        }

        $('.componentOverlay-active').removeClass('componentOverlay-active');
        $metainfo.removeClass('componentOverlay-hover').addClass('componentOverlay-active');

        //设置columns的source为component集合
        var component = $metainfo.data('component');
        var source = [];
        _.each(this.getComponents(), function(component) {
            if (component.type == 'metainfo' || component.type == 'listinfo') {
                return;
            }

            source.push({
                value: component.model.get('name'),
                name: component.model.get('label')
            })
        });
        xlog(source);
        component.name2field['searchField'].source = source;

        this.activeComponentNode = $metainfo.parent();
        var component = $metainfo.data('component');
        W.Broadcaster.trigger('component:select', component);
    },

    /***************************************************************
     * onClickCloseCoverBtn: 点击form cover的关闭按钮的响应函数
     ***************************************************************/
    onClickCloseCoverBtn: function(event) {
        this.$('.formPage_cover').hide();

        var listInfoComponent = this.activeComponentNode.data('component');
        var listColumnInfos = listInfoComponent.model.get('columns');

        //更新header的index
        var index = 1;
        this.$('.formPage_cover th').each(function() {
            var $th = $(this);
            var name = $th.data('component-name');
            listColumnInfos[name].index = index++;
        });

        //选择meta info component
        this.selectMetaInfoComponent();
    },

    /***************************************************************
     * onClickRemoveComponentBtn: 点击删除component组件按钮的响应函数
     ***************************************************************/
    onClickRemoveComponentBtn: function(event) {
        var $componentNode = $(event.currentTarget).parents('.xui-oneComponent').eq(0);
        delete $componentNode.data('component');
        $componentNode.remove();

        //选择meta info component
        this.selectMetaInfoComponent();

        event.stopPropagation();
        event.preventDefault();
    },

    /***************************************************************
     * updateListHeaderPreview: 更新列表header的预览
     ***************************************************************/
    updateListHeaderPreview: function(listInfoComponent, columnComponents) {
        var columnInfos = listInfoComponent.model.get('columns');

        var node = $('<div>');
        columnComponents = _.sortBy(columnComponents, function(component) {
            var name = component.model.get('name');
            return columnInfos[name].index;
        });

        _.each(columnComponents, function(component) {
            if (!columnInfos[component.model.get('name')].select) {
                return;
            }

            var thNode = $('<th>' + component.model.get('label') + '</th>');
            thNode.data('component-name', component.model.get('name'));
            node.append(thNode);
        });

        this.$('.formPage_cover_contentContainer thead tr').empty().append(node.children());
    },

    /***************************************************************
     * updateColumnInfos: 更新list中的column信息
     ***************************************************************/
    updateColumnInfos: function(component) {
        var oldColumnInfos = component.model.get('columns') || {};
        var columnInfos = {};
        var index = 1;
        _.each(component.name2field['columns'].source, function(columnComponent) {
            var columnName = columnComponent.model.get('name');
            var isSelect = oldColumnInfos[columnName] ? oldColumnInfos[columnName].select : true
            columnInfos[columnName] = {select: isSelect, index: index++};
            columnComponent.isSelectIntoList = columnInfos[columnName].select;
            // if (oldColumnInfos[columnName]) {
            //     columnInfos[columnName].select = oldColumnInfos[columnName].select;
            //     columnComponent.model.set('index', index++);
            //     columnComponent.isSelectIntoList = columnInfos[columnName].select;
            // } else {
            //     columnInfos[columnName] = {select: true, index: index++};
            //     columnComponent.isSelectIntoList = true;
            // }
        });

        component.model.set({columns: columnInfos}, {silent: true});
    },

    /***************************************************************
     * onClickPageListInfo: 点击page listinfo区域的响应函数
     ***************************************************************/
    onClickPageListInfo: function(event) {
        var $listinfo = $(event.currentTarget);
        if ($listinfo.hasClass('componentOverlay-active')) {
            xlog('return directly');
            return;
        }

        $('.componentOverlay-active').removeClass('componentOverlay-active');
        $listinfo.removeClass('componentOverlay-hover').addClass('componentOverlay-active');

        this.activeComponentNode = $listinfo;
        var component = $listinfo.data('component');
        //设置columns的source为component集合
        component.name2field['columns'].source = _.filter(this.getComponents(), function(component) {
            if (component.type == 'metainfo' || component.type == 'listinfo') {
                return false;
            } else {
                return true;
            }
        });

        this.updateColumnInfos(component);
        /*
        if (!component.model.get('columns')) {
            //初始化columns field
            var columnInfos = {}
            var index = 1;
            _.each(component.name2field['columns'].source, function(columnComponent) {
                columnInfos[columnComponent.model.get('name')] = {select: true, index: index++};
                columnComponent.isSelectIntoList = true;
            });
            component.model.set({columns: columnInfos}, {silent: true});
        } else {
            //根据list info中的信息更新各个component的isSelectIntoList属性
            columnInfos = component.model.get('columns');
            _.each(component.name2field['columns'].source, function(columnComponent) {
                var columnName = columnComponent.model.get('name');
                if (columnInfos[columnName]) {
                    columnComponent.isSelectIntoList = columnInfos[columnComponent.model.get('name')].select;
                } else {
                    columnInfos[columnComponent.model.get('name')] = {select: true, index: index++};
                    columnComponent.isSelectIntoList = true;
                }
            });
        }
        */

        W.Broadcaster.trigger('component:select', component);

        this.updateListHeaderPreview(component, component.name2field['columns'].source);
        this.$('.formPage_cover').show();

        component.model.on('change', function() {
            this.updateListHeaderPreview(component, component.name2field['columns'].source);
        }, this);
    },    

    /***************************************************************
     * onMouseEnterComponent：鼠标移进component区域的响应函数
     ***************************************************************/
    onMouseEnterComponent: function(event) {
        $(event.currentTarget).addClass('componentOverlay-hover');
    },

    /***************************************************************
     * onMouseLeaveComponent：鼠标移出component区域的响应函数
     ***************************************************************/
    onMouseLeaveComponent: function(event) {
        $(event.currentTarget).removeClass('componentOverlay-hover');
    },
});