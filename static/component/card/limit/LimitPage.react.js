/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:card.create_limit:CreateLimitPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSelect = Reactman.FormSelect;
var FormRadio = Reactman.FormRadio;
var FormText = Reactman.FormText;

var FormSubmit = Reactman.FormSubmit;
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;
var Shops = require('./Shops.react')
var Restriction = require('./Restriction.react');

var Action = require('./Action');
var Store = require('./Store');
var ShopStore = require('./ShopStore');

require('./limit.css');

Reactman.Validater.addRule('require-three-number', {
	type: 'regex',
	extract: 'value',
	regex: /^\d{3,3}?$/g,
	errorHint: '格式不正确，请输入3位数'
});

var LimitPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		ShopStore.addListener(this.getShops);
		return Store.getData();
	},
	onChangeStore: function() {
		this.setState(Store.getData());
	},
	getShops: function(){
		this.setState({
			"shops": ShopStore.getShops(),
			"shopsVisible": true
		})
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		if (property == "card_kind"){
			if (value == "3"){
				Action.showShops();
				this.refs.Shops.showShops(true);
			}else{
				Action.addCheckedShops(["-1"]);
				this.onChangeShops();
				this.refs.Shops.showShops(false);
			}
		}
		var data = Store.getData();
		data[property] = value;
		Action.addOrdinaryRuleInfo(data);
	},
	onChangeShops: function(){
		var data = Store.getData();
		data["shop_limit_list"] = ShopStore.getcheckedOptions().toString();
		Action.addOrdinaryRuleInfo(data);
	},
	onSubmit: function() {
		var name_value = this.refs.name_input.refs.input.value;
		if (name_value.length >20){
			Reactman.PageAction.showHint('error', '名称最多输入20个字符！');
		}else{
			Action.saveOrdinaryRule(Store.getData());
		}
	},
	render:function(){
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<div className="pl10 pt10 pb10"><span style={{fontWeight: 'bold'}}>基本信息</span>（<span style={{color: 'red'}}>*</span>表示必填）</div>
					<FormInput label="卡名称:" type="text" name="name" value={this.state.name} placeholder="1-20个字，中英文、数字特殊符合均可" onChange={this.onChange} ref="name_input" />
					<FormInput label="卡段号:" type="text" name="weizoom_card_id_prefix" value={this.state.weizoom_card_id_prefix} validate="require-three-number" placeholder="请输入3位数组" onChange={this.onChange} />
					<span className="note">
						注：请输入卡号前3位数，以此数组为该批次卡的起始数。
					</span>
					<FormSelect label="卡类型:" name="card_kind" options={[{"value": "-1", "text": "请选择"},{"value": "2", "text": "条件卡"},{"value": "3", "text": "专属卡"}]} validate="require-select" onChange={this.onChange} />
					<Shops visible={this.state.shopsVisible} shops={this.state.shops} onChangeShops={this.onChangeShops} ref="Shops" />
					<Restriction />
					<FormInput label="面值:" type="text" name="money" value={this.state.money} validate="require-price" placeholder="" onChange={this.onChange} />
					<span className="money_note">
						元
					</span>
					<div></div>
					<FormInput label="数量:" type="text" name="count" value={this.state.count} validate="require-positive-int" placeholder="" onChange={this.onChange} />
					<span className="count_note">
						张
					</span>
					<FormText label="备注:" type="text" name="remark" value={this.state.remark} width="300" height="150" placeholder="" onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<FormSubmit onClick={this.onSubmit} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = LimitPage;