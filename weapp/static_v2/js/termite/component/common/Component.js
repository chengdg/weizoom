/**
 * @class W.component.Component
 * 组件的基类
 *
 */
ensureNS('W.component');
W.component.Component = function(obj) {
	var obj = obj || {};
	this.initialize(obj);

	W.component.CID2COMPONENT[this.cid] = this;
}

W.component.cid = 1; //componenet id
W.component.$validateEl = $('<input name="__to_be_validate" />'); //用于进行validate的element

// 相当于让Component继承自Backbone.Events，并增加了若干函数
_.extend(W.component.Component.prototype, Backbone.Events, {
	dragSortHandler: {
		handleComponentEnter: $.noop,
		handleComponentLeave: $.noop
	},

	/**
	 * getDisplayTitle: 获得用于显示的title
	 */
	getDisplayTitle: function() {
		var title = this.model.get('title');
		if (!title) {
			title = this.model.get('name');
		}
		if (!title) {
			title = this.model.get('text');
		}

		if (title && title.length > 10) {
			title = title.substring(0, 10) + '...';
		}
		return title;
	},

	render: function() {
		return W.Render.render(this.toJSON());
	},

	refresh: function($node, options) {
		if (W.Render) {
			var $componentContainer = null;
			if ($node && $node.attr("data-component-cid")) {
				$componentContainer = $node.parents('.xa-componentContainer').eq(0);
			}

			var $newNode = null;
			if ($componentContainer) {
				var html = W.Render.refresh(this.toJSON());
				$newNode = $(html);
				//删除旧节点
				$componentContainer.find('[data-component-cid]').remove();
				//插入新节点
				$componentContainer.prepend($newNode);
			}


			if (options && options.resize) {
				W.Broadcaster.trigger('component:resize', this);
			}

			var messageOptions = {};
			if (options && options.refreshPropertyView) {
				messageOptions.forceUpdatePropertyView = true;
			}
			W.Broadcaster.trigger('mobilewidget:select', this.cid, messageOptions, this);

			if (options && options.refreshPropertyViewForField) {
				W.Broadcaster.trigger('component:refresh_field_editor', options.refreshPropertyViewForField);
			}
		}

		return $newNode;
	},

	/**
	 * obj: 指导创建的对象，包含
	 *  1. model: 创建完component，需要初始化的model数据
	 *  2. shouldIgnoreSubComponent: 是否忽略创建子component
	 */
	initialize: function(obj) {
		//处理cid
		if (obj.cid) {
			this.cid = obj.cid;
			if (W.component.cid <= obj.cid) {
				W.component.cid = obj.cid + 1;
			}
		} else {
			this.cid = W.component.cid++;
			this.isNewCreated = true;
		}
		this.pid = null; //parent component id

		if (!this.shouldShowPropertyViewTitle) {
			this.shouldShowPropertyViewTitle = false;
		}

		//增强property
		this.properties = _.deepClone(this.properties)
		if (this.properties && this.properties.length > 0) {
			var firstGroup = this.properties[0];
			var fields = firstGroup['fields'];
			fields.splice(0, 0, {
				name: 'id',
				type: 'hidden',
				displayName: 'Id',
				isUserProperty: false,
				default: '',
			}, {
				name: 'class',
				type: 'text',
				displayName: 'Class',
				isUserProperty: false,
				default: '',
			}, {
				name: 'name',
				type: 'hidden',
				displayName: 'Name',
				isUserProperty: false,
				default: '',
			}, {
				name: 'index',
				type: 'hidden',
				displayName: '',
				isUserProperty: false,
				default: '-1',
			}, {
				name: 'datasource',
				isUserProperty: false,
				type: 'hidden',
				displayName: '',
				default: {
					'type': 'api',
					'api_name': ''
				},
			});
		}

		this.name2field = {};
		this.fields = [];
		this.mobileTemplate = null; //mobile的html片段模板

		this.model = this.createModel();
		if (obj && obj.model) {
			this.model.set(obj.model, {
				silent: true
			});

			//清除dynamic fields的内容
			var dynamicFields = _.filter(this.name2field, function(field, name) {
				return field.type === 'dynamic-generated-control';
			});
			_.each(dynamicFields, function(dynamicField) {
				this.model.set(dynamicField.name, [], {
					silent: true
				});
			}, this);
		}

		this.autoSelect = false;
		if (obj.hasOwnProperty('auto_select')) {
			this.autoSelect = obj.auto_select;
		}
		xwarn(this.autoSelect);

		//初始化property change handler
		if (!this.propertyChangeHandlers) {
			this.propertyChangeHandlers = {};
		}

		//初始化subComponentTypes
		if (!this.subComponentTypes) {
			this.subComponentTypes = [];
		}

		//初始化dynamicComponentTyeps
		if (!this.dynamicComponentTypes) {
			this.dynamicComponentTypes = [];
		}

		//管理子component
		this.components = [];
		this.cid2component = {};
		if (!obj.shouldIgnoreSubComponent) {
			_.each(this.subComponentTypes, function(componentType) {
				var component = W.component.Component.create(componentType.type, componentType.model);
				this.addComponent(component);
			}, this);
		}
		//管理dynamic component
		if (!obj.shouldIgnoreSubComponent && !this.shouldIgnoreSubComponent) {
			_.each(this.dynamicComponentTypes, function(componentType) {
				if (componentType.model) {
					//只有在提供model的情况下才创建dynamic component
					if (isNaN(componentType.model)) {
						var component = W.component.Component.create(componentType.type, componentType.model);
						this.addComponent(component);;
					} else {
						for (var i = 0; i < componentType.model; i++) {
							var component = W.component.Component.create(componentType.type, {});
							this.addComponent(component);
						}
					}
				}
			}, this);
		} else {
			xwarn('do not create dynamic component');
		}

		//处理property的更新
		this.model.on('change', function(model) {
			var component = this;
			if (window.$M) { //window.$M将由mobile page通过parent.$M = $设置
				_.each(model.changed, function(value, name) {
					var handler = component.propertyChangeHandlers[name];
					if (handler) {
						//获得mobile page中的node
						var selector = '[data-component-cid="' + component.cid + '"]';
						var $node = $M(selector).eq(0);
						if ($node.length === 0) {
							$node = $M('body').eq(0);
						}
						//获得与dynamic component对应的property view中的node
						$propertyViewNode = null;
						if (component.selectable === 'no' || component.forceDisplayInPropertyView === 'yes') {
							$propertyViewNode = $('#propertyView [data-dynamic-cid="' + component.cid + '"]').eq(0);
							if ($propertyViewNode.length === 0) {
								$propertyViewNode = $('#propertyView');
							}
						} else {
							$propertyViewNode = $('#propertyView');
						}
						xlog('[component] >>>>>>>>>>>>>>>>>>>> handle property change');
						xlog('[' + component.type + ']: change property "' + name + '" to: ' + value + '(' + typeof value + ')');
						handler.call(component, $node, model, value, $propertyViewNode);
						$node.find('a').attr('href', 'javascript:void(0);')
						xlog('[component] <<<<<<<<<<<<<<<<<<<< handle property change');
					}
				});
			} else {
				xlog('waiting for $M');
			}

			//W.Broadcaster.trigger('designpage:resize');
			this.trigger('component:change_property', this, model);
			W.Broadcaster.trigger('component:change_property', this, model);
		}, this);
	},

	/**
	 * createModel: 创建model
	 */
	createModel: function() {
		//搜集property
		var defaults = {};
		var property_groups = this.properties;
		var component = this;
		_.each(property_groups, function(group) {
			_.each(group.fields, function(field) {
				component.name2field[field.name] = field;
				component.fields.push(field);
				var defaultValue = '';
				if (field.hasOwnProperty('default')) {
					defaultValue = field["default"];
				}
				defaults[field.name] = defaultValue;
			})
		});

		defaults['index'] = this.cid;
		this.model = new Backbone.Model();
		this.model.set(defaults, {
			silent: true
		});
		return this.model;
	},

	getModel: function() {
		return this.model;
	},

	hasSubComponent: function() {
		return this.components.length > 1;
	},

	getIndex: function() {
		return this.model.get('index');
	},

	setIndex: function(newIndex) {
		this.model.set('index', newIndex);
	},

	incrementIndex: function() {
		var oldIndex = this.model.get('index');
		if (!oldIndex) {
			oldIndex = 0;
		}
		this.model.set('index', oldIndex+1);
	},

	getFieldByName: function(name) {
		return this.name2field[name];
	},

	__getSibling: function(target, direction) {
		var sortedSubComponents = _.sortBy(this.components, function(component) { return component.model.get('index'); });
		var count = sortedSubComponents.length;
		for (var i = 0; i < count; ++i) {
			var subComponent = sortedSubComponents[i];
			if (target.cid == subComponent.cid) {
				if (direction == 'prev') {
					if (i == 0) {
						return null;
					} else {
						return sortedSubComponents[i-1];
					}
				} else {
					if (i == count-1) {
						return null;
					} else {
						return sortedSubComponents[i+1];
					}
				}
			}
		}
		return null;
	},

	getPrevComponentOf: function(subComponent) {
		return this.__getSibling(subComponent, 'prev');
	},

	getNextComponentOf: function(subComponent) {
		return this.__getSibling(subComponent, 'next');
	},

	updateModel: function(modelData) {
	},

	/**
	 * addComponent: 加入子component
	 */
	addComponent: function(component, options) {
		xlog('[component]: add sub component ' + component.cid + ' into ' + this.cid);
		
		if (options && options.position) {
			var position = options.position;
			if (position < 0) {
				//如果options.position < 0，调整index，当前只处理position为-1的情况
				var maxIndexComponent = _.max(this.components, function(component) { return component.model.get('index')});
				var componentIndex = component.model.get('index');
				var maxComponentIndex = maxIndexComponent.model.get('index');
				if (componentIndex < maxComponentIndex) {
					//index顺序正确，do nothing
				} else {
					if (componentIndex === maxComponentIndex) {
						componentIndex += 1;
					}
					component.model.set('index', maxComponentIndex);
					maxIndexComponent.model.set('index', componentIndex);
				}
			} else {
				var sortedSubComponents = _.sortBy(this.components, function(component) { return component.model.get('index'); });
				var targetIndex = 0;
				var direction = options['direction'] || 'after';
				for (var i = 0; i < sortedSubComponents.length; ++i) {
					var tmpComponent = sortedSubComponents[i];
					if (tmpComponent.getIndex() === position) {
						if (direction === 'after') {
							targetIndex = i+1;
						} else {
							targetIndex = i;
						}
					}
				}

				if (targetIndex === sortedSubComponents.length) {
					var newIndex = sortedSubComponents[targetIndex-1].getIndex() + 1;
					component.setIndex(newIndex);
				} else {
					var targetComponent = sortedSubComponents[targetIndex];
					component.setIndex(targetComponent.getIndex());
					for (var i = targetIndex; i < sortedSubComponents.length; ++i) {
						sortedSubComponents[i].incrementIndex();
					}
				}
			}
		}

		this.components.push(component);
		this.cid2component[component.cid] = component;
		component.pid = this.cid;

		//尝试添加dynamic component
		var isDynamicComponent = (component.selectable === 'no' || component.forceDisplayInPropertyView === 'yes'); //selectable为no的component视为dynamic component
		if (isDynamicComponent) {
			var dynamicFields = _.filter(this.name2field, function(field, name) {
				return field.type === 'dynamic-generated-control';
			});
			if (dynamicFields.length > 0) {
				var dynamicField = dynamicFields[0];
				var dynamicValues = _.deepClone(this.model.get(dynamicField.name));
				var valueSet = {};
				_.each(dynamicValues, function(value) {
					valueSet[value] = 1;
				});
				if (!valueSet[component.cid]) {
					dynamicValues.push(component.cid);
					var silent = true;
					if (options && options.isAddDynamicComponent) {
						//根据options.isAddDynamicComponent判断是否需要更新mobile page
						silent = false;
					}
					this.model.set(dynamicField.name, dynamicValues, {
						silent: silent
					});
				}
			}
		}
	},

	insertComponentAfter: function(component, relatedComponent) {
		this.addComponent(component, {position:relatedComponent.getIndex(), direction:'after'})
	},

	/**
	 * getComponentByCid: 根据cid获取component
	 */
	getComponentByCid: function(cid) {
		//return this.cid2component[cid];
		return W.component.CID2COMPONENT[cid];
	},

	/**
	 * getComponentsByType: 根据type获取component集合
	 */
	getComponentsByType: function(type) {
		var components = _.filter(this.components, function(component) {
			return component.type === type;
		});
		return components;
	},

	/**
	 * dropSubComponent: 移除一个直接的sub component
	 */
	dropSubComponent: function(component) {
		cid = parseInt(component.cid);
		if (this.cid2component[cid]) {
			xlog('[component]: drop sub component ' + cid + ' from ' + this.cid);
			delete this.cid2component[cid];
			for (var i = 0; i < this.components.length; ++i) {
				if (this.components[i].cid === cid) {
					this.components.splice(i, 1);
				}
			}
		} else {
			xlog('[component]: no sub component to drop - ' + cid);
		}
	},

	/**
	 * removeComponent: 根据cid删除component
	 */
	removeComponent: function(cid) {
		cid = parseInt(cid);
		if (this.cid2component[cid]) {
			delete this.cid2component[cid];
			for (var i = 0; i < this.components.length; ++i) {
				if (this.components[i].cid === cid) {
					this.components.splice(i, 1);
				}
			}
		} else {
			_.each(this.components, function(component) {
				component.removeComponent(cid);
			})
		}

		if (W.component.CID2COMPONENT && W.component.CID2COMPONENT[cid]) {
			delete W.component.CID2COMPONENT[cid];
		}
	},

	isRootPage: function() {
		var pos = this.type.indexOf(".");
		if (pos == -1) {
			return (this.type === 'page');
		}

		pos += 1;
		var subType = this.type.substring(pos);
		return (subType === 'page');
	},

	canEditHtml: function() {
		if (this.capability) {
			return !!this.capability.editHtml;
		} else {
			return false;
		}
	},

	getDisplayValue: function(value, fieldName){
		if (!value) {
			var field = this.getFieldByName(fieldName);
			var data = {};
			value = field['default'];
			data[fieldName] = value;
			this.model.set(data, {silent: true});
		}
		return value;
	},

	__parseValidateInfo: function(str) {
		var result = {"data-force-validate":"true"};
		var validateInfos = str.split(/\s+/)
		for (var i = 0; i < validateInfos.length; ++i) {
			var validateInfo = validateInfos[i];
			var items = validateInfo.split('=');
			var attr = $.trim(items[0]);
			var value = $.trim(items[1]);
			value = value.substring(1, value.length-1);
			result[attr] = value;
		}

		return result;
	},

	validate: function() {
		var fields = this.fields;
		for (var i = 0; i < fields.length; ++i) {
			var field = fields[i];
			if (field.validate) {
				var attr2value = this.__parseValidateInfo(field.validate);
				var fieldValue = this.model.get(field.name);
				if (field.validateIgnoreDefaultValue) {
					if (fieldValue === field['default']) {
						fieldValue = '';
					}
				}
				W.component.$validateEl.attr('name', this.type+'-'+field.name).attr(attr2value).val(fieldValue);
				if (!W.validate(W.component.$validateEl)) {
					var targetCid = this.cid;
					if (this.pid) {
						var parentComponent = W.component.getComponent(this.pid);
						if (!parentComponent.isRootPage()) {
							targetCid = parentComponent.cid;
						}
						W.Broadcaster.trigger('mobilewidget:select', targetCid, {autoScroll: true}, this);
					} else {
						W.Broadcaster.trigger('designpage:select_page_component', targetCid, {autoScroll: true})
					}
					W.Broadcaster.trigger('component:display_error_hint');
					return false;
				}
			}
		}

		var sortedSubComponents = _.sortBy(this.components, function(component) { return component.model.get('index'); });
		for (var i = 0; i < sortedSubComponents.length; ++i) {
			var component = sortedSubComponents[i];
			if (!component.validate()) {
				return false;
			}
		}

		return true;
	},

	/**
	 * super: 调用基类函数
	 */
	"super": function(name) {
		var name = arguments[0];
		var args = Array.prototype.slice.call(arguments, 1);
		W.component.Component.prototype[name].apply(this, args);
	},

	/**
	 * toJSON: 转换为json
	 */
	toJSON: function() {
		var json = {};
		json.type = this.type;
		json.cid = this.cid;
		json.pid = this.pid;
		json.auto_select = this.autoSelect;

		json.selectable = "yes";
		if (this.selectable) {
			json.selectable = this.selectable;
		}

		json.force_display_in_property_view = "no";
		if (this.force_display_in_property_view) {
			json.force_display_in_property_view = this.forceDisplayInPropertyView;
		}

		json.has_global_content = "no";
		if (this.hasGlobalContent) {
			json.has_global_content = this.hasGlobalContent;
		}

		json.need_server_process_component_data = "no";
		if (this.needServerProcessComponentData) {
			json.need_server_process_component_data = "yes";
		}

		if (this.isNewCreated) {
			json.is_new_created = true;
		}
		json.property_view_title = this.propertyViewTitle;
		json.model = this.model.toJSON();

		if (this.components.length > 0) {
			var components = [];
			_.each(this.components, function(component) {
				components.push(component.toJSON());
			});
			json.components = components;
		} else {
			json.components = [];
		}

		return json;
	},

	/**
	 * dump: 输出component信息
	 */
	dump: function() {
		xlog('========== model ==========');
		xlog(this.toJSON());
		xlog('========== name2field ==========');
		xlog(this.name2field);
	}
});

