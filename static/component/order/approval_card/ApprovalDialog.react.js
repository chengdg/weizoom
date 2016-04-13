/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Action = require('.././rule_order/Action');
var Reactman = require('reactman');


var ApprovalDialog = Reactman.createDialog({
	getInitialState: function() {
		// Action.getLimitAndCommonCard();
		// var product = this.props.data.product;
		return {
			common_status:true,
			limit_status:false
			// comment: product.comment
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		if (this.state.comment === 'error') {
			Reactman.PageAction.showHint('error', '不能关闭对话框');
		} else {
			console.log(this.props.data.index,4444444444444444)
			// var product = this.props.data.product;
			// Reactman.Resource.post({
			// 	resource: 'outline.data_comment',
			// 	data: {
			// 		product_id: product.id,
			// 		comment: this.state.comment
			// 	},
			// 	success: function() {
			// 		this.closeDialog();
			// 	},
			// 	error: function() {
			// 		Reactman.PageAction.showHint('error', '评论失败!');
			// 	},
			// 	scope: this
			// })
		}
	},
	tabchange:function(status) {
		if (status=='common_status') {
			var common_status=true;
			var limit_status=false;
		}else{
			var common_status=false;
			var limit_status=true;
		}
		this.setState({
			common_status:common_status,
			limit_status:limit_status 
		});
		setTimeout(this.refs.CardTable.refs.table.refresh,0);
	},
	render:function(){
		var common_status = this.state.common_status;
		var limit_status = this.state.limit_status;
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<a href="javascript:void(0);" style={{cursor:common_status?'default':'pointer'}} onClick={this.tabchange.bind(this,'common_status')}>通用卡</a>&nbsp;&nbsp;
					<a href="javascript:void(0);" style={{cursor:limit_status?'default':'pointer'}} onClick={this.tabchange.bind(this,'limit_status')}>限制卡</a>
					<CardTable cardruletype={common_status?'common':'limit'} ref='CardTable'/>
				</fieldset>
			</form>
		</div>
		)
	}
})
//
var CardTable = React.createClass({
	rowFormatter: function(field, value, data) {
		// if (field === 'models') {
		// 	var models = value;
		// 	var modelEls = models.map(function(model, index) {
		// 		return (
		// 			<div key={"model"+index}>{model.name} - {model.stocks}</div>
		// 		)
		// 	});
		// 	return (
		// 		<div style={{color:'red'}}>{modelEls}</div>
		// 	);
		// } else if (field === 'name') {
		// 	return (
		// 		<a href={'/outline/data/?id='+data.id}>{value}</a>
		// 	)
		// }else if (field === 'action') {
		// 	return (
		// 	<div>
		// 		<a className="btn btn-link btn-xs" onClick={this.onClickDelete} data-product-id={data.id}>删除</a>
		// 		<a className="btn btn-link btn-xs mt5" href={'/outline/data/?id='+data.id}>编辑</a>
		// 		<a className="btn btn-link btn-xs mt5" onClick={this.onClickComment} data-product-id={data.id}>备注</a>
		// 	</div>
		// 	);
		// } else {
		// 	return value;
		// }
		if (field=='action') {
			return (
				<a className="btn btn-link btn-xs mt5" onClick={this.handleChoice}>选择</a>
				)
		} else {
			return value;
		}
	},
	render: function() {
		var cardruletype = this.props.cardruletype;
		var cardrulesResource= {
			resource: 'order.approval_card',
			data: {
				cardruletype:cardruletype,
			}
		};
		return (
			<Reactman.TablePanel>
				<Reactman.TableActionBar></Reactman.TableActionBar>
				<Reactman.Table resource={cardrulesResource} formatter={this.rowFormatter} pagination={true} countPerPage={2} ref="table">
					<Reactman.TableColumn name="卡名称" field="name" width="120px" />
					<Reactman.TableColumn name="面值" field="money" />
					<Reactman.TableColumn name="库存" field="storage_count" width="120px"/>
					<Reactman.TableColumn name="卡类型" field="card_kind" width="80px" />
					<Reactman.TableColumn name="卡号区间" field="card_range" />
					<Reactman.TableColumn name="操作" field="action" width="80px" />
				</Reactman.Table>
			</Reactman.TablePanel>
		);
	}
});
module.exports = ApprovalDialog;