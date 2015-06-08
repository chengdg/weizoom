/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 活动编辑页面中，用户输入项的列表
 * @constructor
 */
ensureNS('W.view.marketTools');
W.view.marketTools.Shake = Backbone.View.extend({	
	events: {
        'click .tx_addPrizeItem': 'onClickAddPrizeItem',
	},

	getTemplate: function() {
		$('#markettool-shake-prize-tmpl-src').template('markettool-shake-prize-tmpl');
		return 'markettool-shake-prize-tmpl';
	},
	
	initialize: function(options) {
        this.$el = $(this.el);
        this.template = this.getTemplate();
        this.itemClassName = '.tx_prizeItem';
	},

	/**
	 * addTextItem: 添加text item
	 */
	onClickAddPrizeItem: function(event) {
		//item = item || {id: this.idCounter++, can_edit: true};
        //this.$tbody.append($.tmpl(this.textItemTemplate, item));
        var $el = $(event.currentTarget);
      
     
        //var $newItem = this.$prizeItem.clone();
        this.$prizeItem = this.$(this.itemClassName+':last');
        console.log()
        var id = parseInt(this.$prizeItem.attr('data-id')) + 1

        this.$el.append(($.tmpl(this.template, {
            id:id
        })));
        this.loadDate();
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
        	id: 1
        }));

        this.loadDate();

        
    },

    loadDate: function() {
         $('input[data-ui-role="shakeDatepicker"]').each(function() {
            var _this = this;
            var $datepicker = $(_this);
            console.log()
            var format = $datepicker.attr('data-format');
            var min = $datepicker.attr('data-min');
            var max = $datepicker.attr('data-max');
            var $min_el = $($datepicker.attr('data-min-el'));
            var $max_el = $($datepicker.attr('data-max-el'));
            var options = {};
            options = {
                buttonText: '选择日期',
                currentText: '当前时间',
                hourText: "小时",
                controlType: 'select',
                oneLine: true,
                minuteText: "分钟",
                numberOfMonths: 1,
                dateFormat: 'yy-mm-dd',
                //dateFormat: format,
                closeText: '关闭',
                prevText: '&#x3c;上月',
                nextText: '下月&#x3e;',
                monthNames: ['一月','二月','三月','四月','五月','六月',
                    '七月','八月','九月','十月','十一月','十二月'],
                monthNamesShort: ['一','二','三','四','五','六',
                    '七','八','九','十','十一','十二'],
                dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
                dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
                dayNamesMin: ['日','一','二','三','四','五','六'],
                beforeShow: function(e) {
                    if(min === 'now') {
                        $(_this).datetimepicker('option', 'minDate', new Date());
                    }else if(min){
                        $(_this).datetimepicker('option', 'minDate', min);
                    }

                    if($min_el){
                        var startTime = $min_el.val();
                        if(startTime) {
                            $(_this).datetimepicker('option', 'minDate', startTime);
                            $(_this).datetimepicker('option', 'minDateTime', new Date(startTime));
                        }
                    }

                    if(max === 'now') {
                        $(_this).datetimepicker('option', 'maxDate', new Date());
                    }else if(max){
                        $(_this).datetimepicker('option', 'maxDate', max);
                    }

                    if($max_el){
                        var endTime = $max_el.val();
                        if(endTime) {
                            $(_this).datetimepicker('option', 'maxDate', endTime);
                        }
                    }
                },
                onClose: function() {
                }
            };

            $datepicker.datetimepicker(options);
            //cc.beforeShow();
        });

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

