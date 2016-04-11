/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.create_ordinary:CreateOrindaryPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSelect = Reactman.FormSelect;
var FormSubmit = Reactman.FormSubmit;
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Action = require('./Action');
var Store = require('./Store');


var CreateOrindaryPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},
	onChangeStore: function() {
		this.setState(Store.getData());
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var data = Store.getData();
		data[property] = value;
		Action.addOrdinaryRuleInfo(data);
	},
	onSubmit: function() {
		Action.saveOrdinaryRule(Store.getData());
	},
	render:function(){
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<div className="pl10 pt10 pb10"><span style={{fontWeight: 'bold'}}>基本信息</span>（<span style={{color: 'red'}}>*</span>表示必填）</div>
					<FormInput label="卡名称:" type="text" name="name" value={this.state.name} placeholder="1-20个字，中英文、数字特殊符合均可" onChange={this.onChange} />
					<FormInput label="卡段号:" type="text" name="weizoom_card_id_prefix" value={this.state.weizoom_card_id_prefix} validate="require-three-number" placeholder="请输入3位数组" onChange={this.onChange} autoFocus={true}/>
					<FormSelect label="卡类型:" name="card_kind" options={[{"value": "-1", "text": "请选择"},{"value": "0", "text": "实体卡"},{"value": "1", "text": "电子卡"}]} onChange={this.onChange} />
					<FormInput label="面值:" type="text" name="money" value={this.state.money} validate="require-price" placeholder="" onChange={this.onChange} />
					<FormInput label="数量:" type="text" name="count" value={this.state.count} validate="require-positive-int" placeholder="" onChange={this.onChange} />
					<FormInput label="备注:" type="text" name="remark" value={this.state.remark} placeholder="" onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<FormSubmit onClick={this.onSubmit} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = CreateOrindaryPage;