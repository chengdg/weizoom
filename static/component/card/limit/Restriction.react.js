/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:limit:Restriction');

var React = require('react');
var Store = require('./Store');
var Action = require('./Action');

var Restriction = React.createClass({
	onChange: function(event){
		if (event.target.value == 1){
			this.refs.fullUseValue.disabled = false;
			this.refs.fullUseValue.setAttribute('data-validate','require-int::金额必须为数字')
			
		}else{
			this.refs.fullUseValue.disabled = true;
			this.refs.fullUseValue.value = '';
			this.refs.fullUseHint.innerHTML = '';
			this.refs.fullUseValue.removeAttribute('data-validate')
		}
	},
	onChangeInput: function(event){
		var data = Store.getData();
		var property = event.target.name;
		data[property] = event.target.value;
		Action.addOrdinaryRuleInfo(data);
	},
	render:function(){
		return (
			<div className="form-group ml15">
				<label className="col-sm-2 control-label" htmlFor="full_use" >使用限制:</label>
				<div className="col-sm-5">
					<input type="radio" name="full_use" defaultChecked="true" value="-1" onChange={this.onChange} /><span className="pr15">不限制</span>
					<input type="radio" name="full_use" value="1" onChange={this.onChange} /><span className="pr10">满</span>
					<input type="text" className="w60" ref="fullUseValue" name="valid_restrictions" disabled data-validate="" onChange={this.onChangeInput} /><span className="pl10">元可以使用</span>
					<div className="errorHint" ref="fullUseHint" style={{marginLeft: '100px'}}></div>
				</div>
			</div>
		)
	}
})
module.exports = Restriction;
