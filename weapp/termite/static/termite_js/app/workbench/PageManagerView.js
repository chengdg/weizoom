/*
Copyright (c) 2011-2012 Weizoom Inc
*/
/**
 * page manager
 * @class
 */
W.workbench.PageManagerView = Backbone.View.extend({
	el: '',

	events: {
		'click [data-action="addPage"]': 'onClickAddPage',
		'click [data-action="duplicatePage"]': 'onClickCopyPage',
		'click [data-action="makeTemplate"]': 'onClickMakeTemplate',
		'click [data-action="removePage"]': 'onClickRemovePage',
		'click [data-action="selectTemplate"]': 'onClickSelectTemplate',
		'click [data-action="exportProject"]': 'onClickExportProject',
		'click [data-action="importProject"]': 'onClickImportProject',
		'click li.page': 'onClickPage',
		'click #submitPageBtn': 'onClickSubmitPage',
		'click #submitTemplateBtn': 'onClickSubmitTemplate',
		'click #updateTemplateBtn': 'onClickUpdateTemplate',
		'change #addPageDialog select': 'onChangePageTemplate',
		'keyup input[name="pageName"]': 'onKeyup'
	},

	getTemplate: function() {
		$('#page-manager-tmpl-src').template('page-manager-tmpl');
		return "page-manager-tmpl";
	},

	initialize: function(options) {
		this.template = this.getTemplate();
		this.isSystemManager = true;
		if (options.hasOwnProperty('isSystemManager')) {
			this.isSystemManager = options.isSystemManager;
		}
		this.el = $.tmpl(this.template, {
			isSystemManager: this.isSystemManager
		})[0];
		this.$el = $(this.el);

		$(options.el).append(this.$el);

		this.pages = [];
		this.$pageContainer = this.$('.pageManager_pageList');
		this.currentActivePage = null;
		this.id2pageTemplate = {};

		this.enableSortFunction();

		W.Broadcaster.on('component:create', this.onCreateComponent, this);
		W.Broadcaster.on('mobilepage:sort_widget', this.onSortWidget, this);
		W.Broadcaster.on('mobilepage:drag_widget', this.onDragWidget, this);
		W.Broadcaster.on('designpage:finish_init', this.onFinishInitDesignPage, this);
		W.Broadcaster.on('designpage:wait_for_page', this.onWaitForPage, this);
		W.Broadcaster.on('designpage:select_page_component', this.onSelectPageComponentInDesignPage, this);

		W.data.pageManager = this;

		//this.startGetPageTemplatesTask();
	},

	render: function() {
		return;
	},

	/**
	 * getPages: 获得page集合
	 */
	getPages: function() {
		return this.pages;
	},

	getPageByCid: function(cid) {
		cid = parseInt(cid);
		return _.findWhere(this.pages, {
			cid: cid
		});
	},

	/**
	 * getCurrentActivePage: 获得当前选中的page
	 */
	getCurrentActivePage: function() {
		return this.currentActivePage;
	},

	/***********************************************************
	 * enableSortFunction: 开启拖动排序
	 ***********************************************************/
	enableSortFunction: function() {
		this.$pageContainer.sortable({
			axis: 'y',
			/*placeholder: "ui-state-highlight",*/
			stop: _.bind(function() {
				//更新所有page的index
				var ids = [];
				this.$('.page').each(function() {
					$page = $(this);
					ids.push($page.data('component').cid);
				});

				//调用api，后台删除
				W.getApi().call({
					app: 'workbench',
					api: 'page_index/update',
					method: 'post',
					args: {
						project_id: W.projectId,
						ordered_pages: ids.join(',')
					},
					success: function(data) {

					},
					error: function(resp) {
						alert('调整Page顺序失败');
					}
				})
			}, this)
		});
	},

	/***********************************************************
	 * activePage: 设置page为当前活动page
	 ***********************************************************/
	activePage: function($page) {
		this.$('li.selected').removeClass('selected');
		this.$('.icon-white').removeClass('icon-white');

		$page.addClass('selected').find('i').addClass('icon-white');

		var pageComponent = $page.data('component');;
		this.currentActivePage = pageComponent;

		xlog('trigger component:select');
		W.workbench.PageManagerView.currentActivePage = pageComponent;
		W.Broadcaster.trigger('component:select', pageComponent);
	},

	/***********************************************************
	 * addPage: 添加一个Page
	 ***********************************************************/
	addPage: function(title, page, options) {
		options = options || {};

		if (!page) {
			var PageComponentConstructor = W.component.getComponentConstructorByType(W.projectType + ".page");
			page = new PageComponentConstructor({
				model: {
					title: title
				}
			});
		}
		this.pages.push(page);

		var pageHtml = '' +
			'<li class="page">' +
			'<a href="#"><i class="icon-file mr5"></i><span class="pageTitle">' + title + '</span></a>' +
			'<div class="fr">' +
			'<i class="icon-align-justify"></i>' +
			'</div>' +
			'</li>';
		var $node = $(pageHtml);
		$node.data('view', this);
		$node.data('component', page);
		page.dom = $node;
		page.on('component:change_property', function(component, model) {
			_.each(model.changed, function(value, name) {
				if (name === 'title') {
					//更新页面名
					page.dom.find('.pageTitle').text(value);
				}
			});
		});

		this.$pageContainer.append($node);

		//立刻保存新创建的page
		W.Synchronizer.onSelectPage(page);
		var syncCallback = _.bind(function() {
			if (!options.silent) {
				this.activePage(page.dom);
				W.Broadcaster.trigger('pagemanager:addpage', page);
			}
		}, this);
		W.Synchronizer.manualSync(syncCallback);
	},

	/***********************************************************
	 * onCreateComponent: component:create事件的响应函数
	 ***********************************************************/
	onCreateComponent: function(component) {
		if (this.currentActivePage) {
			var layout = W.util.getInsertIndicatorLayoutInMobilePage();

			var $mobilePage = layout.$mobilePage;
			var itemUid = component.cid + '';
			var targetContainerUid = layout.pid;
			xlog('[page manager]: insert ' + itemUid + '(' + (typeof itemUid) + ')' + ' to ' + targetContainerUid + '(' + (typeof targetContainerUid) + ')');
			var component = W.component.getComponent(itemUid);
			var targetComponent = W.component.getComponent(targetContainerUid);
			targetComponent.addComponent(component);

			//替换orderedCids中的'insert'占位符为component的cid，并排序
			var orderedCids = layout.orderedCids;
			var count = orderedCids.length;
			for (var i = 0; i < count; ++i) {
				if (orderedCids[i] === 'insert') {
					orderedCids[i] = itemUid;
				}
			}
			this.onSortWidget(orderedCids);

			W.Broadcaster.trigger('component:finish_create', this.currentActivePage, component);

			/*
            if (this.currentActivePage) {
                this.currentActivePage.addComponent(component);
                this.currentActivePage.dump();
                xlog('trigger finish_create');
                W.Broadcaster.trigger('component:finish_create', this.currentActivePage, component);
            }
            */
		}
	},

	/***********************************************************
	 * onSortWidget: mobilepage:sort_widget事件响应函数
	 ***********************************************************/
	onSortWidget: function(orderedCids) {
		xlog('in onSortWidget...');
		var index = 1;
		_.each(orderedCids, function(cid) {
			W.component.getComponent(cid).model.set('index', index++, {
				silent: true
			});
		})
	},

	/***********************************************************
	 * onDragWidget: mobilepage:drag_widget事件响应函数
	 ***********************************************************/
	onDragWidget: function($mobilePage, itemUid, targetContainerUid) {
		if (!targetContainerUid) {
			//在page内移动，直接返回
			return;
		}

		var sourceContainerUid = W.component.getComponent(itemUid).pid + '';
		if (sourceContainerUid === targetContainerUid) {
			//在同一个容器内移动，直接返回
			return;
		}

		//调整component之间的包含关系
		xlog('[page manager]: drag ' + itemUid + '(' + (typeof itemUid) + ')' + ' from ' + sourceContainerUid + '(' + (typeof sourceContainerUid) + ')' + ' to ' + targetContainerUid + '(' + (typeof targetContainerUid) + ')');
		var component = W.component.getComponent(itemUid);
		var sourceComponent = W.component.getComponent(sourceContainerUid);
		var targetComponent = W.component.getComponent(targetContainerUid);
		targetComponent.addComponent(component);
		sourceComponent.dropSubComponent(component);

		//调用source component, target component的drag sort handler
		var $itemNode = $mobilePage.find('[data-cid="' + component.cid + '"]').eq(0);
		var $sourceNode = $mobilePage.find('[data-cid="' + sourceComponent.cid + '"]').eq(0);
		sourceComponent.dragSortHandler.handleComponentLeave($sourceNode, $itemNode, component);
		var $targetNode = $mobilePage.find('[data-cid="' + targetComponent.cid + '"]').eq(0);
		targetComponent.dragSortHandler.handleComponentEnter($targetNode, $itemNode, component);
	},

	/***********************************************************
	 * onClickAddPage: 点击“添加页面”按钮的响应函数
	 ***********************************************************/
	onClickAddPage: function(event) {
		this.$('input[name="pageName"]').val('');

		$('#addPageDialog').modal('toggle');
		var task = new W.DelayedTask(function() {
			this.$('input[name="pageName"]').focus();
		}, this);
		task.delay(500);
	},

	/***********************************************************
	 * onClickCopyPage: 点击“复制页面”按钮的响应函数
	 ***********************************************************/
	onClickCopyPage: function(event) {
		var currentPageJson = this.currentActivePage.toJSON();
		var currentPageJsonString = JSON.stringify(currentPageJson);
		var tempPage = W.component.Component.parseJSON(JSON.parse(currentPageJsonString), {
			createNewCid: true
		});
		var PageComponentConstructor = W.component.getComponentConstructorByType(W.projectType + ".page");
		page = new PageComponentConstructor({
			model: {
				title: currentPageJson.model.title + ' COPY'
			}
		});
		page.components = tempPage.components;
		this.addPage(page.model.get('title'), page);
	},

	/***********************************************************
	 * onClickMakeTemplate: 点击“创建模板”按钮的响应函数
	 ***********************************************************/
	onClickMakeTemplate: function(event) {
		W.Broadcaster.trigger('designpage:screenshot', function(dataUrl) {
			var $dialog = $('#makeTemplateDialog');
			$dialog.find('img').attr('src', dataUrl);
			$dialog.find('input[name="name"]').val('');
			$dialog.modal('toggle');

			var task = new W.DelayedTask(function() {
				$dialog.find('input[name="name"]').focus();
			}, this);
			task.delay(500);
		});
	},

	/***********************************************************
	 * onClickRemovePage: 点击“删除页面”按钮的响应函数
	 ***********************************************************/
	onClickRemovePage: function(event) {
		var $page = this.$('li.selected');

		//删除page component
		var curPageComponent = $page.data('component');
		this.pages = _.filter(this.pages, function(page) {
			return page.cid != curPageComponent.cid;
		});

		//删除dom node
		$page.removeData(['view', 'component']).remove();

		//active下一个page
		$page = this.$('li.page').eq(0);
		if ($page.length > 0) {
			this.activePage($page);
		}

		//调用api，后台删除
		W.getApi().call({
			app: 'workbench',
			api: 'page/delete',
			method: 'post',
			args: {
				project_id: W.projectId,
				page_id: curPageComponent.cid
			},
			success: function(data) {

			},
			error: function(resp) {
				alert('删除Page失败');
			}
		})
	},

	/***********************************************************
	 * onClickExportProject: 点击“导出工程”按钮的响应函数
	 ***********************************************************/
	onClickExportProject: function(event) {
		window.open('/termite/workbench/project/export/?project_id=' + W.projectId);
	},

	/***********************************************************
	 * onClickImportProject: 点击“导入工程”按钮的响应函数
	 ***********************************************************/
	onClickImportProject: function(event) {
		var $dialog = $('#importProjectDialog');
		if (!$dialog.attr('data-dialog-initialized')) {
			var $fileUploader = $dialog.find('#importProjectDialog-fileUploader').eq(0);
			$fileUploader.uploadify({
				swf: '/static/uploadify.swf',
				multi: false,
				removeCompleted: true,
				uploader: '/termite/workbench/project/import/',
				cancelImg: '/static/img/cancel.png',
				buttonText: '选择工程ZIP...',
				fileTypeDesc: '工程Zip文件',
				fileTypeExts: '*.zip',
				method: 'post',
				formData: {
					project_id: W.projectId
				},
				removeTimeout: 0.0,
				onUploadSuccess: function(file, path, response) {
					window.location.reload();
				},
				onUploadComplete: function() {},
				onUploadError: function(file, errorCode, errorMsg, errorString) {
					xlog(errorCode);
					xlog(errorMsg);
					xlog(errorString);
				}
			});

			$dialog.attr('data-dialog-initialized', true);
		}
		$dialog.modal('show');
	},

	/***********************************************************
	 * onClickPage: 点击“页面”的响应函数
	 ***********************************************************/
	onClickPage: function(event) {
		var $page = $(event.currentTarget);
		this.activePage($page);

		/*
        var $page = $(event.currentTarget);
        if ($page.hasClass('pageManager_addAction')) {
            return;
        }
        
        var pageView = $page.data('pageView');
        this.trigger('pagemanager:activepage', pageView.tabIndex);
        */
	},

	/***********************************************************
	 * onFinishInitDesignPage: design page的designpage:finish_init事件的响应函数
	 ***********************************************************/
	onFinishInitDesignPage: function() {
		if (this.currentActivePage) {
			W.Broadcaster.trigger('component:select', this.currentActivePage, 'designpage:finish_init');
		}
	},

	/***********************************************************
	 * onWaitForPage: design page的designpage:wait_for_page事件的响应函数
	 ***********************************************************/
	onWaitForPage: function() {
		if (this.currentActivePage) {
			W.Broadcaster.trigger('component:select', this.currentActivePage, 'designpage:wait_for_page');
		}
	},

	/***********************************************************
	 * onSelectPageComponentInDesignPage: design page的designpage:select_page_component事件的响应函数
	 * TODO: 不刷新页面
	 ***********************************************************/
	onSelectPageComponentInDesignPage: function() {
		var event = {};
		event.currentTarget = $('#pageManager li.page').get(0);
		this.onClickPage(event);
	},

	/***********************************************************
	 * onKeyup: 输入回车键的响应函数
	 ***********************************************************/
	onKeyup: function(event) {
		if (event.keyCode != 13) {
			return;
		}

		this.onClickSubmitPage();
	},

	/***********************************************************
	 * onClickSubmitPage: 点击“创建页面”按钮的响应函数
	 ***********************************************************/
	onClickSubmitPage: function(event) {
		var title = $.trim(this.$('input[name="pageName"]').val());
		if (!title) {
			alert('请输入页面名');
			return;
		}

		var $select = $('#addPageDialog select[name="pageTemplate"]');
		var pageTemplateId = parseInt($select.val());
		if (!pageTemplateId) {
			pageTemplateId = 0;
		}
		$('#addPageDialog').modal('hide');

		if (pageTemplateId === 0) {
			//空白页面
			var task = new W.DelayedTask(function() {
				this.addPage(title);
			}, this);
			task.delay(100);
		} else {
			var task = new W.DelayedTask(function() {
				var pageTemplate = this.id2pageTemplate[pageTemplateId];
				var tempPage = W.component.Component.parseJSON(JSON.parse(pageTemplate.pageJson), {
					createNewCid: true
				});
				var PageComponentConstructor = W.component.getComponentConstructorByType(W.projectType + ".page");
				page = new PageComponentConstructor({
					model: {
						title: title
					}
				});
				page.components = tempPage.components;
				this.addPage(title, page);
			}, this);
			task.delay(100);
		}

	},

	/***********************************************************
	 * onClickSubmitTemplate: 点击“创建模板”按钮的响应函数
	 ***********************************************************/
	onClickSubmitTemplate: function(event) {
		var $dialog = $('#makeTemplateDialog');
		var name = $dialog.find('input[name="name"]').val();
		if (!name) {
			alert('请输入模板名');
			return;
		}
		var image = $dialog.find('img').attr('src');
		image = image.replace(/^data:image\/(png|jpg);base64,/, "")
		var page = JSON.stringify(this.currentActivePage.toJSON());

		$dialog.modal('hide');
		W.getLoadingView().show();
		W.getApi().call({
			app: 'workbench',
			api: 'page_template/create',
			method: 'post',
			args: {
				project_id: W.projectId,
				image: image,
				page: page,
				name: name
			},
			success: function() {
				W.getLoadingView().hide();
				W.getSuccessHintView().show('创建封面成功!')
			},
			error: function() {
				W.getLoadingView().hide();
				alert('创建封面失败!')
			}
		});
	},

	/***********************************************************
	 * startGetPageTemplatesTask: 启动获取page template集合的task
	 ***********************************************************/
	/*
    startGetPageTemplatesTask: function() {
        //加载template page
        var task = new W.DelayedTask(function() {
            W.getApi().call({
                app: 'workbench',
                api: 'page_templates/get',
                args: {
                    project_type: W.projectType
                },
                scope: this,
                success: function(data) {
                    var pageTemplates = data;
                    var $select = $('#addPageDialog select[name="pageTemplate"]');
                    var items = [];
                    _.each(pageTemplates, function(pageTemplate) {
                        items.push('<option value="' + pageTemplate.id + '">' + pageTemplate.name + '</option>')
                        this.id2pageTemplate[pageTemplate.id] = pageTemplate;
                    }, this);
                    $select.empty().html(items.join(''));
                },
                error: function() {

                }
            })
        }, this);
        task.delay(300);
    },
    */

	/***********************************************************
	 * onChangePageTemplate: 切换page template的响应函数
	 ***********************************************************/
	/*
    onChangePageTemplate: function(event) {
        var $select = $(event.currentTarget);
        var pageTemplateId = parseInt($select.val());
        var pageTemplate = this.id2pageTemplate[pageTemplateId];
        var $image = $('#addPageDialog img');
        $image.attr('src', pageTemplate.url);
    },
    */

	/***********************************************************
	 * onClickSelectTemplate: 点击“切换模板”按钮的响应函数
	 ***********************************************************/
	onClickSelectTemplate: function(event) {
		/*
        var $link = $(event.currentTarget);
        $('#selectTemplateDialog').modal('toggle');
        W.getApi().call({
            app: 'webapp',
            api: 'project_templates/get',
            args: {
                project_id: W.projectId
            },
            success: function(data) {
                var templates = data;
                var items = [];
                _.each(templates, function(template) {
                    items.push('<label class="radio">' + 
                                '<input type="radio" name="template" value="' + template.id + '" />' + template.name +
                                '</label>');
                });
                var $node = $(items.join(''));
                var selector = 'input[value="' + W.projectId + '"]';
                $node.find(selector).attr('checked', 'checked');
                $('#selectTemplateDialog .modal-body').empty().html($node);
            },
            error: function() {
                alert('加载模板失败！');
            }
        })
        */
		W.dialog.showDialog('W.dialog.workbench.SelectTemplateeDialog', {
			success: function(data) {
				var targetTemplateProjectId = data.id;
				window.location.href = '/termite/workbench/project/edit/' + targetTemplateProjectId + '/';
				/*W.getApi().call({
                    app: 'webapp',
                    api: 'project_template/update',
                    method: 'post',
                    args: {
                        project_id: W.projectId,
                        target_project_inner_name: data.innerName
                    },
                    success: function(data) {
                        W.getLoadingView().hide();
                        window.location.href = '/termite/workbench/project/edit/' + targetTemplateProjectId + '/';
                    },
                    error: function() {
                        W.getLoadingView().hide();
                        alert('更新模板失败！');
                    }
                })*/
			}
		});
	},

	/***********************************************************
	 * onClickUpdateTemplate: 点击“切换模板”对话框的“确定”按钮的响应函数
	 ***********************************************************/
	/*
    onClickUpdateTemplate: function(event) {
        var $link = $(event.currentTarget);
        var templateId = $('#selectTemplateDialog input[type="radio"]:checked').val();

        $('#selectTemplateDialog').modal('hide');
        W.getLoadingView().show();
        W.getApi().call({
            app: 'webapp',
            api: 'project_template/update',
            method: 'post',
            args: {
                current_template_id: W.projectId,
                new_template_id: templateId
            },
            success: function(data) {
                W.getLoadingView().hide();
                window.location.href = '/termite/workbench/project/edit/' + templateId + '/';
            },
            error: function() {
                W.getLoadingView().hide();
                alert('加载模板失败！');
            }
      })
    }
    */
});