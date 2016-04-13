/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.limit::ShopStore');
var EventEmitter = require('events').EventEmitter
var assign = require('object-assign');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var StoreUtil = Reactman.StoreUtil;

var Constant = require('./Constant');

var ShopStore = StoreUtil.createStore(Dispatcher, {
	actions: {
		'handleShowShops': Constant.CARD_SHOW_SHOPS,
		'handleAddShops': Constant.CARD_ADD_SHOP,
		'handleDeleteShop': Constant.CARD_DELETE_SHOP
	},

	init: function() {
		this.shops = []
		this.data = [];
		this.user_ids = [];
		this.checked = [];
	},
	handleShowShops: function(action){
		var shops = action.data.shops;
		this.shops = shops;
		var datas = []
		for (var i in shops){
			datas.push({
				"value": String(shops[i]["user_id"]),
				"text": shops[i]["store_name"]
			})
		}
		this.data = datas;
		this.__emitChange();
	},
	handleAddShops: function(action){
		console.log(action.data,"gggggggggggggg")
		var user_ids = action.data
		var shops = this.shops
		var checked = []
		for (var i in shops){
			for(var j in user_ids){
				if (shops[i]["user_id"] == user_ids[j]){
					checked.push(shops[i])
				}
			}
		}
		this.user_ids = user_ids;
		this.checked = checked;
		this.__emitChange();
	},
	handleDeleteShop: function(action){
		var user_id = action.data;
		var user_ids = this.user_ids;
		for(var i in user_ids){
			if (user_id == user_ids[i]){
				user_ids.splice(i,1)
			}
		}
		var shops = this.shops
		var checked = []
		for (var i in shops){
			for(var j in user_ids){
				if (shops[i]["user_id"] == user_ids[j]){
					checked.push(shops[i])
				}
			}
		}
		this.user_ids = user_ids;
		this.checked = checked;
		this.__emitChange();
	},
	getcheckedOptions: function(){
		return this.user_ids;
	},
	getCheckedShops: function(){
		return this.checked;
	},
	getShops: function(){
		return this.data;
	},
})

module.exports = ShopStore;