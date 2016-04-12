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
		'handleCreateCardRuleOrderResponse':Constant.CREATE_CRAD_RULE_ORDER,
		'handleUpdateProduct': Constant.CARD_DATA_UPDATE_PRODUCT,
		'handleUpdateAddProduct': Constant.CARD_DATA_UPDATE_ADD_PRODUCT,
		'handleGetRuleOrderList':Constant.CARD_RULE_ORDER,
		'handleAddCardLines':Constant.ADD_CARD_LINES,
	},
	init: function() {
		this.filter = {};
		this.data = {};
		this.data.card_order_list = {};
		this.data.cardlines = [{CardName:'',CardRuleNum:'',CardRuleTimeStart:'',CardRuleTimeEnd:''}];
	},
	handleUpdateProduct: function(action) {
		this.data[action.data.property] = action.data.value;
		this.__emitChange();
	},
	handleUpdateAddProduct: function(action) {
		this.data.cardlines[action.data.index][action.data.property] = action.data.value;
		this.__emitChange();
	},
	handleCreateCardRuleOrderResponse: function(action){
		window.location.href="/order/rule_order/";
		this.__emitChange();
	},
	handleGetRuleOrderList: function(action){
		this.data.card_order_list = JSON.parse(action.data.card_order_list);
		this.__emitChange();
	},
	handleAddCardLines:function() {
		this.data.cardlines.push({CardName:'',CardRuleNum:'',CardRuleTimeStart:'',CardRuleTimeEnd:''});
		this.__emitChange();
	},
	getData: function() {
		return this.data;
	},
	getCardRuleOrder: function() {
		return this.data.card_order_list;
	},

});
module.exports = Store;