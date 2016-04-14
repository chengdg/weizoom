/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

// var Store = require('./Store');
// var Constant = require('./Constant');
// var Action = require('./Action');

var RemarkCommentDialog = Reactman.createDialog({
	getInitialState: function() {
		var rule = this.props.data.rule;
		return {
			remark: rule.remark
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		var rule = this.props.data.rule;
		Reactman.Resource.post({
			resource: 'card.limit',
			data: {
				rule_id: rule.id,
				remark: this.state.remark
			},
			success: function() {
				this.closeDialog();
			},
			error: function() {
				Reactman.PageAction.showHint('error', '备注失败!');
			},
			scope: this
		})
	},

	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormText label="备注:" name="remark" placeholder="" value={this.state.remark} onChange={this.onChange} autoFocus={true} inDialog={true} width={350} height={200}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = RemarkCommentDialog;