W.component.Component.parseJSON = function(obj, options) {
	obj.shouldIgnoreSubComponent = true;
	if (options && options.createNewCid) {
		obj.cid = W.component.cid++;
	} else {
		obj.cid = parseInt(obj.cid);
	}
	var type = obj.type;
	var ComponentClass = W.component.TYPE2COMPONENT[type];
	xlog('type: ' + type + ', ComponentClass: ' + ComponentClass);
	var component = new ComponentClass(obj);

	if (obj.components) {
		_.each(obj.components, function(subComponentJsonObj) {
			component.addComponent(W.component.Component.parseJSON(subComponentJsonObj, options));
		});
	}

	return component;
}

W.component.Component.create = function(type, model) {
	xlog('[component factory]: create component ' + type);
	var ComponentClass = W.component.TYPE2COMPONENT[type];
	var component = new ComponentClass({
		model: model
	});

	return component;
}

//W.component.Component.extend = Backbone.Model.extend;
W.component.Component.extend = function() {
	//调用Backbone的extend，创建component class
	var componentClass = Backbone.Model.extend.apply(this, arguments);

	//注册<component type, component class>
	var componentType = arguments[0].type;
	W.component.register(componentType, componentClass);
	return componentClass;
};


/**
 * 组件集合
 */
W.component.COMPONENTS = []
W.component.TYPE2COMPONENT = {}
W.component.CID2COMPONENT = {}

