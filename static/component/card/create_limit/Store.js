/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.create_ordinary::Store');
var EventEmitter = require('events').EventEmitter
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleOrdinaryAddRuleInfo': Constant.CARD_ADD_LIMIT_RULE_INFO,
		'handleSaveOrdinaryRule': Constant.CARD_DATA_SAVE_LIMIT_RULE
	},

	init: function() {
		this.data = {'id':-1, 'models':[]};
	},

	handleOrdinaryAddRuleInfo: function(action) {
		this.data = action.data;
		this.__emitChange();
	},

	handleSaveOrdinaryRule: function() {
		window.location.href = '/card/limit_rules/'
	},

	getData: function() {
		return this.data;
	}
})

module.exports = Store;