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
		this.data = {"shopsVisible": false,shops:[]};
	},

	handleOrdinaryAddRuleInfo: function(action) {
		this.data = action.data;
		this.__emitChange();
	},
	handleShowShops: function(action){
		this.data.shops = action.data.shops;
		this.__emitChange();
	},
	getShops: function(){
		return this.data.shops;
	},

	handleSaveOrdinaryRule: function(action) {
		window.location.href = '/card/limit_rules/'
	},

	getData: function() {
		return this.data;
	}
})

module.exports = Store;