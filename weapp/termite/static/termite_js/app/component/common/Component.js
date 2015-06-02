/**
 * @class W.component.Component
 * 组件的基类
 *
 */
W.component.Component = function(obj) {
	var obj = obj || {};
	this.initialize(obj);

	W.component.CID2COMPONENT[this.cid] = this;
}

W.component.cid = 1; //componenet id

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

		//增强property
		this.properties = _.deepClone(this.properties)
		if (this.properties && this.properties.length > 0) {
			var firstGroup = this.properties[0];
			var fields = firstGroup['fields'];
			fields.splice(0, 0, {
				name: 'id',
				type: 'text',
				displayName: 'Id',
				default: '',
			}, {
				name: 'class',
				type: 'text',
				displayName: 'Class',
				default: '',
			}, {
				name: 'name',
				type: 'text',
				displayName: 'Name',
				validate: 'required-none',
				default: '',
			}, {
				name: 'index',
				type: 'hidden',
				displayName: '',
				default: '-1',
			}, {
				name: 'datasource',
				type: 'hidden',
				displayName: '',
				default: {
					'type': 'api',
					'api_name': ''
				},
			});
		}

		this.name2field = {};
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
		if (!obj.shouldIgnoreSubComponent) {
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
		}

		//处理property的更新
		this.model.on('change', function(model) {
			var component = this;
			if (window.$M) { //window.$M将由mobile page通过parent.$M = $设置
				_.each(model.changed, function(value, name) {
					var handler = component.propertyChangeHandlers[name];
					if (handler) {
						//获得mobile page中的node
						var selector = '[data-cid="' + component.cid + '"]';
						var $node = $M(selector).eq(0);
						if ($node.length === 0) {
							$node = $M('body').eq(0);
						}
						//获得与dynamic component对应的property view中的node
						$propertyViewNode = null;
						if (component.selectable === 'no' || component.forceDisplayInPropertyView === 'yes') {
							$propertyViewNode = $('#propertyView [data-dynamic-cid="' + component.cid + '"]').eq(0);
						}
						xlog('[component] >>>>>>>>>>>>>>>>>>>> handle property change');
						xlog('[' + component.type + ']: change property "' + name + '" to: ' + value + '(' + typeof value + ')');
						handler.call(component, $node, model, value, $propertyViewNode);
						xlog('[component] <<<<<<<<<<<<<<<<<<<< handle property change');
					}
				});
			} else {
				xlog('waiting for $M');
			}

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

	/**
	 * addComponent: 加入子component
	 */
	addComponent: function(component, options) {
		xlog('[component]: add sub component ' + component.cid + ' into ' + this.cid);
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

	/**
	 * getComponentByCid: 根据cid获取component
	 */
	getComponentByCid: function(cid) {
		//return this.cid2component[cid];
		return W.component.CID2COMPONENT[cid];
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