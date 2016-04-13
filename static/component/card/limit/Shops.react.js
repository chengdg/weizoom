/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.limit:Shops.react');

var React = require('react');
var Reactman = require('Reactman');
var CommentDialog = require('./CommentDialog.react');

var Action = require('./Action');
var Store = require('./Store');
var ShopStore = require('./ShopStore');

var Shops = React.createClass({
	getInitialState: function(){
		ShopStore.addListener(this.onChangeShop);
		return({
			visible: false,
			checkedShops: []
		})
	},

	onClickComment: function(){
		var _this = this;
		Reactman.PageAction.showDialog({
			title: "请选择商家", 
			component: CommentDialog, 
			data: {
				shops: ShopStore.getShops()
			},
			success: function(inputData, dialogState) {
				Action.addCheckedShops(dialogState.checkedOptions);
				_this.props.onChangeShops();
			}
		});

	},
	deleteShop: function(event){
		var user_id = event.target.getAttribute('data-user-id');
		Action.deleteShop(user_id);
		this.props.onChangeShops();
	},
	onChangeShop: function(){
		this.setState({
			checkedShops: ShopStore.getCheckedShops()
		})
	},
	showShops: function(visible){
		this.setState({
			visible: visible
		})
	},
	render:function(){
		var style = {
			display: "none"
		}
		if (this.state.visible){
			style["display"] = "block"
		}
		var checkedShops = this.state.checkedShops;
		var _this = this;
		var checkedNodes = checkedShops.map(function(data,index){
			return(
				<div className="btn btn-info mr5" key={index}>
					<span className="mr5">{data.store_name}</span>
					<span>
						<span className="glyphicon glyphicon-remove" data-user-id={data.user_id} onClick={_this.deleteShop}></span>
					</span>
				</div>
			)
		});
		return (
			<div>
				<div  className="form-group ml15" style={style}>
					<label className="col-sm-2 control-label"  htmlFor="parents_name">专属商家:</label>
					<a href="javascript:void(0)" className="ml15" onClick={this.onClickComment}>+添加商家</a> <input className="ml15" type="checkbox" name="is_new_member_special" ref="is_new_member_special"/> 新会员专属            
				</div>
				<div className="form-group ml15">
					<label className="col-sm-2 control-label"></label>
					<div className="col-sm-5">
						{checkedNodes}
					</div>
				</div>
			</div>
		

		)
	}
})
module.exports = Shops;