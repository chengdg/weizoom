/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Action = require('.././rule_order/Action');
var Reactman = require('reactman');
var CardTable = require('./ApprovalDialogTable.react');


var ApprovalDialog = Reactman.createDialog({
	getInitialState: function() {
		return {
			common_status:true,
			limit_status:false
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
			var card = this.refs.CardTable.state;
			if (card==null) {
				Reactman.PageAction.showHint('error', '请选择一张卡!');
			}else if(!card.id){
				Reactman.PageAction.showHint('error', '请选择一张卡!');
			}else{
				this.setState({
					choiced_card:card ,
				});
				this.closeDialog();
			}
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

module.exports = ApprovalDialog;