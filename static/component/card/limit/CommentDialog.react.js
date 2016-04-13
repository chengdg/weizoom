/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.datas:CommentDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var ShopStore = require('./ShopStore');
// var Constant = require('./Constant');
var Action = require('./Action');

var CommentDialog = Reactman.createDialog({
	getInitialState: function() {
		var shops = this.props.data.shops;
		return {
			comment: shops,
			checkedOptions: ShopStore.getcheckedOptions()
		}
	},

	onChange: function(checkedOptions, event) {
		this.setState({
			"checkedOptions": checkedOptions
		})
	},

	onBeforeCloseDialog: function() {
		if (this.state.checkedOptions.length == 0){
			Reactman.PageAction.showHint('error', '请至少选择一个');
		}else{
			this.closeDialog();
		}
	},

	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormCheckbox value={this.state.checkedOptions} options={this.state.comment} onChange={this.onChange} inDialog={true}/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = CommentDialog;