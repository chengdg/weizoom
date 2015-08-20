/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * 右侧的property视图
 * @class
 */
ensureNS('W.workbench');
W.workbench.PageSynchronizer = Backbone.View.extend({
	el: '',

	events: {
	},
	
	initialize: function(options) {
        this.pageJson = null;
        this.currentPage = null;
        W.Broadcaster.on('component:select', this.onSelectPage, this);

        this.underManualSync = false;
	},

    render: function() {
        /*
        this.$el.append($.tmpl(this.template, {}));
        */
    },

    /**
     * run: 启动同步器
     */
    run: function() {
        //var task = new W.DelayedTask(this.synchronize, this);
        //task.delay(5000);
    },

    manualSync: function(callback) {
        var sup = this;
        sup.synchronize({
            manual: true,
            callback: callback,
            image: ''
        });
//        W.Broadcaster.trigger('designpage:screenshot', function(dataUrl) {
//            var image = dataUrl;
//            image = image.replace(/^data:image\/(png|jpg);base64,/, "");
//            sup.synchronize({
//                manual: true,
//                callback: callback,
//                image: image
//            });
//            //task.delay(500);
//        });
    },

    /**
     * synchronize: 同步数据
     */
    synchronize: function(options) {
        //验证
        if (!W.isSystemManager) {
            if(!this.currentPage.validate()) {
                return;
            }
        }

        var isManualSync = !!(options && options.manual)
        if (isManualSync) {
            //手工sync，设置manualSync标识
            this.underManualSync = true;
        }

        if (!isManualSync && this.underManualSync) {
            //定时sync任务，上一次有手工sync，则该次跳过
            this.underManualSync = false;
            var task = new W.DelayedTask(this.synchronize, this);
            task.delay(5000);
            return;
        }

        xlog('currentPage: ', this.currentPage);
        if (this.currentPage) {
            var json = JSON.stringify(this.currentPage.toJSON());
            W.Broadcaster.trigger('page_synchronizer:synchronizing');
            var _this = this;
            //if (json != this.pageJson) {
            if (true) {
                xlog('call project/update api');
                this.pageJson = json;
                W.getApi().call({
                    app: 'termite2',
                    api: 'project',
                    method: 'post',
                    args: {
                        field: 'page_content',
                        page_json: json,
                        page_id: this.currentPage.cid,
                        id: W.projectId
                    },
                    success: function(data) {
                        xlog('[synchronizer]: synchronize success!!');
                        if (_this.currentPage.isNewCreated) {
                            //消除创建标识
                            _this.currentPage.isNewCreated = false;
                        }
                        W.Broadcaster.trigger('page_synchronizer:success');
                        if (isManualSync) {
                            if (options.callback) {
                                options.callback(data);
                            }
                        } else {
                            var task = new W.DelayedTask(_this.synchronize, _this);
                            task.delay(5000);
                        }
                    },
                    error: function(resp) {
                        alert('同步失败!');
                        if (isManualSync) {
                        } else {
                            var task = new W.DelayedTask(_this.synchronize, _this);
                            task.delay(5000);
                        }
                    }
                })
                xlog('[synchronizer]: dirty page, synchronize it!');
            } else {
                W.Broadcaster.trigger('page_synchronizer:success');
                if (isManualSync) {
                } else {
                    var task = new W.DelayedTask(this.synchronize, this);
                    task.delay(5000);
                }
            }
        } else {
            if (isManualSync) {
            } else {
                var task = new W.DelayedTask(this.synchronize, this);
                task.delay(5000);
            }
        }
    },

    /**
     * onSelectPage: 切换page的响应函数
     */
    onSelectPage: function(component) {
        if (component.isRootPage()) {
            xlog('[synchronizer]: change page');
            this.pageJson = null;//JSON.stringify(component.toJSON());
            this.currentPage = component;
        }
    }
    
});