W.component.register = function(type, component) {
	component.type = type;
	W.component.COMPONENTS.push(component);
	W.component.TYPE2COMPONENT[type] = component;
}

W.component.getSelectSource = function(nameOrArray, component) {
	if ($.isFunction(nameOrArray)) {
		return nameOrArray(component);
	} else if (typeof nameOrArray === 'string') {
		var obj = window;
		var items = nameOrArray.split('.');
		var itemCount = items.length;
		for (var i = 0; i < itemCount; ++i) {
			var item = items[i];
			if (obj.hasOwnProperty(item)) {
				obj = obj[item];
			} else {
				obj = [];
				break;
			}
		}

		if (obj === null) {
			obj = [];
		}
		return obj;
	} else {
		return nameOrArray;
	}
}

W.data.getData = function(nameOrObj) {
	if ($.isFunction(nameOrObj)) {
		var args = Array.prototype.slice.call(arguments, 1);
		return nameOrObj.apply(window, args);
	} else if (typeof nameOrObj === 'string') {
		if (nameOrObj[0] === '{') {
			//参数是一个object的字符串形式
			return $.parseJSON(nameOrObj);
		}

		var obj = window;
		var items = nameOrObj.split('.');
		var itemCount = items.length;
		for (var i = 0; i < itemCount; ++i) {
			var item = items[i];
			if (obj.hasOwnProperty(item)) {
				obj = obj[item];
			} else {
				obj = [];
				break;
			}
		}

		if (obj === null) {
			obj = [];
		}
		if ($.isFunction(obj)) {
			var args = Array.prototype.slice.call(arguments, 1);
			return obj.apply(window, args);
		} else {
			return obj;
		}
	} else {
		return nameOrObj;
	}
}

W.component.getFieldsByType = function(type) {
	return W.component.TYPE2COMPONENT[type].prototype.properties[0].fields;
}

W.component.getPropertyViewTitleByType = function(type) {
	return W.component.TYPE2COMPONENT[type].prototype.propertyViewTitle;
}

W.component.getComponent = function(cid) {
	return W.component.CID2COMPONENT[cid];
}

W.component.getComponentConstructorByType = function(type) {
	return W.component.TYPE2COMPONENT[type]
}