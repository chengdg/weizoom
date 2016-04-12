/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.limit:Shops.react');

var React = require('react');
var Reactman = require('Reactman');
var CommentDialog = require('./CommentDialog.react');

var Action = require('./Action');
var ShopStore = require('./ShopStore');

var Shops = React.createClass({

	onClickComment: function(){
		Reactman.PageAction.showDialog({
			title: "请选择商家", 
			component: CommentDialog, 
			data: {
				shops: ShopStore.getShops()
			},
			success: function(inputData, dialogState) {
			}
		});

	},

	render:function(){
		var style = {
			display: "none"
		}
		if (this.props.visible){
			style["display"] = "block"
		}
		return (
		<div  className="form-group ml15" style={style}>
			<label className="col-sm-2 control-label"  htmlFor="parents_name">专属商家:</label>
			<a href="javascript:void(0)" className="ml15" onClick={this.onClickComment}>+添加商家</a> <input className="ml15" type="checkbox" name="is_new_member_special" ref="is_new_member_special"/> 新会员专属            
		</div>
		)
	}
})
module.exports = Shops;