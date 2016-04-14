/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.limit_rules::Store');
var EventEmitter = require('events').EventEmitter
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var Store = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleUpdateLimitRemark': Constant.CARD_LIMIT_UPDATE_REMARK,
	},

	init: function() {
		this.data = {
		}
	},

	handleUpdateLimitRemark: function(action) {
		this.__emitChange();
	},
	getData: function(){
		return this.data;
	}
})

module.exports = Store;