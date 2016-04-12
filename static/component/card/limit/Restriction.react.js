/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:limit:Restriction');

var React = require('react');

var Restriction = React.createClass({

	render:function(){
		return (
			<div className="form-group ml15">
				<label className="col-sm-2 control-label" htmlFor="full_use" >使用限制:</label>
				<div className="col-sm-5">
					<input type="radio" name="full_use" defaultChecked="true" ref="noFullUse" /><span className="pr15">不限制</span>
					<input type="radio" name="full_use" ref="fullUse" /><span className="pr10">满</span>
					<input type="text" className="w60" ref="fullUseValue" disabled data-validate="" /><span className="pl10">元可以使用</span>
					<div className="errorHint" ref="fullUseHint" style={{marginLeft: '100px'}}></div>
				</div>
			</div>
		)
	}
})
module.exports = Restriction;
