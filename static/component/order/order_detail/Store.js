/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data::Store');
var EventEmitter = require('events').EventEmitter
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher,{
	name:'CreateCardStore',

	actions:{
		'handleGetRuleIdResponse':Constant.GET_RULE_ID,
	},

	init: function() {
		this.data = {
			'rule_id' :0,
			'order_item_id': 0
		}
	},

	handleGetRuleIdResponse: function(action) {
		this.data.rule_id = action.data.rule_id;
		this.data.order_item_id = action.data.order_item_id;
		this.__emitChange();
	},
	
	getRuleId: function() {
		return this.data;
	},

});
module.exports = Store;