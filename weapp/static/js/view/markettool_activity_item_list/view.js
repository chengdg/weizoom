/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 活动编辑页面中，用户输入项的列表
 * @constructor
 */
ensureNS('W.view.markettool');
W.view.markettool.ActivityItemListView = Backbone.View.extend({	
	events: {
		'click .tx_delete_option': 'deleteItem',
        'click .tx_add_text': 'onClickAddTextItemButton',
        'click .tx_add_radio': 'onClickAddRadioItemButton',
        'click .tx_add_image': 'onClickAddImageItemButton',
        'click .tx_add_checkbox': 'onClickAddCheckboxItemButton',
	},

	getTemplate: function() {
		$('#markettool-activity-item-list-tmpl-src').template('markettool-activity-item-list-tmpl');
		return 'markettool-activity-item-list-tmpl';
	},

	getTextItemTemplate: function() {
		$('#markettool-activity-item-text-tmpl-src').template('markettool-activity-item-text-tmpl');
		return 'markettool-activity-item-text-tmpl';
	},

	getRadioItemTemplate: function() {
		$('#markettool-activity-item-radio-tmpl-src').template('markettool-activity-item-radio-tmpl');
		return 'markettool-activity-item-radio-tmpl';
	},

	getImageItemTemplate: function() {
		$('#markettool-activity-item-image-tmpl-src').template('markettool-activity-item-image-tmpl');
		return 'markettool-activity-item-image-tmpl';
	},

    getCheckboxItemTemplate: function() {
        $('#markettool-activity-item-checkbox-tmpl-src').template('markettool-activity-item-checkbox-tmpl');
        return 'markettool-activity-item-checkbox-tmpl';
    },
	
	initialize: function(options) {
		this.$el = $(this.el);
		this.textItemTemplate = this.getTextItemTemplate();
        this.radioItemTemplate = this.getRadioItemTemplate();
		this.checkboxItemTemplate = this.getCheckboxItemTemplate();
		this.imageItemTemplate = this.getImageItemTemplate();
		this.template = this.getTemplate();
        //使用ignoreEmptyItems兼容以前无items时自动显示“姓名”，“手机号”输入项的行为
        this.ignoreEmptyItems = false;
        if (options.hasOwnProperty('ignoreEmptyItems')) {
            this.ignoreEmptyItems = options.ignoreEmptyItems;
        }

		this.$tbody = null;
		this.idCounter = 99999;
		this.canEdit = options.hasOwnProperty('canEdit') ? options.canEdit : true;

		this.items = options.items || [];
	},

	/**
	 * addTextItem: 添加text item
	 */
	addTextItem: function(item) {
		item = item || {id: this.idCounter++, can_edit: true};
        this.$tbody.append($.tmpl(this.textItemTemplate, item));
    },

    /**
	 * onClickAddTextItemButton: 点击“+输入框”按钮的响应函数
	 */
    onClickAddTextItemButton: function(event) {
    	this.addTextItem();
    },

    /**
	 * addRadioItem: 添加radio item
	 */
    addRadioItem: function(item) {
    	item = item || {id: this.idCounter++, can_edit: true};
        this.$tbody.append($.tmpl(this.radioItemTemplate, item));
    },

    /**
	 * onClickAddRadioItemButton: 点击“+单选框”按钮的响应函数
	 */
    onClickAddRadioItemButton: function(event) {
    	this.addRadioItem();
    },

    /**
     * addCheckboxItem: 添加checkbox item
     */
    addCheckboxItem: function(item) {
        item = item || {id: this.idCounter++, can_edit: true};
        this.$tbody.append($.tmpl(this.checkboxItemTemplate, item));
    },

    /**
     * onClickAddCheckboxItemButton: 点击“+多选框”按钮的响应函数
     */
    onClickAddCheckboxItemButton: function(event) {
        this.addCheckboxItem();
    },

    /**
	 * addImageItem: 添加image item
	 */
    addImageItem: function(item) {
    	item = item || {id: this.idCounter++, can_edit: true};
        this.$tbody.append($.tmpl(this.imageItemTemplate, item));
    }, 

    /**
	 * onClickAddImageItemButton: 点击“+上传图片”按钮的响应函数
	 */
    onClickAddImageItemButton: function(event) {
    	this.addImageItem();
    },

    /**
	 * deleteItem: 点击“删除”按钮的响应函数
	 */
    deleteItem: function(event) {
    	event.stopPropagation();
    	event.preventDefault();
    	var $link = $(event.target);
    	W.view.fn.requreConfirm({
            $el: $link,
            confirm: function() {
            	W.view.fn.finishConfirm();
            	$link.parents('tr').remove();
            }
        });        
    },

    /**
     * __initData: 初始化数据
     */
    __initData: function(items) {
        if (this.items.length == 0) {
            //初始时，默认添加“姓名”和“手机号”
            if (!this.ignoreEmptyItems) {
                this.addTextItem({
                    id: this.idCounter++,
                    title: '姓名',
                    is_mandatory: false
                });
                this.addTextItem({
                    id: this.idCounter++,
                    title: '手机号',
                    is_mandatory: false
                });
            }
        } else {
            _.each(this.items, function(item) {
                item.can_edit = this.canEdit;
                item.id = this.idCounter++;
                if ((item.type === 'text') || (item.type === 'input')) {
                    this.addTextItem(item);
                } else if ((item.type === 'select') || (item.type === 'radio')) {
                    this.addRadioItem(item);
                } else if (item.type === 'image') {
                    this.addImageItem(item);
                } else if (item.type === 'checkbox') {
                    this.addCheckboxItem(item);
                }
            }, this);
        }
    },

    render: function(data) {
        this.$el.append($.tmpl(this.template, {
        	canEdit: this.canEdit
        }));

        this.$tbody = this.$('tbody');

        this.__initData();
    },

    getViewData: function() {
        var id2data = {};
        this.$el.find('tbody tr').each(function() {
            var $tr = $(this);
            var $inputs = $tr.find('[name]');
            for (var i = 0; i < $inputs.length; ++i) {
                var $input = $inputs.eq(i);
                var inputName = $input.attr('name');
                var items = inputName.split('_');
                var type = items[1];
                var name = items[2];
                var id = parseInt(items[3]);
                if (name === 'mandatory') {
                    //mandatory选择框
                    var value = $input.is(":checked");
                } else {
                    var value = $input.val();
                }

                if (!id2data.hasOwnProperty(id)) {
                    id2data[id] = {'type': type, 'id': id};
                }
                if (name === 'mandatory') {
                    name = 'is_mandatory'
                } else if (name === 'data') {
                    name = 'initial_data';
                }
                id2data[id][name] = value;
            }
        });

        return _.values(id2data);
    },

    setViewData: function(data) {
        this.items = data;
        this.__initData();
    }
});

W.registerUIRole('div[data-ui-role="user-input-controls"]', function() {
    var $div = $(this);

    var initData = $div.attr('data-init-data');

    if (initData) {
        initData = $.parseJSON(initData);
    }

    var view = new W.view.markettool.ActivityItemListView({
        el: $div[0],
        canEdit: true,
        items: initData,
        ignoreEmptyItems: true
    });
    view.render();

    $div.data('view', view);
});