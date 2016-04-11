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
		'handleGetCardRuleResponse':Constant.GET_CARD_RULE
	},
	init: function() {
		this.data = {};
	},
	handleGetCardRuleResponse: function(action){
		console.log(action.data.card_rule_list);
		console.log("=========");
		this.data = action.data.card_rule_list;
		this.__emitChange();
	},
	getCardRule: function(){
		return this.data;
	}
});
module.exports = Store;