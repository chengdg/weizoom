/*
Copyright (c) 2011-2012 Weizoom Inc
*/

ensureNS('W.view.common');
W.view.common.ViperComponentGroupView = Backbone.View.extend({
    el: '',

    events: {
        'click .xa-componentGroup-add': 'onClickAddGroupButton',
        'click .xa-componentGroup-delete': 'onClickDeleteGroupButton'
    },

    getTemplate: function() {
    },

    isInitialized: false,

    initialize: function(options) {
        this.$el = $(this.el);

        this.groupName = options.groupName || '';
        this.maxComponentGroupCount = options.maxComponentGroupCount;
        this.groupCount = this.$('.xui-inner-group .xui-inner-components').length;

        this.inputNameTemplate = _.template('__viperCG:<%=groupName%>:<%=index%>:<%=inputName%>');
        this.hiddenInputTemplate = _.template("<input type='hidden' name='<%=name%>' value='<%=value%>' />");

        this.validInputElements = {
            "input":true,
            "select":true,
            "textarea":true
        }
    },

    render: function() {
        this.$('.xui-componentGroup .xui-inner-componentsTemplate [name]').each(function() {
            var $el = $(this);
            $el.attr('data-name', $el.attr('name'));
            $el.removeAttr('name');
        });

        //去除template中的data-cid
        this.$('.xui-componentGroup .xui-inner-componentsTemplate [data-cid]').each(function() {
            $(this).removeAttr('data-cid');
        });

        if (this.groupCount == 0) {
            this.__addOneGroup();
        } else {
            this.__initInputElement();
        }

        this.$componentsList = this.$('.xui-inner-group .xui-inner-components');
        setInterval(_.bind(this.__changeInputName, this), 1000);
    },

    /**
     * __isValidInputElement: 判断是否是valid input element
     */
    __isValidInputElement: function(tagName) {
        return this.validInputElements[tagName];
    },

    /**
     * __changeInputName: 监控并改变input name
     */
    __changeInputName: function(tagName) {
        if (this.changeInputNameCounter > 0) {
            xwarn('change input name...')
            this.changeInputNameCounter -= 1;
            for (var i = 0; i < this.$componentsList.length; ++i) {
                var $components = this.$componentsList.eq(i);
                var index = $components.attr('data-components-index');
                var $inputs = $components.find('[name]');
                for (var j = 0; j < $inputs.length; ++j) {
                    var $input = $inputs.eq(j);
                    var tagName = $input.get(0).tagName.toLowerCase();
                    if (!this.__isValidInputElement(tagName)) {
                        continue;
                    }

                    var originalName = $input.attr('name');
                    if (originalName.indexOf('__viperCG:') != -1) {
                        continue;
                    }

                    var newName = this.inputNameTemplate({
                        groupName: this.groupName,
                        index: index,
                        inputName: originalName
                    });
                    xwarn('change ' + originalName + ' to ' + newName);
                    $input.attr('name', newName);
                }
            }
        } else {
            xwarn('no need to change input name!');
        }
    },

    /**
     * __checkInputType: 检查input的类型
     */
    __checkInputType: function($input) {
        var dom = $input.get(0);
        var type = $input.attr('type');
        var tagName = dom.tagName.toLowerCase();
        if (tagName === 'input' && (type === 'radio' || type === 'checkbox')) {
            return {
                "type": type,
                "shouldSetValue": false,
                "shouldCheckInput": true
            }
        } else {
            return {
                type: type,
                "shouldSetValue": true,
                "shouldCheckInput": false
            }
        }
    },

    /**
     * __initInputElement: 初始化input控件，1. 获取value；2. 改造name
     */
    __initInputElement: function() {
        var record = W.loadJSON('record');
        if (!record) {
            //prevent init input in design mode
            return;
        }

        //初始化input数据
        var inputsShouldCheck = {}
        var _this = this;
        var $componentsList = this.$('.xui-inner-group .xui-inner-components');
        for (var i = 0; i < $componentsList.length; ++i) {
            var $components = $componentsList.eq(i);
            var index = $components.attr('data-components-index');
            var $inputs = $components.find('[name]');
            for (var j = 0; j < $inputs.length; ++j) {
                var $input = $inputs.eq(j);
                var tagName = $input.get(0).tagName.toLowerCase();
                if (!_this.__isValidInputElement(tagName)) {
                    continue;
                }

                var originalName = $input.attr('name');
                var newName = _this.inputNameTemplate({
                    groupName: _this.groupName,
                    index: index,
                    inputName: originalName
                });
                
                $input.attr('name', newName);

                var value = record[newName];
                var inputInfo = _this.__checkInputType($input);
                if (inputInfo.shouldSetValue) { 
                    $input.val(record[newName]);
                }
                if (inputInfo.shouldCheckInput) {
                    if (value === $input.val()) {
                        $input.attr('checked', 'checked');
                    }
                }

                if ($input.attr('data-should-set-data')) {
                    $input.data('view').setViewData(record[newName]);
                }
            }
        }

        //初始化view数据
        this.$('[data-should-set-data]').each(function() {
            var $view = $(this);
            var view = $view.data('view');
            if (!view) {
                return;
            }
            
            var originalName = $view.attr('data-component-name');
            if (!originalName) {
                return;
            }

            if (originalName.indexOf('__viperCG:') !== -1) {
                //这种类型的元素在上一步已被处理
                return;
            }

            var $components = $view.parents('.xui-inner-components').eq(0);
            var index = $components.attr('data-components-index');
            var name = _this.inputNameTemplate({
                    groupName: _this.groupName,
                    index: index,
                    inputName: originalName
            });

            view.setViewData(record[name]);
        });
    },

    /**
     * __addOneGroup: 添加一个group
     */
    __addOneGroup: function() {
        if (this.maxComponentGroupCount !== 0 && this.groupCount >= this.maxComponentGroupCount) {
            //确保最大component group count限制
            W.getErrorHintView().show('最多添加'+ this.maxComponentGroupCount + '个');
            return;
        }

        var $node = $(this.$('#xui-inner-componentsTemplate').html());

        //改变group中input的name
        this.groupCount += 1;
        var _this = this;
        $node.attr('data-components-index', this.groupCount);
        $node.find('[data-name]').each(function() {
            var $input = $(this);
            var tagName = $input.get(0).tagName.toLowerCase();
            if (!_this.__isValidInputElement(tagName)) {
                return;
            }

            var name = _this.inputNameTemplate({
                groupName: _this.groupName,
                index: _this.groupCount,
                inputName: $input.attr('data-name')
            });
            $input.attr('name', name);
        });

        
        this.$('.xui-inner-group').append($node);
        W.createWidgets($node);
        this.changeInputNameCounter = 2;
        $node.find('input').eq(0).focus();

        this.$componentsList = this.$('.xui-inner-group .xui-inner-components');
    },

    /**
     * refreshOrder: 更新显示顺序信息
     */
    refreshOrder: function() {
        var $componentsList = this.$('.xui-inner-group .xui-inner-components');
        var _this = this;
        for (var i = 0; i < $componentsList.length; ++i) {
            var $components = $componentsList.eq(i);
            $components.find('[name]').each(function() {
                var $input = $(this);
                var originalName = $input.attr('name');
                var items = originalName.split(':');
                originalName = items[items.length-1];
                var newName = _this.inputNameTemplate({
                    groupName: _this.groupName,
                    index: i+1,
                    inputName: originalName
                });
                $input.attr('name', newName);
            });
        }

        this.groupCount = $componentsList.length;
    },

    /**
     * onClickAddGroupButton: 点击添加按钮的响应函数
     */
    onClickAddGroupButton: function(event) {
        this.__addOneGroup();
    },

    /**
     * onClickDeleteGroupButton: 点击删除按钮的响应函数
     */
    onClickDeleteGroupButton: function(event) {
        var $button = $(event.currentTarget);
        $button.parents('.xui-inner-components').remove();

        this.refreshOrder();
    },

    /**
     * collectEmbededViewData: 收集embeded view的数据
     */
    collectEmbededViewData: function() {
        var _this = this;
        this.$('[data-should-extract-data]').each(function() {
            var $view = $(this);
            if (!$view.is(":visible")) {
                return;
            }

            var view = $view.data('view');
            var data = view.getViewData();

            var originalName = $view.attr('data-component-name');
            var $components = $view.parents('.xui-inner-components').eq(0);
            var index = $components.attr('data-components-index');
            var name = _this.inputNameTemplate({
                    groupName: _this.groupName,
                    index: index,
                    inputName: originalName
            });
            
            _this.$el.append(_this.hiddenInputTemplate({
                name: name,
                value: data
            }))
        });
    }
});


W.registerUIRole('[data-ui-role="viper-component-group"]', function() {
    var $componentGroup = $(this);
    var maxComponentGroupCount = parseInt($componentGroup.attr('data-max-component-group-count') || 0);
    var groupName = $componentGroup.attr('data-group-name');
    var view = new W.view.common.ViperComponentGroupView({
        el: $componentGroup.get(),
        groupName: groupName,
        maxComponentGroupCount: maxComponentGroupCount
    });
    view.render();

    $componentGroup.data('view', view);
});